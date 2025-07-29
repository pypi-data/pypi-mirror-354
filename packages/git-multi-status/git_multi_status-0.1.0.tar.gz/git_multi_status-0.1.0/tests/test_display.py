"""Tests for display module."""

from git_multi_status.config import Config, RepoStatus
from git_multi_status.display import StatusDisplay


class TestStatusDisplay:
    """Test StatusDisplay class."""

    def test_display_clean_repo(self, capsys):
        """Test displaying clean repository status."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo")

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo: ok" in captured.out

    def test_display_clean_repo_excluded(self, capsys):
        """Test displaying clean repository with exclude_ok enabled."""
        config = Config(exclude_ok=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo")

        display.display_status(status)

        captured = capsys.readouterr()
        assert captured.out.strip() == ""  # Should be empty

    def test_display_repo_with_branch(self, capsys):
        """Test displaying repository status with branch name."""
        config = Config(show_branch=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", current_branch="main")

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo (main): ok" in captured.out

    def test_display_repo_needs_push(self, capsys):
        """Test displaying repository that needs push."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", needs_push_branches=["main", "feature"])

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo: Needs push (main,feature)" in captured.out

    def test_display_repo_needs_pull(self, capsys):
        """Test displaying repository that needs pull."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", needs_pull_branches=["main"])

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo: Needs pull (main)" in captured.out

    def test_display_repo_needs_upstream(self, capsys):
        """Test displaying repository that needs upstream."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", needs_upstream_branches=["feature"])

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo: Needs upstream (feature)" in captured.out

    def test_display_repo_uncommitted_changes(self, capsys):
        """Test displaying repository with uncommitted changes."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", has_uncommitted=True)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo: Uncommitted changes" in captured.out

    def test_display_repo_untracked_files(self, capsys):
        """Test displaying repository with untracked files."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", has_untracked=True)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo: Untracked files" in captured.out

    def test_display_repo_with_stashes(self, capsys):
        """Test displaying repository with stashes."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", stash_count=3)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "/test/repo: 3 stashes" in captured.out

    def test_display_repo_multiple_issues(self, capsys):
        """Test displaying repository with multiple issues."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(
            path="/test/repo", needs_push_branches=["main"], has_uncommitted=True, has_untracked=True, stash_count=1
        )

        display.display_status(status)

        captured = capsys.readouterr()
        output = captured.out
        assert "/test/repo:" in output
        assert "Needs push (main)" in output
        assert "Uncommitted changes" in output
        assert "Untracked files" in output
        assert "1 stashes" in output

    def test_display_repo_flattened(self, capsys):
        """Test displaying repository status in flattened mode."""
        config = Config(flatten=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", needs_push_branches=["main"], has_uncommitted=True)

        display.display_status(status)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2  # Two separate lines
        assert "/test/repo: Needs push (main)" in lines[0]
        assert "/test/repo: Uncommitted changes" in lines[1]

    def test_display_unsafe_repo(self, capsys):
        """Test displaying unsafe repository."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", is_unsafe=True)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "Unsafe ownership" in captured.out

    def test_display_locked_repo(self, capsys):
        """Test displaying locked repository."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", is_locked=True)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "Locked. Skipping." in captured.out

    def test_display_ignored_repo(self, capsys):
        """Test displaying ignored repository."""
        config = Config()
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", is_ignored=True)

        display.display_status(status)

        captured = capsys.readouterr()
        assert captured.out.strip() == ""  # Should be empty

    def test_filter_push_status(self, capsys):
        """Test filtering push status with no_push option."""
        config = Config(no_push=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", needs_push_branches=["main"])

        display.display_status(status)

        captured = capsys.readouterr()
        assert "Needs push" not in captured.out
        assert "/test/repo: ok" in captured.out

    def test_filter_pull_status(self, capsys):
        """Test filtering pull status with no_pull option."""
        config = Config(no_pull=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", needs_pull_branches=["main"])

        display.display_status(status)

        captured = capsys.readouterr()
        assert "Needs pull" not in captured.out
        assert "/test/repo: ok" in captured.out

    def test_filter_upstream_status(self, capsys):
        """Test filtering upstream status with no_upstream option."""
        config = Config(no_upstream=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", needs_upstream_branches=["feature"])

        display.display_status(status)

        captured = capsys.readouterr()
        assert "Needs upstream" not in captured.out
        assert "/test/repo: ok" in captured.out

    def test_filter_uncommitted_status(self, capsys):
        """Test filtering uncommitted status with no_uncommitted option."""
        config = Config(no_uncommitted=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", has_uncommitted=True)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "Uncommitted changes" not in captured.out
        assert "/test/repo: ok" in captured.out

    def test_filter_untracked_status(self, capsys):
        """Test filtering untracked status with no_untracked option."""
        config = Config(no_untracked=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", has_untracked=True)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "Untracked files" not in captured.out
        assert "/test/repo: ok" in captured.out

    def test_filter_stashes_status(self, capsys):
        """Test filtering stashes status with no_stashes option."""
        config = Config(no_stashes=True)
        display = StatusDisplay(config)
        status = RepoStatus(path="/test/repo", stash_count=2)

        display.display_status(status)

        captured = capsys.readouterr()
        assert "stashes" not in captured.out
        assert "/test/repo: ok" in captured.out
