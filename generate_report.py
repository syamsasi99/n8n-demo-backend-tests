"""
Enhanced Test Report Generator
Processes pytest JSON output and generates a detailed test report
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def generate_enhanced_report(json_report_path: str = "test_results.json",
                             output_path: str = "test_report_enhanced.json"):
    """
    Generate an enhanced test report from pytest JSON output

    Args:
        json_report_path: Path to pytest JSON report
        output_path: Path for enhanced output report
    """
    try:
        with open(json_report_path, 'r') as f:
            pytest_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_report_path} not found. Run tests first.")
        sys.exit(1)

    # Extract test results
    tests = pytest_data.get('tests', [])

    # Categorize tests by outcome
    passed = [t for t in tests if t['outcome'] == 'passed']
    failed = [t for t in tests if t['outcome'] == 'failed']
    skipped = [t for t in tests if t['outcome'] == 'skipped']
    errors = [t for t in tests if t['outcome'] == 'error']

    # Build enhanced report
    enhanced_report = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "pytest_version": pytest_data.get('pytest_version', 'unknown'),
            "python_version": pytest_data.get('python', 'unknown'),
            "total_duration": pytest_data.get('duration', 0),
            "exit_code": pytest_data.get('exitcode', -1)
        },
        "summary": {
            "total_tests": len(tests),
            "passed": len(passed),
            "failed": len(failed),
            "skipped": len(skipped),
            "errors": len(errors),
            "pass_rate": round((len(passed) / len(tests) * 100), 2) if tests else 0,
            "fail_rate": round((len(failed) / len(tests) * 100), 2) if tests else 0
        },
        "test_results": {
            "passed": [
                {
                    "name": t['nodeid'],
                    "duration": t.get('duration', 0),
                    "outcome": t['outcome'],
                    "logs": extract_logs(t)
                }
                for t in passed
            ],
            "failed": [
                {
                    "name": t['nodeid'],
                    "duration": t.get('duration', 0),
                    "outcome": t['outcome'],
                    "error_message": t.get('call', {}).get('longrepr', 'No error message'),
                    "logs": extract_logs(t)
                }
                for t in failed
            ],
            "skipped": [
                {
                    "name": t['nodeid'],
                    "outcome": t['outcome'],
                    "reason": t.get('call', {}).get('longrepr', 'No reason provided')
                }
                for t in skipped
            ]
        },
        "performance_metrics": {
            "fastest_test": get_fastest_test(tests),
            "slowest_test": get_slowest_test(tests),
            "average_duration": round(sum(t.get('duration', 0) for t in tests) / len(tests), 3) if tests else 0
        }
    }

    # Write enhanced report
    with open(output_path, 'w') as f:
        json.dump(enhanced_report, f, indent=2)

    print(f"\n{'='*60}")
    print("TEST EXECUTION REPORT")
    print(f"{'='*60}")
    print(f"Total Tests: {enhanced_report['summary']['total_tests']}")
    print(f"Passed: {enhanced_report['summary']['passed']} ({enhanced_report['summary']['pass_rate']}%)")
    print(f"Failed: {enhanced_report['summary']['failed']} ({enhanced_report['summary']['fail_rate']}%)")
    print(f"Skipped: {enhanced_report['summary']['skipped']}")
    print(f"Errors: {enhanced_report['summary']['errors']}")
    print(f"Duration: {enhanced_report['report_metadata']['total_duration']:.2f}s")
    print(f"{'='*60}")
    print(f"\nEnhanced report saved to: {output_path}")

    return enhanced_report


def extract_logs(test_result):
    """Extract API logs from test result"""
    # Check if logs are present in the test metadata
    metadata = test_result.get('metadata', {})
    if 'logs' in metadata:
        return metadata['logs']

    # Check in user_properties (pytest-json-report stores them here)
    user_properties = test_result.get('user_properties', [])
    for prop in user_properties:
        # Handle both tuple format and dict format
        if isinstance(prop, (list, tuple)) and len(prop) == 2:
            key, value = prop
            if key == 'logs':
                return value
        elif isinstance(prop, dict) and 'logs' in prop:
            return prop['logs']

    # If no logs found, return None
    return None


def get_fastest_test(tests):
    """Get the fastest test"""
    if not tests:
        return None
    fastest = min(tests, key=lambda t: t.get('duration', float('inf')))
    return {
        "name": fastest['nodeid'],
        "duration": fastest.get('duration', 0)
    }


def get_slowest_test(tests):
    """Get the slowest test"""
    if not tests:
        return None
    slowest = max(tests, key=lambda t: t.get('duration', 0))
    return {
        "name": slowest['nodeid'],
        "duration": slowest.get('duration', 0)
    }


if __name__ == "__main__":
    generate_enhanced_report()
