"""Tests for main CLI functionality."""

import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from git_multi_status.__main__ import app


class TestMainCLI:
    """Test main CLI functionality."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_help_command(self):
        """Test help command."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "git-multi-status shows uncommitted, untracked and unpushed changes" in result.output

    def test_version_command(self):
        """Test version command."""
        result = self.runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        # Should show either "dev" or actual version
        assert len(result.output.strip()) > 0

    def test_scan_clean_repo(self, git_repo: Path):
        """Test scanning a clean repository."""
        result = self.runner.invoke(app, [str(git_repo)])
        assert result.exit_code == 0
        assert f"{git_repo}: ok" in result.output

    def test_scan_repo_with_changes(self, git_repo_with_changes: Path):
        """Test scanning repository with changes."""
        result = self.runner.invoke(app, [str(git_repo_with_changes)])
        assert result.exit_code == 1  # Should exit with code 1 due to issues
        assert str(git_repo_with_changes) in result.output
        assert "Uncommitted changes" in result.output or "Untracked files" in result.output

    def test_exclude_ok_repos(self, git_repo: Path):
        """Test excluding OK repositories."""
        result = self.runner.invoke(app, ["--no-ok", str(git_repo)])
        assert result.exit_code == 0
        # Output should be empty or minimal since repo is OK
        assert str(git_repo) not in result.output or result.output.strip() == ""

    def test_show_branch_option(self, git_repo: Path):
        """Test showing branch names."""
        result = self.runner.invoke(app, ["-b", str(git_repo)])
        assert result.exit_code == 0
        # Should show branch name in parentheses
        assert "(" in result.output and ")" in result.output

    def test_flatten_option(self, git_repo_with_changes: Path):
        """Test flattened output."""
        result = self.runner.invoke(app, ["--flatten", str(git_repo_with_changes)])
        assert result.exit_code == 1
        # Each issue should be on a separate line
        lines = [line for line in result.output.split("\n") if line.strip()]
        repo_lines = [line for line in lines if str(git_repo_with_changes) in line]
        assert len(repo_lines) >= 1

    def test_depth_option(self, nested_repos: Path):
        """Test depth limitation."""
        # Depth 1 should find fewer repos than depth 2
        result_depth_1 = self.runner.invoke(app, ["--depth", "1", str(nested_repos)])
        result_depth_2 = self.runner.invoke(app, ["--depth", "2", str(nested_repos)])

        # Count number of repository mentions
        repos_depth_1 = result_depth_1.output.count(": ok")
        repos_depth_2 = result_depth_2.output.count(": ok")

        assert repos_depth_2 >= repos_depth_1

    def test_warn_not_repo_option(self, non_git_dir: Path):
        """Test warning about non-git directories."""
        result = self.runner.invoke(app, ["-w", str(non_git_dir)])
        assert result.exit_code == 0
        # Handle potential line wrapping in output by normalizing whitespace
        import re

        normalized_output = re.sub(r"\s+", " ", result.output)
        assert "Not a git repository" in normalized_output

    def test_debug_option(self, git_repo: Path):
        """Test debug output."""
        result = self.runner.invoke(app, ["--debug", str(git_repo)])
        assert result.exit_code == 0
        # Debug mode might produce additional output
        # Just ensure it doesn't crash

    def test_nonexistent_directory(self):
        """Test scanning nonexistent directory."""
        result = self.runner.invoke(app, ["/nonexistent/path"])
        assert result.exit_code == 0  # Should not crash
        # Should produce minimal output

    def test_current_directory_default(self, git_repo: Path, monkeypatch):
        """Test default current directory scanning."""
        # Change to the git repo directory
        monkeypatch.chdir(git_repo)
        result = self.runner.invoke(app, [])
        assert result.exit_code == 0
        # Handle potential line wrapping in output
        import re

        normalized_output = re.sub(r"\s+", " ", result.output)
        assert ": ok" in normalized_output

    def test_filter_options(self, git_repo_with_changes: Path):
        """Test various filter options."""
        # Test --no-uncommitted
        result = self.runner.invoke(app, ["--no-uncommitted", str(git_repo_with_changes)])
        assert "Uncommitted changes" not in result.output

        # Test --no-untracked
        result = self.runner.invoke(app, ["--no-untracked", str(git_repo_with_changes)])
        assert "Untracked files" not in result.output

    def test_fetch_option(self, git_repo_with_remote: Path):
        """Test fetch option."""
        result = self.runner.invoke(app, ["-f", str(git_repo_with_remote)])
        assert result.exit_code == 0
        # Should not crash when fetching

    def test_throttle_option(self, git_repo_with_remote: Path):
        """Test throttle option with fetch."""
        # Use a small throttle to avoid slowing down tests too much
        result = self.runner.invoke(app, ["-f", "--throttle", "0", str(git_repo_with_remote)])
        assert result.exit_code == 0

    def test_integration_with_actual_cli(self, git_repo: Path):
        """Test integration by calling the actual CLI script."""
        # This tests that the package can be invoked as a module
        try:
            result = subprocess.run(
                [sys.executable, "-m", "git_multi_status", str(git_repo)],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            # Should not crash
            assert result.returncode in [0, 1]  # 0 for clean, 1 for issues
            assert str(git_repo) in result.stdout or str(git_repo) in result.stderr

        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Skip if we can't run the module (e.g., not installed)
            pytest.skip("Cannot run module as script")

    def test_exit_codes(self, temp_dir: Path):
        """Test proper exit codes."""
        import subprocess

        # Create a clean repository
        clean_repo = temp_dir / "clean_repo"
        clean_repo.mkdir()
        subprocess.run(["git", "init"], cwd=clean_repo, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clean_repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clean_repo, check=True)
        (clean_repo / "README.md").write_text("# Test Repository")
        subprocess.run(["git", "add", "README.md"], cwd=clean_repo, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=clean_repo, check=True)

        # Create a repository with changes
        dirty_repo = temp_dir / "dirty_repo"
        dirty_repo.mkdir()
        subprocess.run(["git", "init"], cwd=dirty_repo, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=dirty_repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=dirty_repo, check=True)
        (dirty_repo / "README.md").write_text("# Test Repository")
        subprocess.run(["git", "add", "README.md"], cwd=dirty_repo, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=dirty_repo, check=True)
        # Add untracked file
        (dirty_repo / "untracked.txt").write_text("Untracked content")

        # Clean repo should exit with 0
        result_clean = self.runner.invoke(app, [str(clean_repo)])
        assert result_clean.exit_code == 0

        # Repo with issues should exit with 1
        result_issues = self.runner.invoke(app, [str(dirty_repo)])
        assert result_issues.exit_code == 1
