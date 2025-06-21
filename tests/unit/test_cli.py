"""
Unit tests for CLI module.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.pyllmvalidate.cli import parse_args, print_diff_summary
from src.pyllmvalidate.validators.core import DiffAnalysis, FileInfo


class TestCLI:
    """Test CLI functionality."""
    
    def test_parse_args_default(self):
        """Test parsing arguments with defaults."""
        with patch('sys.argv', ['cli.py']):
            args = parse_args()
            assert args.env is None
            assert args.lint_context is False
    
    def test_parse_args_with_options(self):
        """Test parsing arguments with options."""
        with patch('sys.argv', ['cli.py', '--env', 'test', '--lint-context']):
            args = parse_args()
            assert args.env == 'test'
            assert args.lint_context is True
    
    def test_print_diff_summary(self, capsys):
        """Test printing diff summary."""
        files = [
            FileInfo(path="file1.py", status="M", insertions=3, deletions=1),
            FileInfo(path="file2.py", status="A", insertions=5, deletions=0)
        ]
        
        diff_analysis = DiffAnalysis(
            files=files,
            git_diff_output="test diff output"
        )
        
        print_diff_summary(diff_analysis)
        captured = capsys.readouterr()
        
        assert "Files changed: 2" in captured.out
        assert "file1.py (M) +3/-1" in captured.out
        assert "file2.py (A) +5/-0" in captured.out
        assert "test diff output" in captured.out 