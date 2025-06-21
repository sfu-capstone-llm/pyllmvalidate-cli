"""
Command-line interface for PyllmValidate.
"""

import argparse
import sys

from .utils.git_utils import get_git_diff
from .utils.ai_utils import init_ai_client, get_ai_response
from .utils.lint_utils import add_lint_context
from .validators.core import DiffAnalysis


def print_diff_summary(diff_analysis: DiffAnalysis):
    """Print diff summary."""
    print(f"\nFiles changed: {len(diff_analysis.files)}")

    for file_info in diff_analysis.files:
        print(
            f"  {file_info.path} ({file_info.status}) +{file_info.insertions}/-{file_info.deletions}"
        )

    print(f"\nGit diff output:\n{diff_analysis.git_diff_output}")
    print("=" * 50)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Validate code patches using AI")
    parser.add_argument("--env", action="store", help="Environment configuration")
    parser.add_argument("--lint-context", action="store_true", help="Include linting context")
    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_args()
    diff_analysis = get_git_diff()

    print_diff_summary(diff_analysis)

    if args.lint_context:
        diff_analysis.git_diff_output = add_lint_context(diff_analysis.git_diff_output)

    client = init_ai_client()

    # Get correctness
    is_correct = get_ai_response(
        "Only output 'true' or 'false' on correctness of the git diff.", 
        diff_analysis, 
        client
    )
    print(is_correct)

    if is_correct is None:
        print("no is_correct back from ai")
        sys.exit(1)

    # Get reason
    reason = get_ai_response(
        f"You stated that this git diff is {is_correct}. Tell us the reason why right away.", 
        diff_analysis, 
        client
    )

    response = {
        "is_correct": is_correct.strip().lower() == "true",
        "reason": reason.strip()
    }

    print(f"\nAI Result: {response}")


if __name__ == "__main__":
    main()
