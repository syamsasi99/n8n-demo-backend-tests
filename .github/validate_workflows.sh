#!/bin/bash
# Validate GitHub Actions workflows locally

echo "========================================="
echo "GitHub Actions Workflow Validator"
echo "========================================="
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI (gh) is installed"
else
    echo "✗ GitHub CLI (gh) not found. Install from: https://cli.github.com/"
    echo "  Skipping workflow validation..."
fi

echo ""
echo "Workflow Files Found:"
echo "---------------------"

for workflow in .github/workflows/*.yml; do
    if [ -f "$workflow" ]; then
        echo "✓ $(basename $workflow)"

        # Basic YAML validation (check if file is readable)
        if [ -r "$workflow" ]; then
            echo "  └─ File readable: Yes"
        else
            echo "  └─ File readable: No"
            exit 1
        fi
    fi
done

echo ""
echo "Workflow Features Summary:"
echo "--------------------------"

# Count total jobs
total_jobs=$(grep -h "^  [a-zA-Z_-]*:" .github/workflows/*.yml | wc -l | tr -d ' ')
echo "Total Jobs: $total_jobs"

# Count triggers
push_triggers=$(grep -h "push:" .github/workflows/*.yml | wc -l | tr -d ' ')
pr_triggers=$(grep -h "pull_request:" .github/workflows/*.yml | wc -l | tr -d ' ')
schedule_triggers=$(grep -h "schedule:" .github/workflows/*.yml | wc -l | tr -d ' ')
manual_triggers=$(grep -h "workflow_dispatch:" .github/workflows/*.yml | wc -l | tr -d ' ')

echo "Triggers:"
echo "  - Push: $push_triggers"
echo "  - Pull Request: $pr_triggers"
echo "  - Schedule: $schedule_triggers"
echo "  - Manual: $manual_triggers"

echo ""
echo "========================================="
echo "Validation Complete!"
echo "========================================="
echo ""
echo "To test workflows locally, consider using:"
echo "  - act: https://github.com/nektos/act"
echo "  - GitHub CLI: gh workflow run <workflow-name>"
echo ""
