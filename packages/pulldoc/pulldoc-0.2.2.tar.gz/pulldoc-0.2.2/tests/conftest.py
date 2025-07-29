"""Pytest configuration and fixtures for pulldoc project."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def mock_github_repo():
    """Mock GitHub repository for testing."""
    mock_repo = Mock()
    mock_repo.get_pulls.return_value = []
    return mock_repo


@pytest.fixture
def mock_github_client():
    """Mock GitHub client for testing."""
    with patch('src.service.collector.Github') as mock_github:
        mock_client = Mock()
        mock_github.return_value = mock_client
        yield mock_client


@pytest.fixture
def sample_pr_data():
    """Sample PR data for testing."""
    return {
        "title": "Fix authentication bug",
        "body": "This PR fixes the authentication issue in the login module.",
        "number": 123,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z",
        "modified_files": [
            {
                "filename": "src/auth.py",
                "status": "modified",
                "changes": 10,
                "patch": "@@ -1,5 +1,5 @@\n def login():\n-    return False\n+    return True"
            }
        ]
    }


@pytest.fixture
def sample_pr_file(temp_dir, sample_pr_data):
    """Create a sample PR file for testing."""
    pr_file = temp_dir / "pr_0123.json"
    pr_file.write_text(json.dumps(sample_pr_data, ensure_ascii=False, indent=2))
    return pr_file


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    mock_settings = Mock()
    mock_settings.github_token = "mock_token"
    mock_settings.base_dir = Path("/tmp/test")
    mock_settings.summary_system_prompt = "Summarize the following PR in {language}: {content}"
    return mock_settings


@pytest.fixture
def mock_litellm():
    """Mock litellm responses for testing."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Mock summary content"
    mock_response.usage.prompt_tokens = 100
    mock_response.usage.completion_tokens = 50
    mock_response.usage.total_tokens = 150
    mock_response._hidden_params = {"response_cost": 0.001}

    with patch('src.service.summarizer.litellm.completion') as mock_completion:
        mock_completion.return_value = mock_response
        yield mock_completion
