"""
Core validation models and logic for PyllmValidate.
"""

from typing import List
from pydantic import BaseModel


class FileInfo(BaseModel):
    """Information about a file in the git diff."""
    path: str
    status: str  # A (added), M (modified), D (deleted)
    insertions: int
    deletions: int
    content_before: str | None = None


class DiffAnalysis(BaseModel):
    """Analysis of git diff with file information."""
    files: List[FileInfo]
    git_diff_output: str


class AIResponse(BaseModel):
    """Response from AI validation."""
    correct: bool
    reason: str


# System prompt template for AI validation
SYSTEM_PROMPT_TEMPLATE = """
Description:
- You are running in a CLI tool to validate code patches.
- You should analyze the code patches for correctness
- The names of the function should have less weight to the overal decision

Input:
- File information and git diff output
- If no changes, treat as correct

{output_format}
""" 