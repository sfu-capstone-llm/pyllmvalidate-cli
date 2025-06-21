"""
Git utilities for analyzing repository changes.
"""

import sys
from git import InvalidGitRepositoryError, Repo
from ..validators.core import DiffAnalysis, FileInfo


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