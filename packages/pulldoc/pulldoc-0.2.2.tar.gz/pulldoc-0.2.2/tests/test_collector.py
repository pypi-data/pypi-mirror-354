"""Tests for the collector module."""

import json
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest

from src.service.collector import fetch_prs


class TestFetchPRs:
    """Test class for fetch_prs function."""

    @patch('src.service.collector.settings')
    @patch('src.service.collector.Github')
    def test_fetch_prs_success(self, mock_github_class, mock_settings, temp_dir):
        """Test successful PR fetching."""
        # Setup mocks
        mock_settings.github_token = "test_token"
        mock_settings.base_dir = temp_dir

        # Mock GitHub API objects
        mock_github = Mock()
        mock_repo = Mock()
        mock_pr = Mock()
        mock_file = Mock()

        # Configure mock PR
        mock_pr.number = 123
        mock_pr.title = "Test PR"
        mock_pr.body = "Test PR body"
        mock_pr.created_at.isoformat.return_value = "2024-01-01T10:00:00Z"
        mock_pr.updated_at.isoformat.return_value = "2024-01-01T12:00:00Z"

        # Configure mock file
        mock_file.filename = "test.py"
        mock_file.status = "modified"
        mock_file.changes = 5
        mock_file.patch = "test patch"

        mock_pr.get_files.return_value = [mock_file]
        mock_pr.get_review_comments.return_value = []
        mock_pr.get_issue_comments.return_value = []
        mock_repo.get_pulls.return_value = [mock_pr]
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github

        # Execute
        fetch_prs("test/repo")

        # Verify
        mock_github_class.assert_called_once_with("test_token")
        mock_github.get_repo.assert_called_once_with("test/repo")
        mock_repo.get_pulls.assert_called_once_with(state="all", sort="created")

        # Check if file was created
        expected_dir = temp_dir / "test/repo" / "raws"
        expected_file = expected_dir / "pr_0123.json"
        assert expected_file.exists()

        # Verify file contents
        saved_data = json.loads(expected_file.read_text())
        assert saved_data["number"] == 123
        assert saved_data["title"] == "Test PR"
        assert saved_data["body"] == "Test PR body"
        assert len(saved_data["modified_files"]) == 1
        assert saved_data["modified_files"][0]["filename"] == "test.py"

    @patch('src.service.collector.settings')
    @patch('src.service.collector.Github')
    def test_fetch_prs_with_start_end(self, mock_github_class, mock_settings, temp_dir):
        """Test PR fetching with start and end parameters."""
        # Setup mocks
        mock_settings.github_token = "test_token"
        mock_settings.base_dir = temp_dir

        mock_github = Mock()
        mock_repo = Mock()
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github

        # Mock pulls list with slicing
        mock_pulls = [Mock() for _ in range(10)]
        for i, pr in enumerate(mock_pulls):
            pr.number = i + 1
            pr.title = f"PR {i + 1}"
            pr.body = f"Body {i + 1}"
            pr.created_at.isoformat.return_value = "2024-01-01T10:00:00Z"
            pr.updated_at.isoformat.return_value = "2024-01-01T12:00:00Z"
            pr.get_files.return_value = []
            pr.get_review_comments.return_value = []
            pr.get_issue_comments.return_value = []

        mock_repo.get_pulls.return_value = mock_pulls

        # Execute with start=2, end=4 (should process PRs 2-3)
        fetch_prs("test/repo", start=2, end=4)

        # Verify slicing (start=2 becomes index 1, end=4 stays 4)
        # Should process items at indices 1 and 2 (PRs 2 and 3)
        expected_files = [temp_dir / "test/repo" / "raws" / "pr_0002.json",
                         temp_dir / "test/repo" / "raws" / "pr_0003.json"]

        for expected_file in expected_files:
            assert expected_file.exists()

    @patch('src.service.collector.settings')
    @patch('src.service.collector.Github')
    def test_fetch_prs_github_error(self, mock_github_class, mock_settings):
        """Test handling of GitHub API errors."""
        # Setup mocks
        mock_settings.github_token = "test_token"
        mock_settings.base_dir = Path("/tmp")

        # Mock GitHub to raise an exception
        mock_github_class.side_effect = Exception("GitHub API error")

        # Execute and verify exception is raised
        with pytest.raises(Exception, match="GitHub API error"):
            fetch_prs("test/repo")

    @patch('src.service.collector.settings')
    @patch('src.service.collector.Github')
    def test_fetch_prs_pr_processing_error(self, mock_github_class, mock_settings, temp_dir):
        """Test handling of individual PR processing errors."""
        # Setup mocks
        mock_settings.github_token = "test_token"
        mock_settings.base_dir = temp_dir

        mock_github = Mock()
        mock_repo = Mock()
        mock_pr1 = Mock()
        mock_pr2 = Mock()

        # Configure first PR to raise error
        mock_pr1.number = 1
        mock_pr1.get_files.side_effect = Exception("PR processing error")

        # Configure second PR to succeed
        mock_pr2.number = 2
        mock_pr2.title = "Working PR"
        mock_pr2.body = "Working PR body"
        mock_pr2.created_at.isoformat.return_value = "2024-01-01T10:00:00Z"
        mock_pr2.updated_at.isoformat.return_value = "2024-01-01T12:00:00Z"
        mock_pr2.get_files.return_value = []
        mock_pr2.get_review_comments.return_value = []
        mock_pr2.get_issue_comments.return_value = []

        mock_repo.get_pulls.return_value = [mock_pr1, mock_pr2]
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github

        # Execute (should not raise exception)
        fetch_prs("test/repo")

        # Verify only second PR was saved
        expected_dir = temp_dir / "test/repo" / "raws"
        assert not (expected_dir / "pr_0001.json").exists()
        assert (expected_dir / "pr_0002.json").exists()

    @patch('src.service.collector.settings')
    @patch('src.service.collector.Github')
    def test_fetch_prs_empty_repository(self, mock_github_class, mock_settings, temp_dir):
        """Test fetching from repository with no PRs."""
        # Setup mocks
        mock_settings.github_token = "test_token"
        mock_settings.base_dir = temp_dir

        mock_github = Mock()
        mock_repo = Mock()
        mock_repo.get_pulls.return_value = []
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github

        # Execute
        fetch_prs("test/repo")

        # Verify directory is created but no PR files
        expected_dir = temp_dir / "test/repo" / "raws"
        assert expected_dir.exists()
        assert len(list(expected_dir.glob("pr_*.json"))) == 0
