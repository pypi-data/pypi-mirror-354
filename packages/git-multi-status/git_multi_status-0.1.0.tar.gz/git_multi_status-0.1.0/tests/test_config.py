"""Tests for config module."""

from git_multi_status.config import Config, RepoStatus


class TestConfig:
    """Test Config dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = Config()

        assert config.exclude_ok is False
        assert config.flatten is False
        assert config.show_branch is False
        assert config.warn_not_repo is False
        assert config.no_push is False
        assert config.no_pull is False
        assert config.no_upstream is False
        assert config.no_uncommitted is False
        assert config.no_untracked is False
        assert config.no_stashes is False
        assert config.do_fetch is False
        assert config.throttle == 0
        assert config.depth == 2
        assert config.debug is False
        assert config.directory == "."

    def test_custom_values(self):
        """Test custom configuration values."""
        config = Config(
            exclude_ok=True,
            flatten=True,
            show_branch=True,
            warn_not_repo=True,
            depth=5,
            debug=True,
            directory="/custom/path",
        )

        assert config.exclude_ok is True
        assert config.flatten is True
        assert config.show_branch is True
        assert config.warn_not_repo is True
        assert config.depth == 5
        assert config.debug is True
        assert config.directory == "/custom/path"


class TestRepoStatus:
    """Test RepoStatus dataclass."""

    def test_default_values(self):
        """Test default status values."""
        status = RepoStatus(path="/test/repo")

        assert status.path == "/test/repo"
        assert status.current_branch is None
        assert status.needs_push_branches == []
        assert status.needs_pull_branches == []
        assert status.needs_upstream_branches == []
        assert status.has_uncommitted is False
        assert status.has_untracked is False
        assert status.stash_count == 0
        assert status.is_locked is False
        assert status.is_ignored is False
        assert status.is_unsafe is False

    def test_is_ok_when_clean(self):
        """Test is_ok property when repository is clean."""
        status = RepoStatus(path="/test/repo")
        assert status.is_ok is True

    def test_is_ok_with_push_needed(self):
        """Test is_ok property when push is needed."""
        status = RepoStatus(path="/test/repo", needs_push_branches=["main"])
        assert status.is_ok is False

    def test_is_ok_with_pull_needed(self):
        """Test is_ok property when pull is needed."""
        status = RepoStatus(path="/test/repo", needs_pull_branches=["main"])
        assert status.is_ok is False

    def test_is_ok_with_upstream_needed(self):
        """Test is_ok property when upstream is needed."""
        status = RepoStatus(path="/test/repo", needs_upstream_branches=["feature"])
        assert status.is_ok is False

    def test_is_ok_with_uncommitted_changes(self):
        """Test is_ok property with uncommitted changes."""
        status = RepoStatus(path="/test/repo", has_uncommitted=True)
        assert status.is_ok is False

    def test_is_ok_with_untracked_files(self):
        """Test is_ok property with untracked files."""
        status = RepoStatus(path="/test/repo", has_untracked=True)
        assert status.is_ok is False

    def test_is_ok_with_stashes(self):
        """Test is_ok property with stashes."""
        status = RepoStatus(path="/test/repo", stash_count=2)
        assert status.is_ok is False

    def test_is_ok_when_locked(self):
        """Test is_ok property when repository is locked."""
        status = RepoStatus(path="/test/repo", is_locked=True)
        assert status.is_ok is False

    def test_is_ok_when_unsafe(self):
        """Test is_ok property when repository is unsafe."""
        status = RepoStatus(path="/test/repo", is_unsafe=True)
        assert status.is_ok is False

    def test_mutable_defaults_initialization(self):
        """Test that mutable default values are properly initialized."""
        status1 = RepoStatus(path="/test/repo1")
        status2 = RepoStatus(path="/test/repo2")

        # Modify one status
        status1.needs_push_branches.append("main")

        # Other status should not be affected
        assert status2.needs_push_branches == []
        assert status1.needs_push_branches == ["main"]
