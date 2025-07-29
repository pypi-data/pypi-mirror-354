"""Tests for repo_finder module."""

from pathlib import Path

from git_multi_status.repo_finder import find_git_repositories


class TestFindGitRepositories:
    """Test find_git_repositories function."""

    def test_single_repo_depth_zero(self, git_repo: Path):
        """Test finding single repository with depth 0."""
        repos = list(find_git_repositories(str(git_repo), depth=0))
        assert len(repos) == 1
        assert repos[0] == str(git_repo)

    def test_non_git_dir_depth_zero(self, non_git_dir: Path):
        """Test non-git directory with depth 0."""
        repos = list(find_git_repositories(str(non_git_dir), depth=0))
        assert len(repos) == 0

    def test_non_git_dir_with_warning(self, non_git_dir: Path, capsys):
        """Test non-git directory with warning enabled."""
        repos = list(find_git_repositories(str(non_git_dir), depth=0, warn_not_repo=True))
        assert len(repos) == 0

        captured = capsys.readouterr()
        # Handle potential line wrapping in output
        import re

        normalized_output = re.sub(r"\s+", " ", captured.out)
        assert "Not a git repository" in normalized_output
        assert str(non_git_dir) in captured.out

    def test_nested_repos_depth_one(self, nested_repos: Path):
        """Test finding nested repositories with depth 1."""
        repos = list(find_git_repositories(str(nested_repos), depth=1))

        # Should find repo1 and repo2, but not repo3 (too deep)
        repo_names = [Path(repo).name for repo in repos]
        assert "repo1" in repo_names
        assert "repo2" in repo_names
        assert len(repos) == 2

    def test_nested_repos_depth_two(self, nested_repos: Path):
        """Test finding nested repositories with depth 2."""
        repos = list(find_git_repositories(str(nested_repos), depth=2))

        # Should find all repositories
        repo_names = [Path(repo).name for repo in repos]
        assert "repo1" in repo_names
        assert "repo2" in repo_names
        assert "repo3" in repo_names
        assert len(repos) == 3

    def test_nested_repos_unlimited_depth(self, nested_repos: Path):
        """Test finding nested repositories with unlimited depth."""
        repos = list(find_git_repositories(str(nested_repos), depth=-1))

        # Should find all repositories
        repo_names = [Path(repo).name for repo in repos]
        assert "repo1" in repo_names
        assert "repo2" in repo_names
        assert "repo3" in repo_names
        assert len(repos) == 3

    def test_empty_directory(self, temp_dir: Path):
        """Test empty directory."""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()

        repos = list(find_git_repositories(str(empty_dir), depth=2))
        assert len(repos) == 0

    def test_nonexistent_directory(self):
        """Test nonexistent directory."""
        repos = list(find_git_repositories("/nonexistent/path", depth=2))
        assert len(repos) == 0

    def test_absolute_path_conversion(self, git_repo: Path):
        """Test that relative paths are converted to absolute."""
        # Test with relative path
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(git_repo.parent)
            repos = list(find_git_repositories(git_repo.name, depth=0))
            assert len(repos) == 1
            assert os.path.isabs(repos[0])
        finally:
            os.chdir(old_cwd)

    def test_repo_in_subdirectory_not_descended(self, temp_dir: Path):
        """Test that we don't descend into git repositories."""
        # Create a git repo with another git repo inside it
        outer_repo = temp_dir / "outer"
        outer_repo.mkdir()

        import subprocess

        subprocess.run(["git", "init"], cwd=outer_repo, check=True, capture_output=True)

        # Create subdirectory with another git repo
        inner_dir = outer_repo / "inner"
        inner_dir.mkdir()
        subprocess.run(["git", "init"], cwd=inner_dir, check=True, capture_output=True)

        repos = list(find_git_repositories(str(temp_dir), depth=3))

        # Should only find the outer repo, not the inner one
        assert len(repos) == 1
        assert repos[0] == str(outer_repo)
