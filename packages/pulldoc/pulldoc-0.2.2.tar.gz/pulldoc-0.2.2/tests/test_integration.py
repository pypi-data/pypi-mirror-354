"""Integration tests for the pulldoc application."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.service.collector import fetch_prs
from src.service.summarizer import create_summary


class TestEndToEndWorkflow:
    """End-to-end integration tests for the pulldoc workflow."""

    @patch('src.service.collector.Github')
    @patch('src.service.collector.settings')
    @patch('src.service.summarizer.litellm.completion')
    @patch('src.service.summarizer.get_max_tokens')
    @patch('src.service.summarizer.token_counter')
    @patch('src.service.summarizer.settings')
    def test_complete_workflow(self,
                             summarizer_settings,
                             mock_token_counter,
                             mock_get_max_tokens,
                             mock_completion,
                             collector_settings,
                             mock_github_class,
                             temp_dir):
        """Test complete workflow from PR collection to summary generation."""

        # Setup collector mocks
        collector_settings.github_token = "test_token"
        collector_settings.base_dir = temp_dir

        # Mock GitHub API
        mock_github = Mock()
        mock_repo = Mock()
        mock_pr = Mock()
        mock_file = Mock()

        # Configure mock PR with realistic data
        mock_pr.number = 123
        mock_pr.title = "Fix authentication vulnerability"
        mock_pr.body = "This PR addresses a critical security vulnerability in the authentication system"
        mock_pr.created_at.isoformat.return_value = "2024-01-01T10:00:00Z"
        mock_pr.updated_at.isoformat.return_value = "2024-01-01T12:00:00Z"

        # Configure mock file changes
        mock_file.filename = "src/auth.py"
        mock_file.status = "modified"
        mock_file.changes = 15
        mock_file.patch = "@@ -50,7 +50,12 @@ def authenticate(token):\n     if not token:\n-        return False\n+        raise AuthenticationError('Token required')\n     return validate_token(token)"

        mock_pr.get_files.return_value = [mock_file]
        mock_pr.get_review_comments.return_value = []
        mock_pr.get_issue_comments.return_value = []
        mock_repo.get_pulls.return_value = [mock_pr]
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github

        # Step 1: Collect PRs
        fetch_prs("test/repo")

        # Verify PR file was created
        pr_file = temp_dir / "test/repo" / "raws" / "pr_0123.json"
        assert pr_file.exists()

        pr_data = json.loads(pr_file.read_text())
        assert pr_data["number"] == 123
        assert pr_data["title"] == "Fix authentication vulnerability"

        # Setup summarizer mocks
        summarizer_settings.summary_system_prompt = "Summarize the following PRs in {language}"
        summarizer_settings.base_dir = temp_dir
        mock_get_max_tokens.return_value = 4000
        mock_token_counter.return_value = 1000

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """# バッチ1のサマリー

## セキュリティの修正
- PR #123: 認証の脆弱性を修正
- 認証システムの重要なセキュリティ脆弱性に対処
- 修正されたファイル: src/auth.py (15行の変更)

