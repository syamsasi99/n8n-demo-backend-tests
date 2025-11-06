#!/bin/bash
# Quick start script to run tests and generate reports

echo "========================================"
echo "Backend API Integration Test Framework"
echo "========================================"
echo ""

# Run pytest
echo "Running tests..."
pytest

# Check if tests ran successfully
if [ $? -eq 0 ] || [ -f "test_results.json" ]; then
    echo ""
    echo "Generating enhanced report..."
    python generate_report.py

    echo ""
    echo "========================================"
    echo "Reports generated:"
    echo "  - test_results.json (pytest report)"
    echo "  - test_report_enhanced.json (detailed report)"
    echo "========================================"
else
    echo "Error: Tests failed to run properly"
    exit 1
fi
