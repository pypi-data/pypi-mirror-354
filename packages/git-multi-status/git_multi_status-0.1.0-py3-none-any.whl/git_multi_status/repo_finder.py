"""Repository finder for git-multi-status."""

import os
from typing import Generator

from rich.console import Console
from rich.text import Text

from .git_utils import is_git_repo

console = Console()


def find_git_repositories(start_dir: str, depth: int = 2, warn_not_repo: bool = False) -> Generator[str, None, None]:
    """Find all git repositories up to a certain depth.

    Args:
        start_dir: Directory to start searching from
        depth: Search depth (0=no recursion, -1=unlimited, >0=max depth)
        warn_not_repo: Whether to warn about non-git directories

    Yields:
        Paths to git repositories
    """
    start_dir = os.path.abspath(start_dir)

    if depth == 0:
        # Only check if the start_dir itself is a git repo
        if is_git_repo(start_dir):
            yield start_dir
        elif warn_not_repo:
            _warn_not_repo(start_dir)
        return

    for repo_path in _walk_directories(start_dir, depth, warn_not_repo):
        yield repo_path


def _walk_directories(start_dir: str, max_depth: int, warn_not_repo: bool) -> Generator[str, None, None]:
    """Walk directory tree looking for git repositories.

    Args:
        start_dir: Directory to start from
        max_depth: Maximum depth to search (-1 for unlimited)
        warn_not_repo: Whether to warn about non-git directories

    Yields:
        Paths to git repositories
    """
    for root, dirs, _ in os.walk(start_dir, followlinks=True):
        if ".git" in dirs:
            yield root
            # Don't descend into git repositories
            dirs.clear()
        elif warn_not_repo:
            _warn_not_repo(root)

        # Calculate current depth and stop if we've reached max depth
        if max_depth > 0:
            rel_path = os.path.relpath(root, start_dir)
            current_depth = len(rel_path.split(os.sep)) if rel_path != "." else 0

            if current_depth >= max_depth:
                dirs.clear()


def _warn_not_repo(path: str) -> None:
    """Display warning for non-git directory.

    Args:
        path: Directory path that is not a git repository
    """
    text = Text()
    text.append(f"{path}: ")
    text.append("Not a git repository", style="yellow")
    console.print(text)