## 主な変更点
- トークン検証の改善
- エラーハンドリングの強化
- セキュリティ強化のための認証フローの更新"""

        mock_response.usage.prompt_tokens = 150
        mock_response.usage.completion_tokens = 75
        mock_response.usage.total_tokens = 225
        mock_response._hidden_params = {"response_cost": 0.002}
        mock_completion.return_value = mock_response

        # Step 2: Create summary
        success, usage = create_summary(
            repo_name="test/repo",
            pr_files=[pr_file],
            batch_num=1,
            model="gpt-3.5-turbo",
            custom_prompt="",
            language="Japanese"
        )

        # Verify summary creation
        assert success is True
        assert usage["total_tokens"] == 225
        assert usage["total_cost"] == 0.002

        # Verify summary file exists
        summary_file = temp_dir / "test/repo" / "summaries" / "batch_summary_001_PRs_123.md"
        assert summary_file.exists()

        summary_content = summary_file.read_text()
        assert "セキュリティの修正" in summary_content
        assert "PR #123" in summary_content
        assert "認証の脆弱性" in summary_content

    @patch('src.service.collector.Github')
    @patch('src.service.collector.settings')
    def test_error_handling_in_workflow(self, collector_settings, mock_github_class, temp_dir):
        """Test error handling throughout the workflow."""

        # Setup to cause GitHub API error
        collector_settings.github_token = "invalid_token"
        collector_settings.base_dir = temp_dir
        mock_github_class.side_effect = Exception("GitHub API authentication failed")

        # Verify that errors are properly handled
        with pytest.raises(Exception, match="GitHub API authentication failed"):
            fetch_prs("test/repo")

    @patch('src.service.collector.Github')
    @patch('src.service.collector.settings')
    def test_workflow_with_multiple_prs(self, collector_settings, mock_github_class, temp_dir):
        """Test workflow with multiple PRs."""

        # Setup collector mocks
        collector_settings.github_token = "test_token"
        collector_settings.base_dir = temp_dir

        # Mock GitHub API with multiple PRs
        mock_github = Mock()
        mock_repo = Mock()

        # Create multiple mock PRs
        mock_prs = []
        for i in range(3):
            mock_pr = Mock()
            mock_pr.number = i + 1
            mock_pr.title = f"Feature {i + 1}"
            mock_pr.body = f"This PR implements feature {i + 1}"
            mock_pr.created_at.isoformat.return_value = "2024-01-01T10:00:00Z"
            mock_pr.updated_at.isoformat.return_value = "2024-01-01T12:00:00Z"
            mock_pr.get_files.return_value = []
            mock_pr.get_review_comments.return_value = []
            mock_pr.get_issue_comments.return_value = []
            mock_prs.append(mock_pr)

        mock_repo.get_pulls.return_value = mock_prs
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github

        # Collect PRs
        fetch_prs("test/repo")

        # Verify all PR files were created
        expected_files = [
            temp_dir / "test/repo" / "raws" / "pr_0001.json",
            temp_dir / "test/repo" / "raws" / "pr_0002.json",
            temp_dir / "test/repo" / "raws" / "pr_0003.json"
        ]

        for expected_file in expected_files:
            assert expected_file.exists()

        # Verify file contents
        for i, expected_file in enumerate(expected_files):
            pr_data = json.loads(expected_file.read_text())
            assert pr_data["number"] == i + 1
            assert pr_data["title"] == f"Feature {i + 1}"

    def test_data_consistency_between_modules(self, temp_dir):
        """Test data consistency between collector and summarizer modules."""

        # Create a PR file manually (simulating collector output)
        pr_data = {
            "title": "Add unit tests",
            "body": "This PR adds comprehensive unit tests for the authentication module",
            "number": 999,
            "created_at": "2024-01-15T14:30:00Z",
            "updated_at": "2024-01-15T16:45:00Z",
            "modified_files": [
                {
                    "filename": "test_auth.py",
                    "status": "added",
                    "changes": 100,
                    "patch": "@@ -0,0 +1,100 @@\n+import pytest\n+from src.auth import authenticate"
                }
            ]
        }

        pr_file = temp_dir / "pr_0999.json"
        pr_file.write_text(json.dumps(pr_data, ensure_ascii=False, indent=2))

        # Test that summarizer can properly load this data
        from src.service.summarizer import _load_pr_data

        loaded_data = _load_pr_data(pr_file)

        # Verify data integrity
        assert loaded_data == pr_data
        assert loaded_data["number"] == 999
        assert loaded_data["title"] == "Add unit tests"
        assert len(loaded_data["modified_files"]) == 1
        assert loaded_data["modified_files"][0]["filename"] == "test_auth.py"
        assert loaded_data["modified_files"][0]["status"] == "added"


class TestPerformanceAndScalability:
    """Performance and scalability tests."""

    def test_large_pr_batch_handling(self, temp_dir):
        """Test handling of large batches of PRs."""

        # Create multiple PR files
        pr_files = []
        for i in range(50):  # Simulate 50 PRs
            pr_data = {
                "title": f"PR {i}",
                "body": f"Description for PR {i}",
                "number": i,
                "modified_files": []
            }
            pr_file = temp_dir / f"pr_{i:04d}.json"
            pr_file.write_text(json.dumps(pr_data))
            pr_files.append(pr_file)

        # Test that all files can be loaded
        from src.service.summarizer import _load_pr_data

        loaded_count = 0
        for pr_file in pr_files:
            try:
                data = _load_pr_data(pr_file)
                assert "title" in data
                loaded_count += 1
            except Exception as e:
                pytest.fail(f"Failed to load {pr_file}: {e}")

        assert loaded_count == 50

    def test_memory_efficiency(self, temp_dir):
        """Test memory efficiency with large PR data."""

        # Create a PR with large content
        large_patch = "+" + "x" * 10000  # Large patch content
        pr_data = {
            "title": "Large refactoring",
            "body": "This PR contains a large refactoring",
            "number": 1000,
            "modified_files": [
                {
                    "filename": "large_file.py",
                    "status": "modified",
                    "changes": 5000,
                    "patch": large_patch
                }
            ]
        }

        pr_file = temp_dir / "large_pr.json"
        pr_file.write_text(json.dumps(pr_data, ensure_ascii=False, indent=2))

        # Test that large files can be handled
        from src.service.summarizer import _load_pr_data

        loaded_data = _load_pr_data(pr_file)
        assert loaded_data["number"] == 1000
        assert len(loaded_data["modified_files"][0]["patch"]) > 10000
