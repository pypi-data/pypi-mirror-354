"""Tests for the summarizer module."""

import json
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest

from src.service.summarizer import (
    _load_pr_data,
    _save_summary,
    create_summary,
    make_llm_request,
)


class TestMakeLLMRequest:
    """Test class for make_llm_request function."""

    @patch('src.service.summarizer.litellm.completion')
    def test_make_llm_request_success(self, mock_completion):
        """Test successful LLM request."""
        # Setup mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test summary content"
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        mock_response._hidden_params = {"response_cost": 0.001}
        mock_completion.return_value = mock_response

        # Execute
        content, usage = make_llm_request(
            content="Test content",
            model="gpt-3.5-turbo",
            prompt="Test prompt"
        )

        # Verify
        assert content == "Test summary content"
        assert usage["prompt_tokens"] == 100
        assert usage["completion_tokens"] == 50
        assert usage["total_tokens"] == 150
        assert usage["total_cost"] == 0.001

        mock_completion.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Test prompt"},
                {"role": "user", "content": "Test content"},
            ],
            temperature=0.1,
            max_tokens=2000,
        )

    @patch('src.service.summarizer.litellm.completion')
    def test_make_llm_request_failure(self, mock_completion):
        """Test LLM request failure handling."""
        # Setup mock to raise exception
        mock_completion.side_effect = Exception("LLM API error")

        # Execute and verify exception is raised
        with pytest.raises(Exception, match="LLM API error"):
            make_llm_request(
                content="Test content",
                model="gpt-3.5-turbo",
                prompt="Test prompt"
            )


class TestLoadPRData:
    """Test class for _load_pr_data function."""

    def test_load_pr_data_success(self, sample_pr_file, sample_pr_data):
        """Test successful PR data loading."""
        result = _load_pr_data(sample_pr_file)

        assert result == sample_pr_data
        assert result["number"] == 123
        assert result["title"] == "Fix authentication bug"

    def test_load_pr_data_file_not_found(self):
        """Test handling of non-existent file."""
        non_existent_file = Path("/non/existent/file.json")

        with pytest.raises(Exception):
            _load_pr_data(non_existent_file)

    def test_load_pr_data_invalid_json(self, temp_dir):
        """Test handling of invalid JSON file."""
        invalid_file = temp_dir / "invalid.json"
        invalid_file.write_text("invalid json content")

        with pytest.raises(Exception):
            _load_pr_data(invalid_file)


class TestSaveSummary:
    """Test class for _save_summary function."""

    def test_save_summary_success(self, temp_dir):
        """Test successful summary saving."""
        output_path = temp_dir / "summary.txt"
        summary_content = "This is a test summary"

        _save_summary(summary_content, output_path)

        assert output_path.exists()
        assert output_path.read_text() == summary_content

    def test_save_summary_directory_creation(self, temp_dir):
        """Test summary saving with directory creation."""
        output_path = temp_dir / "new_dir" / "summary.txt"
        summary_content = "This is a test summary"

        # Create parent directory
        output_path.parent.mkdir(parents=True, exist_ok=True)
        _save_summary(summary_content, output_path)

        assert output_path.exists()
        assert output_path.read_text() == summary_content


