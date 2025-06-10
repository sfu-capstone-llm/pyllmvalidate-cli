import argparse
import shutil
import subprocess
import sys
from typing import List

from git import InvalidGitRepositoryError, Repo
from openai import OpenAI
from pydantic import BaseModel


class FileInfo(BaseModel):
    path: str
    status: str  # A (added), M (modified), D (deleted)
    insertions: int
    deletions: int
    content_before: str | None = None


class DiffAnalysis(BaseModel):
    files: List[FileInfo]
    git_diff_output: str


class AIResponse(BaseModel):
    correct: bool
    reason: str


system_prompt_template = """
Description:
- You are running in a CLI tool to validate code patches.
- You should analyze the code patches for correctness
- The names of the function should have less weight to the overal decision

Input:
- File information and git diff output
- If no changes, treat as correct

Output:
- Always respond with JSON in STRING format specified by the pydantic JSON schema that's provided below
- Dot not include the markdown ```
- You MUST use this format for the output

Pydantic JSON schema:
{schema}

Example:
{{
    "correct": false,
    "reason": "The patch modifies the 'add' function to return `a * b` instead of `a - b`, which is likely incorrect because the function name suggests addition, not multiplication."
}}
"""


def analyze_diff_files(repo: Repo) -> DiffAnalysis:
    """Get file information for all files in the diff."""
    diffs = repo.index.diff(None)
    diff_output = repo.git.diff()

    files_info = []

    for diff_item in diffs:
        file_path = diff_item.a_path or diff_item.b_path
        assert file_path is not None

        # Get insertion/deletion counts
        insertions = deletions = 0
        try:
            diff_stats = repo.git.diff("--numstat", file_path).strip()
            if diff_stats and not diff_stats.startswith("-"):
                parts = diff_stats.split("\t")
                if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                    insertions = int(parts[0])
                    deletions = int(parts[1])
        except Exception:
            pass

        content_before = None
        if diff_item.change_type == "M":  # only show content_before for modified files
            try:
                content_before = repo.git.show(f"HEAD:{file_path}")
            except Exception:
                if diff_item.a_blob:
                    content_before = diff_item.a_blob.data_stream.read().decode(
                        "utf-8", errors="replace"
                    )

        if diff_item.change_type is None:
            continue

        files_info.append(
            FileInfo(
                path=file_path,
                status=diff_item.change_type,
                insertions=insertions,
                deletions=deletions,
                content_before=content_before,
            )
        )

    return DiffAnalysis(files=files_info, git_diff_output=diff_output)


def get_git_diff() -> DiffAnalysis:
    """Get git diff analysis."""
    try:
        repo = Repo(".")
        diff = analyze_diff_files(repo)
        print("DIFF", diff)
        return diff
    except InvalidGitRepositoryError:
        print("Error: current directory is not a valid git repository", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error getting git diff: {e}", file=sys.stderr)
        sys.exit(1)


def print_diff_summary(diff_analysis: DiffAnalysis):
    """Print diff summary."""
    print(f"\nFiles changed: {len(diff_analysis.files)}")

    for file_info in diff_analysis.files:
        print(
            f"  {file_info.path} ({file_info.status}) +{file_info.insertions}/-{file_info.deletions}"
        )

    print(f"\nGit diff output:\n{diff_analysis.git_diff_output}")
    print("=" * 50)


def main():
    args = parseArgs()
    diff_analysis = get_git_diff()

    print_diff_summary(diff_analysis)  # print(code_diff)

    if args.lint_context:
        diff_analysis.git_diff_output = add_lint_context(diff_analysis.git_diff_output)
        # print(diff_analysis)

    system_prompt = system_prompt_template.format(schema=AIResponse.model_json_schema())

    client = initAIClient()
    completion = client.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diff_analysis.git_diff_output},
        ],
    )

    _res = completion.choices[0].message.content
    print(_res)

    if _res is None:
        print("no res back from ai")
        return sys.exit(1)

    # Clean Markdown formatting if present
    # if _res.strip().startswith("```json"):
    #     _res = _res.strip().removeprefix("```json").removesuffix("```").strip()

    res = AIResponse.model_validate_json(_res)
    print(f"\nAI Result: {res}")


def add_lint_context(system_prompt: str) -> str:
    if not shutil.which("ruff"):
        print("Error: ruff is not installed or not in PATH")
        return sys.exit(1)

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


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", action="store")
    parser.add_argument("--lint-context", action="store_true")
    args = parser.parse_args()
    return args


def initAIClient() -> OpenAI:
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


if __name__ == "__main__":
    main()
