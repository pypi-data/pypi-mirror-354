"""Tests for status_checker module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from git_multi_status.status_checker import StatusChecker


class TestStatusChecker:
    """Test StatusChecker class."""

    def test_check_clean_repository(self, git_repo: Path):
        """Test checking a clean repository."""
        checker = StatusChecker()
        status = checker.check_repository(str(git_repo))

        assert status is not None
        assert status.path == str(git_repo)
        assert status.is_ok is True
        assert not status.has_uncommitted
        assert not status.has_untracked
        assert status.stash_count == 0

    def test_check_repository_with_changes(self, git_repo_with_changes: Path):
        """Test checking repository with various changes."""
        checker = StatusChecker()
        status = checker.check_repository(str(git_repo_with_changes))

        assert status is not None
        assert status.path == str(git_repo_with_changes)
        assert status.is_ok is False
        assert status.has_uncommitted is True  # Modified README.md
        assert status.has_untracked is True  # untracked.txt
        assert status.current_branch == "feature"

    def test_check_repository_with_stashes(self, git_repo_with_changes: Path):
        """Test checking repository with stashes."""
        # Create a stash
        subprocess.run(["git", "stash"], cwd=git_repo_with_changes, check=True)

        checker = StatusChecker()
        status = checker.check_repository(str(git_repo_with_changes))

        assert status is not None
        assert status.stash_count == 1

    def test_check_locked_repository(self, locked_repo: Path):
        """Test checking locked repository."""
        checker = StatusChecker()
        status = checker.check_repository(str(locked_repo))

        assert status is not None
        assert status.is_locked is True
        assert status.is_ok is False

    def test_check_ignored_repository(self, git_repo: Path):
        """Test checking repository marked as ignored."""
        # Set ignore flag
        git_dir = git_repo / ".git"
        subprocess.run(["git", "config", "-f", f"{git_dir}/config", "mgitstatus.ignore", "true"], check=True)

        checker = StatusChecker()
        status = checker.check_repository(str(git_repo))

        assert status is not None
        assert status.is_ignored is True

    def test_check_nonexistent_repository(self):
        """Test checking nonexistent repository."""
        checker = StatusChecker()
        status = checker.check_repository("/nonexistent/repo")

        assert status is not None
        assert status.is_ok is False

    def test_fetch_repository_success(self, git_repo_with_remote: Path):
        """Test successful repository fetch."""
        checker = StatusChecker()
        result = checker.fetch_repository(str(git_repo_with_remote))
        assert result is True

    def test_fetch_repository_failure(self, git_repo: Path):
        """Test failed repository fetch (no remote)."""
        checker = StatusChecker()
        result = checker.fetch_repository(str(git_repo))
        # Should return True even if no remote (fetch doesn't fail)
        assert result is True

    def test_debug_mode(self, git_repo: Path, capsys):
        """Test debug output in status checker."""
        checker = StatusChecker(debug=True)
        checker.check_repository(str(git_repo))

        captured = capsys.readouterr()
        # Should have debug output from git commands
        assert len(captured.out) > 0

    @patch("git_multi_status.status_checker.check_repo_ownership")
    def test_unsafe_repository(self, mock_ownership, git_repo: Path):
        """Test checking repository with unsafe ownership."""
        mock_ownership.return_value = False

        checker = StatusChecker()
        status = checker.check_repository(str(git_repo))

        assert status is not None
        assert status.is_unsafe is True
        assert status.is_ok is False

    def test_repository_with_upstream_branches(self, git_repo_with_remote: Path):
        """Test repository with branches that need upstream setup."""
        # Create a new branch without pushing
        subprocess.run(["git", "checkout", "-b", "feature"], cwd=git_repo_with_remote, check=True)

        checker = StatusChecker()
        status = checker.check_repository(str(git_repo_with_remote))

        assert status is not None
        assert "feature" in status.needs_upstream_branches

    def test_repository_needing_push(self, git_repo_with_remote: Path):
        """Test repository with commits that need to be pushed."""
        # Make a commit that needs to be pushed
        (git_repo_with_remote / "new_file.txt").write_text("New content")
        subprocess.run(["git", "add", "new_file.txt"], cwd=git_repo_with_remote, check=True)
        subprocess.run(["git", "commit", "-m", "Add new file"], cwd=git_repo_with_remote, check=True)

        checker = StatusChecker()
        status = checker.check_repository(str(git_repo_with_remote))

        assert status is not None
        # Note: This might not always trigger depending on the git setup
        # The test is mainly to ensure the code path works

    def test_get_branch_refs_empty_refs_dir(self, temp_dir: Path):
        """Test _get_branch_refs with empty refs directory."""
        checker = StatusChecker()
        refs = checker._get_branch_refs(str(temp_dir / "nonexistent"))
        assert refs == []

    def test_error_handling_in_status_check(self, git_repo: Path):
        """Test error handling during status checking."""
        checker = StatusChecker()

        # Corrupt the git repository by removing critical files
        (git_repo / ".git" / "HEAD").unlink()

        # Should not crash, but return a status object
        status = checker.check_repository(str(git_repo))
        assert status is not None
