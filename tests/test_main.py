import pytest
from unittest.mock import Mock, patch
from main import DiffAnalysis, FileInfo, analyze_diff_files, get_git_diff

@pytest.fixture
def mock_repo():
    repo = Mock()
    repo.index.diff.return_value = []
    repo.git.diff.return_value = ""
    return repo

def test_analyze_diff_files_empty(mock_repo):
    result = analyze_diff_files(mock_repo)
    assert isinstance(result, DiffAnalysis)
    assert len(result.files) == 0
    assert result.git_diff_output == ""

def test_analyze_diff_files_with_changes(mock_repo):
    # Mock a modified file
    diff_item = Mock()
    diff_item.a_path = "test.py"
    diff_item.b_path = "test.py"
    diff_item.change_type = "M"
    diff_item.a_blob = None
    
    mock_repo.index.diff.return_value = [diff_item]
    
    # Set up the git.diff mock to handle different arguments
    def mock_diff(*args, **kwargs):
        if args and args[0] == "--numstat":
            return "1\t2"
        return "diff output"
    mock_repo.git.diff.side_effect = mock_diff
    # Mock git.show to return a string
    mock_repo.git.show.return_value = "old content"
    
    result = analyze_diff_files(mock_repo)
    assert isinstance(result, DiffAnalysis)
    assert len(result.files) == 1
    assert result.files[0].path == "test.py"
    assert result.files[0].status == "M"
    assert result.files[0].insertions == 1
    assert result.files[0].deletions == 2
    assert result.files[0].content_before == "old content"
    assert result.git_diff_output == "diff output"

@patch('main.Repo')
def test_get_git_diff_success(mock_repo_class, mock_repo):
    mock_repo_class.return_value = mock_repo
    result = get_git_diff()
    assert isinstance(result, DiffAnalysis)
    mock_repo_class.assert_called_once_with(".") 