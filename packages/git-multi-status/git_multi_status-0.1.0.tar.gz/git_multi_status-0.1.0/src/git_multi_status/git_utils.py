"""Git utility functions for git-multi-status."""

import os
import subprocess
from typing import Optional

from rich.console import Console

console = Console()


class GitError(Exception):
    """Exception raised for git-related errors."""

    pass


def run_git_command(
    git_dir: Optional[str], work_tree: Optional[str], *args: str, timeout: float = 30.0, debug: bool = False
) -> str:
    """Run a git command and return its output.

    Args:
        git_dir: Path to .git directory
        work_tree: Path to working tree
        *args: Git command arguments
        timeout: Command timeout in seconds
        debug: Enable debug output

    Returns:
        Command output as string

    Raises:
        GitError: If command fails or times out
    """
    cmd = ["git"]
    if work_tree:
        cmd.extend(["--work-tree", work_tree])
    if git_dir:
        cmd.extend(["--git-dir", git_dir])
    cmd.extend(args)

    if debug:
        console.print(f"[dim]Running git command: {' '.join(cmd)}[/dim]")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)

        if result.returncode != 0:
            if debug:
                console.print(f"[dim]Command failed with return code: {result.returncode}[/dim]")
                if result.stderr:
                    console.print(f"[dim]Error: {result.stderr.strip()}[/dim]")
            return ""

        output = result.stdout.strip()
        if debug and output:
            console.print(f"[dim]Command output: {output}[/dim]")

        return output

    except subprocess.TimeoutExpired as e:
        raise GitError(f"Git command timed out after {timeout}s: {' '.join(cmd)}") from e
    except OSError as e:
        raise GitError(f"Failed to execute git command: {e}") from e


def is_git_repo(path: str) -> bool:
    """Check if a directory is a git repository.

    Args:
        path: Directory path to check

    Returns:
        True if directory contains a .git subdirectory
    """
    git_path = os.path.join(path, ".git")
    return os.path.isdir(git_path)


def get_repo_config_bool(git_dir: str, key: str, default: bool = False) -> bool:
    """Get a boolean configuration value from git config.

    Args:
        git_dir: Path to .git directory
        key: Configuration key
        default: Default value if key not found

    Returns:
        Configuration value as boolean
    """
    git_conf = os.path.join(git_dir, "config")
    try:
        value = run_git_command(git_dir, None, "config", "-f", git_conf, "--bool", key)
        if not value:  # Empty string means command failed
            return default
        return value.lower() == "true"
    except GitError:
        return default


def is_repo_locked(git_dir: str) -> bool:
    """Check if repository is locked.

    Args:
        git_dir: Path to .git directory

    Returns:
        True if repository has an index.lock file
    """
    return os.path.exists(os.path.join(git_dir, "index.lock"))


def check_repo_ownership(git_dir: str) -> bool:
    """Check if current user owns the git directory.

    Args:
        git_dir: Path to .git directory

    Returns:
        True if current user owns the directory, False otherwise
    """
    try:
        git_dir_owner = os.stat(git_dir).st_uid
        current_user_id = os.getuid()
        return current_user_id == git_dir_owner
    except OSError:
        return False


def refresh_git_index(git_dir: str, work_tree: str, debug: bool = False) -> None:
    """Refresh the git index to ensure accurate status.

    Args:
        git_dir: Path to .git directory
        work_tree: Path to working tree
        debug: Enable debug output

    Raises:
        GitError: If refresh fails
    """
    if not os.path.isdir(git_dir) or not os.path.isdir(work_tree):
        raise GitError(f"Invalid git directory or work tree: {git_dir}, {work_tree}")

    # Run the refresh command - we don't need to check the result as it's just a refresh
    run_git_command(git_dir, work_tree, "update-index", "-q", "--refresh", debug=debug)


def get_current_branch(git_dir: str, debug: bool = False) -> str:
    """Get the currently checked out branch.

    Args:
        git_dir: Path to .git directory
        debug: Enable debug output

    Returns:
        Branch name or empty string if not on a branch
    """
    return run_git_command(git_dir, None, "rev-parse", "--abbrev-ref", "HEAD", debug=debug)


def get_stash_count(git_dir: str, work_tree: str, debug: bool = False) -> int:
    """Get the number of stashes in the repository.

    Args:
        git_dir: Path to .git directory
        work_tree: Path to working tree
        debug: Enable debug output

    Returns:
        Number of stashes
    """
    old_cwd = os.getcwd()
    try:
        os.chdir(work_tree)
        stashes = run_git_command(git_dir, None, "stash", "list", debug=debug)
        return len(stashes.splitlines()) if stashes else 0
    finally:
        os.chdir(old_cwd)


def fetch_repo(git_dir: str, work_tree: str, debug: bool = False) -> None:
    """Fetch updates from remote repository.

    Args:
        git_dir: Path to .git directory
        work_tree: Path to working tree
        debug: Enable debug output

    Raises:
        GitError: If fetch fails
    """
    run_git_command(git_dir, work_tree, "fetch", "-q", debug=debug)
