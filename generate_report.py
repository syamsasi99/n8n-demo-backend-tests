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
                    "outcome": t['outcome']
                }
                for t in passed
            ],
            "failed": [
                {
                    "name": t['nodeid'],
                    "duration": t.get('duration', 0),
                    "outcome": t['outcome'],
                    "error_message": t.get('call', {}).get('longrepr', 'No error message'),
                    "error_type": extract_error_type(t)
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
        "failure_analysis": analyze_failures(failed),
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

    if failed:
        print(f"\nFAILURE ANALYSIS:")
        for error_type, count in enhanced_report['failure_analysis']['error_types'].items():
            print(f"  - {error_type}: {count}")

    return enhanced_report


def extract_error_type(test_result):
    """Extract the error type from test result"""
    longrepr = test_result.get('call', {}).get('longrepr', '')

    if isinstance(longrepr, str):
        if 'APIException' in longrepr:
            if '408' in longrepr or 'timeout' in longrepr.lower():
                return 'Timeout'
            elif '500' in longrepr:
                return 'Internal Server Error'
            elif '502' in longrepr:
                return 'Bad Gateway'
            elif '503' in longrepr:
                return 'Service Unavailable'
            elif '401' in longrepr:
                return 'Unauthorized'
            elif '403' in longrepr:
                return 'Forbidden'
            elif '404' in longrepr:
                return 'Not Found'
            elif '422' in longrepr:
                return 'Validation Error'
            elif '429' in longrepr:
                return 'Rate Limit Exceeded'
            elif '409' in longrepr:
                return 'Conflict'
            return 'API Exception'
        elif 'AssertionError' in longrepr:
            return 'Assertion Failed'

    return 'Unknown Error'


def analyze_failures(failed_tests):
    """Analyze patterns in test failures"""
    error_types = {}

    for test in failed_tests:
        error_type = extract_error_type(test)
        error_types[error_type] = error_types.get(error_type, 0) + 1

    return {
        "total_failures": len(failed_tests),
        "error_types": error_types,
        "most_common_error": max(error_types.items(), key=lambda x: x[1])[0] if error_types else None
    }


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
