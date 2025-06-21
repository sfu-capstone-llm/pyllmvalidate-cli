"""
Unit tests for validators module.
"""

import pytest
from src.pyllmvalidate.validators.core import FileInfo, DiffAnalysis, AIResponse


class TestFileInfo:
    """Test FileInfo model."""
    
    def test_file_info_creation(self):
        """Test creating a FileInfo instance."""
        file_info = FileInfo(
            path="test.py",
            status="M",
            insertions=5,
            deletions=2,
            content_before="old content"
        )
        
        assert file_info.path == "test.py"
        assert file_info.status == "M"
        assert file_info.insertions == 5
        assert file_info.deletions == 2
        assert file_info.content_before == "old content"
    
    def test_file_info_without_content_before(self):
        """Test creating a FileInfo instance without content_before."""
        file_info = FileInfo(
            path="new_file.py",
            status="A",
            insertions=10,
            deletions=0
        )
        
        assert file_info.content_before is None


class TestDiffAnalysis:
    """Test DiffAnalysis model."""
    
    def test_diff_analysis_creation(self):
        """Test creating a DiffAnalysis instance."""
        files = [
            FileInfo(path="file1.py", status="M", insertions=3, deletions=1),
            FileInfo(path="file2.py", status="A", insertions=5, deletions=0)
        ]
        
        diff_analysis = DiffAnalysis(
            files=files,
            git_diff_output="diff output here"
        )
        
        assert len(diff_analysis.files) == 2
        assert diff_analysis.git_diff_output == "diff output here"


class TestAIResponse:
    """Test AIResponse model."""
    
    def test_ai_response_creation(self):
        """Test creating an AIResponse instance."""
        response = AIResponse(
            correct=True,
            reason="The code changes are correct and follow best practices."
        )
        
        assert response.correct is True
        assert "correct" in response.reason.lower() 