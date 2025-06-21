"""
Linting utilities for code validation.
"""

import shutil
import subprocess
import sys


def add_lint_context(system_prompt: str) -> str:
    """Add ruff linting context to the system prompt."""
    if not shutil.which("ruff"):
        print("Error: ruff is not installed or not in PATH")
        sys.exit(1)

    prompt = system_prompt + "\n\n" + "Ruff linting context:\n"

    result = subprocess.run(
        ["ruff", "check"],
        capture_output=True,  # captures stdout and stderr
        text=True,  # returns output as string (instead of bytes)
    )

    if result.returncode == 0:
        prompt = prompt + result.stdout
    else:
        prompt = prompt + f"ruff check failed: {result.stdout}"
    return prompt 