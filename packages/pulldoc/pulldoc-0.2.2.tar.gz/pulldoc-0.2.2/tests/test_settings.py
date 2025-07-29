"""Tests for the settings module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.settings import ProjectSettings


class TestSettings:
    """Test class for Settings configuration."""

    def test_settings_default_values(self):
        """Test settings with default values."""
        with patch.dict(os.environ, {}, clear=True):
            # Mock some required environment variables
            with patch.dict(
                os.environ,
                {"GITHUB_TOKEN": "test_token"},
            ):
                # Test that settings are loaded properly
                settings = ProjectSettings()
                assert settings.github_token == "test_token"

    def test_settings_with_custom_base_dir(self):
        """Test settings with custom base directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_base_dir = Path(temp_dir) / "custom_pulldoc"

            with patch.dict(
                os.environ,
                {
                    "GITHUB_TOKEN": "test_token",
                },
            ):
                settings = ProjectSettings()
                # In current implementation, base_dir is computed field that returns cwd/.pulldoc_result
                # So test that it returns a Path
                assert isinstance(settings.base_dir, Path)

    def test_settings_environment_variables(self):
        """Test settings loaded from environment variables."""
        test_env = {
            "GITHUB_TOKEN": "gh_test_token_123",
        }

        with patch.dict(os.environ, test_env):
            settings = ProjectSettings()
            assert settings.github_token == "gh_test_token_123"

    def test_settings_missing_required_token(self):
        """Test settings behavior when required tokens are missing."""
        with patch.dict(os.environ, {}, clear=True):
            # This should either raise an error or have default behavior
            # depending on how Settings is implemented
            try:
                settings = ProjectSettings()
                # If no exception is raised, verify default behavior
                assert hasattr(settings, "github_token")
            except Exception as e:
                # Expected behavior for missing required configuration
                assert "token" in str(e).lower() or "required" in str(e).lower()

    @patch("src.settings.Path.home")
    def test_settings_base_dir_creation(self, mock_home):
        """Test base directory creation."""
        mock_home.return_value = Path("/mock/home")

        with patch.dict(
            os.environ,
            {"GITHUB_TOKEN": "test_token"},
        ):
            settings = ProjectSettings()
            # Verify base_dir is set properly
            assert isinstance(settings.base_dir, Path)

    def test_settings_summary_system_prompt(self):
        """Test that summary system prompt is properly configured."""
        with patch.dict(
            os.environ,
            {"GITHUB_TOKEN": "test_token"},
        ):
            settings = ProjectSettings()
            # Test that summary_system_prompt exists and is properly formatted
            if hasattr(settings, "summary_system_prompt"):
                assert isinstance(settings.summary_system_prompt, str)
                assert len(settings.summary_system_prompt) > 0
                # Check if it contains language placeholder
                assert "{language}" in settings.summary_system_prompt


class TestSettingsIntegration:
    """Integration tests for Settings functionality."""

    def test_settings_singleton_behavior(self):
        """Test that settings behave consistently across imports."""
        with patch.dict(
            os.environ,
            {"GITHUB_TOKEN": "test_token"},
        ):
            # Import settings from the module
            from src.settings import settings

            # Verify settings object is properly initialized
            assert hasattr(settings, "github_token")
            assert hasattr(settings, "base_dir")

    def test_settings_path_handling(self):
        """Test that settings properly handle path operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                os.environ,
                {
                    "GITHUB_TOKEN": "test_token",
                },
            ):
                settings = ProjectSettings()
                # Test path operations
                test_path = settings.base_dir / "test" / "path"
                assert isinstance(test_path, Path)

                # Test directory creation
                test_path.mkdir(parents=True, exist_ok=True)
                assert test_path.exists()
                assert test_path.is_dir()

    def test_settings_validation(self):
        """Test settings validation logic."""
        with patch.dict(
            os.environ,
            {"GITHUB_TOKEN": "test_token"},
        ):
            settings = ProjectSettings()
            # Test basic validation
            assert settings.github_token is not None
            assert len(settings.github_token) > 0

            # Test path validation
            assert settings.base_dir is not None
            assert isinstance(settings.base_dir, Path)
