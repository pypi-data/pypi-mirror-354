"""Test fixtures and configuration for git-multi-status tests."""

import subprocess
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def git_repo(temp_dir: Path) -> Path:
    """Create a test git repository."""
    repo_dir = temp_dir / "test_repo"
    repo_dir.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)

    # Create initial commit
    (repo_dir / "README.md").write_text("# Test Repository")
    subprocess.run(["git", "add", "README.md"], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)

    return repo_dir


@pytest.fixture
def git_repo_with_changes(git_repo: Path) -> Path:
    """Create a git repository with various types of changes."""
    # Add untracked file
    (git_repo / "untracked.txt").write_text("Untracked content")

    # Add uncommitted changes
    (git_repo / "README.md").write_text("# Modified README")

    # Create and switch to new branch
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=git_repo, check=True)

    # Add some commits on feature branch
    (git_repo / "feature.txt").write_text("Feature content")
    subprocess.run(["git", "add", "feature.txt"], cwd=git_repo, check=True)
    subprocess.run(["git", "commit", "-m", "Add feature"], cwd=git_repo, check=True)

    return git_repo


@pytest.fixture
def git_repo_with_remote(git_repo: Path, temp_dir: Path) -> Path:
    """Create a git repository with a remote."""
    # Create bare remote repository
    remote_dir = temp_dir / "remote.git"
    remote_dir.mkdir()
    subprocess.run(["git", "init", "--bare"], cwd=remote_dir, check=True)

    # Add remote to repo
    subprocess.run(["git", "remote", "add", "origin", str(remote_dir)], cwd=git_repo, check=True)

    # Get the current branch name (might be main or master)
    result = subprocess.run(
        ["git", "branch", "--show-current"], cwd=git_repo, capture_output=True, text=True, check=True
    )
    current_branch = result.stdout.strip()

    # Push to remote
    subprocess.run(["git", "push", "-u", "origin", current_branch], cwd=git_repo, check=True)

    return git_repo


@pytest.fixture
def non_git_dir(temp_dir: Path) -> Path:
    """Create a non-git directory."""
    non_git = temp_dir / "not_git"
    non_git.mkdir()
    (non_git / "file.txt").write_text("Not a git repo")
    return non_git


@pytest.fixture
def nested_repos(temp_dir: Path) -> Path:
    """Create nested git repositories structure."""
    # Create main directory
    main_dir = temp_dir / "projects"
    main_dir.mkdir()

    # Create multiple repos at different levels
    for repo_name in ["repo1", "repo2", "subdir/repo3"]:
        repo_path = main_dir / repo_name
        repo_path.mkdir(parents=True)

        subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)

        (repo_path / "README.md").write_text(f"# {repo_name}")
        subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)

    return main_dir


@pytest.fixture
def locked_repo(git_repo: Path) -> Path:
    """Create a git repository with a lock file."""
    lock_file = git_repo / ".git" / "index.lock"
    lock_file.write_text("locked")
    return git_repo