class TestCreateSummary:
    """Test class for create_summary function."""

    @patch('src.service.summarizer.make_llm_request')
    @patch('src.service.summarizer.get_max_tokens')
    @patch('src.service.summarizer.token_counter')
    @patch('src.service.summarizer.settings')
    def test_create_summary_success(self, mock_settings, mock_token_counter,
                                  mock_get_max_tokens, mock_make_llm_request,
                                  sample_pr_file, temp_dir):
        """Test successful summary creation."""
        # Setup mocks
        mock_settings.summary_system_prompt = "Summarize in {language}"
        mock_settings.base_dir = temp_dir
        mock_get_max_tokens.return_value = 4000
        mock_token_counter.return_value = 1000
        mock_make_llm_request.return_value = ("Test summary", {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
            "total_cost": 0.001
        })

        # Execute
        success, usage = create_summary(
            repo_name="test/repo",
            pr_files=[sample_pr_file],
            batch_num=1,
            model="gpt-3.5-turbo",
            custom_prompt="",
            language="English"
        )

        # Verify
        assert success is True
        assert usage["total_tokens"] == 150
        mock_make_llm_request.assert_called_once()

    @patch('src.service.summarizer.make_llm_request')
    @patch('src.service.summarizer.get_max_tokens')
    @patch('src.service.summarizer.token_counter')
    @patch('src.service.summarizer.settings')
    def test_create_summary_token_limit_exceeded(self, mock_settings, mock_token_counter,
                                               mock_get_max_tokens, mock_make_llm_request,
                                               temp_dir):
        """Test summary creation when token limit is exceeded."""
        # Create multiple PR files
        pr_files = []
        for i in range(3):
            pr_data = {
                "title": f"PR {i}",
                "body": f"Body {i}",
                "number": i,
                "modified_files": []
            }
            pr_file = temp_dir / f"pr_{i:04d}.json"
            pr_file.write_text(json.dumps(pr_data))
            pr_files.append(pr_file)

        # Setup mocks - first call exceeds limit, subsequent calls are within limit
        mock_settings.summary_system_prompt = "Summarize in {language}"
        mock_settings.base_dir = temp_dir
        mock_get_max_tokens.return_value = 2000
        mock_token_counter.side_effect = [5000, 1000, 1000]  # First call exceeds, others OK
        mock_make_llm_request.side_effect = [
            ("Summary 1", {"prompt_tokens": 50, "completion_tokens": 25, "total_tokens": 75, "total_cost": 0.001}),
            ("Summary 2", {"prompt_tokens": 50, "completion_tokens": 25, "total_tokens": 75, "total_cost": 0.001})
        ]

        # Execute
        success, usage = create_summary(
            repo_name="test/repo",
            pr_files=pr_files,
            batch_num=1,
            model="gpt-3.5-turbo",
            custom_prompt="",
            language="English"
        )

        # Verify
        assert success is True
        assert usage["total_tokens"] == 150  # Sum of both calls
        assert mock_make_llm_request.call_count == 2

    @patch('src.service.summarizer._load_pr_data')
    def test_create_summary_load_error(self, mock_load_pr_data, temp_dir):
        """Test summary creation when PR data loading fails."""
        # Setup mock to raise exception
        mock_load_pr_data.side_effect = Exception("Load error")

        pr_file = temp_dir / "pr_0001.json"
        pr_file.touch()  # Create empty file

        # Execute and verify function returns False on error
        success, usage = create_summary(
            repo_name="test/repo",
            pr_files=[pr_file],
            batch_num=1,
            model="gpt-3.5-turbo",
            custom_prompt="",
            language="English"
        )

        # Verify failure is indicated
        assert success is False

    @patch('src.service.summarizer.make_llm_request')
    @patch('src.service.summarizer.get_max_tokens')
    @patch('src.service.summarizer.token_counter')
    @patch('src.service.summarizer.settings')
    def test_create_summary_with_custom_prompt(self, mock_settings, mock_token_counter,
                                             mock_get_max_tokens, mock_make_llm_request,
                                             sample_pr_file):
        """Test summary creation with custom prompt."""
        # Setup mocks
        mock_settings.base_dir = Path("/tmp")
        mock_get_max_tokens.return_value = 4000
        mock_token_counter.return_value = 1000
        mock_make_llm_request.return_value = ("Custom summary", {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
            "total_cost": 0.001
        })

        custom_prompt = "Create a detailed technical summary"

        # Execute
        success, usage = create_summary(
            repo_name="test/repo",
            pr_files=[sample_pr_file],
            batch_num=1,
            model="gpt-3.5-turbo",
            custom_prompt=custom_prompt,
            language="English"
        )

        # Verify custom prompt was used
        assert success is True
        call_args = mock_make_llm_request.call_args
        assert call_args[1]["prompt"] == custom_prompt


class TestIntegration:
    """Integration tests for summarizer functions."""

    @patch('src.service.summarizer.litellm.completion')
    @patch('src.service.summarizer.get_max_tokens')
    @patch('src.service.summarizer.token_counter')
    @patch('src.service.summarizer.settings')
    def test_end_to_end_summary_creation(self, mock_settings, mock_token_counter,
                                       mock_get_max_tokens, mock_completion,
                                       temp_dir):
        """Test end-to-end summary creation workflow."""
        # Create test PR file
        pr_data = {
            "title": "Fix critical bug",
            "body": "This PR fixes a critical authentication bug",
            "number": 456,
            "modified_files": [
                {"filename": "auth.py", "status": "modified", "changes": 5}
            ]
        }
        pr_file = temp_dir / "pr_0456.json"
        pr_file.write_text(json.dumps(pr_data, ensure_ascii=False, indent=2))

        # Setup mocks
        mock_settings.summary_system_prompt = "Summarize in {language}"
        mock_settings.base_dir = temp_dir
        mock_get_max_tokens.return_value = 4000
        mock_token_counter.return_value = 1000

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Comprehensive bug fix summary"
        mock_response.usage.prompt_tokens = 200
        mock_response.usage.completion_tokens = 100
        mock_response.usage.total_tokens = 300
        mock_response._hidden_params = {"response_cost": 0.002}
        mock_completion.return_value = mock_response

        # Execute
        success, usage = create_summary(
            repo_name="test/repo",
            pr_files=[pr_file],
            batch_num=1,
            model="gpt-4",
            custom_prompt="",
            language="Japanese"
        )

        # Verify
        assert success is True
        assert usage["total_tokens"] == 300
        assert usage["total_cost"] == 0.002

        # Verify summary file was created (filename format: batch_summary_001_PRs_456.md)
        summary_file = temp_dir / "test/repo" / "summaries" / "batch_summary_001_PRs_456.md"
        assert summary_file.exists()
        summary_content = summary_file.read_text()
        assert "Comprehensive bug fix summary" in summary_content
