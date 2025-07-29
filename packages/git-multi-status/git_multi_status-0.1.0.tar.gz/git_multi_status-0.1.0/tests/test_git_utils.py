"""Tests for git_utils module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from git_multi_status.git_utils import (
    GitError,
    check_repo_ownership,
    fetch_repo,
    get_current_branch,
    get_repo_config_bool,
    get_stash_count,
    is_git_repo,
    is_repo_locked,
    refresh_git_index,
    run_git_command,
)


class TestRunGitCommand:
    """Test run_git_command function."""

    def test_successful_command(self, git_repo: Path):
        """Test successful git command execution."""
        git_dir = str(git_repo / ".git")
        result = run_git_command(git_dir, None, "rev-parse", "--verify", "HEAD")
        assert len(result) == 40  # SHA-1 hash length

    def test_failed_command(self, git_repo: Path):
        """Test failed git command returns empty string."""
        git_dir = str(git_repo / ".git")
        result = run_git_command(git_dir, None, "rev-parse", "--verify", "nonexistent")
        assert result == ""

    def test_with_work_tree(self, git_repo: Path):
        """Test command with work tree specified."""
        git_dir = str(git_repo / ".git")
        result = run_git_command(git_dir, str(git_repo), "status", "--porcelain")
        assert isinstance(result, str)

    def test_debug_output(self, git_repo: Path, capsys):
        """Test debug output is produced when enabled."""
        git_dir = str(git_repo / ".git")
        run_git_command(git_dir, None, "rev-parse", "--verify", "HEAD", debug=True)
        captured = capsys.readouterr()
        assert "Running git command:" in captured.out

    @patch("subprocess.run")
    def test_timeout_error(self, mock_run):
        """Test timeout handling."""
        mock_run.side_effect = subprocess.TimeoutExpired("git", 1.0)

        with pytest.raises(GitError, match="Git command timed out"):
            run_git_command("/fake", None, "status")

    @patch("subprocess.run")
    def test_os_error(self, mock_run):
        """Test OS error handling."""
        mock_run.side_effect = OSError("Command not found")

        with pytest.raises(GitError, match="Failed to execute git command"):
            run_git_command("/fake", None, "status")


class TestIsGitRepo:
    """Test is_git_repo function."""

    def test_valid_git_repo(self, git_repo: Path):
        """Test detection of valid git repository."""
        assert is_git_repo(str(git_repo)) is True

    def test_non_git_directory(self, non_git_dir: Path):
        """Test detection of non-git directory."""
        assert is_git_repo(str(non_git_dir)) is False

    def test_nonexistent_directory(self):
        """Test nonexistent directory."""
        assert is_git_repo("/nonexistent/path") is False


class TestGetRepoConfigBool:
    """Test get_repo_config_bool function."""

    def test_existing_config_true(self, git_repo: Path):
        """Test reading existing config value (true)."""
        git_dir = str(git_repo / ".git")
        # Set a config value
        subprocess.run(["git", "config", "-f", f"{git_dir}/config", "test.value", "true"], check=True)

        result = get_repo_config_bool(git_dir, "test.value")
        assert result is True

    def test_existing_config_false(self, git_repo: Path):
        """Test reading existing config value (false)."""
        git_dir = str(git_repo / ".git")
        # Set a config value
        subprocess.run(["git", "config", "-f", f"{git_dir}/config", "test.value", "false"], check=True)

        result = get_repo_config_bool(git_dir, "test.value")
        assert result is False

    def test_nonexistent_config(self, git_repo: Path):
        """Test reading nonexistent config value."""
        git_dir = str(git_repo / ".git")
        result = get_repo_config_bool(git_dir, "nonexistent.key")
        assert result is False

    def test_nonexistent_config_with_default(self, git_repo: Path):
        """Test reading nonexistent config value with custom default."""
        git_dir = str(git_repo / ".git")
        result = get_repo_config_bool(git_dir, "nonexistent.key", True)
        assert result is True


class TestIsRepoLocked:
    """Test is_repo_locked function."""

    def test_unlocked_repo(self, git_repo: Path):
        """Test unlocked repository."""
        git_dir = str(git_repo / ".git")
        assert is_repo_locked(git_dir) is False

    def test_locked_repo(self, locked_repo: Path):
        """Test locked repository."""
        git_dir = str(locked_repo / ".git")
        assert is_repo_locked(git_dir) is True


class TestCheckRepoOwnership:
    """Test check_repo_ownership function."""

    def test_owned_repo(self, git_repo: Path):
        """Test repository owned by current user."""
        git_dir = str(git_repo / ".git")
        assert check_repo_ownership(git_dir) is True

    def test_nonexistent_repo(self):
        """Test nonexistent repository."""
        assert check_repo_ownership("/nonexistent/.git") is False


class TestRefreshGitIndex:
    """Test refresh_git_index function."""

    def test_successful_refresh(self, git_repo: Path):
        """Test successful index refresh."""
        git_dir = str(git_repo / ".git")
        # Should not raise an exception
        refresh_git_index(git_dir, str(git_repo))

    def test_failed_refresh(self):
        """Test failed index refresh."""
        # This should raise a GitError since the paths don't exist
        with pytest.raises(GitError):
            refresh_git_index("/nonexistent/.git", "/nonexistent")


class TestGetCurrentBranch:
    """Test get_current_branch function."""

    def test_main_branch(self, git_repo: Path):
        """Test getting current branch name."""
        git_dir = str(git_repo / ".git")
        branch = get_current_branch(git_dir)
        assert branch in ["main", "master"]  # Could be either depending on git version

    def test_feature_branch(self, git_repo_with_changes: Path):
        """Test getting feature branch name."""
        git_dir = str(git_repo_with_changes / ".git")
        branch = get_current_branch(git_dir)
        assert branch == "feature"


class TestGetStashCount:
    """Test get_stash_count function."""

    def test_no_stashes(self, git_repo: Path):
        """Test repository with no stashes."""
        git_dir = str(git_repo / ".git")
        count = get_stash_count(git_dir, str(git_repo))
        assert count == 0

    def test_with_stashes(self, git_repo_with_changes: Path):
        """Test repository with stashes."""
        git_dir = str(git_repo_with_changes / ".git")

        # Create a stash
        subprocess.run(["git", "stash"], cwd=git_repo_with_changes, check=True)

        count = get_stash_count(git_dir, str(git_repo_with_changes))
        assert count == 1


class TestFetchRepo:
    """Test fetch_repo function."""

    def test_successful_fetch(self, git_repo_with_remote: Path):
        """Test successful repository fetch."""
        git_dir = str(git_repo_with_remote / ".git")
        # Should not raise an exception
        fetch_repo(git_dir, str(git_repo_with_remote))

    def test_failed_fetch(self, git_repo: Path):
        """Test failed repository fetch (no remote)."""
        git_dir = str(git_repo / ".git")
        # Should not raise an exception even if no remote exists
        # fetch_repo just calls run_git_command which returns empty string on failure
        fetch_repo(git_dir, str(git_repo))
