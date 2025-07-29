"""Git repository status checker for git-multi-status."""

import os
from typing import Optional

from .config import RepoStatus
from .git_utils import (
    GitError,
    check_repo_ownership,
    fetch_repo,
    get_current_branch,
    get_repo_config_bool,
    get_stash_count,
    is_repo_locked,
    refresh_git_index,
    run_git_command,
)


class StatusChecker:
    """Check the status of git repositories."""

    def __init__(self, debug: bool = False):
        """Initialize status checker.

        Args:
            debug: Enable debug output
        """
        self.debug = debug

    def check_repository(self, repo_path: str) -> Optional[RepoStatus]:
        """Check the status of a git repository.

        Args:
            repo_path: Path to the repository

        Returns:
            RepoStatus object or None if repo should be skipped
        """
        git_dir = os.path.join(repo_path, ".git")

        # Initialize status object
        status = RepoStatus(path=repo_path)

        # Check repository safety and basic conditions
        if not self._check_repo_safety(git_dir, status):
            return status

        # Check if repo should be ignored
        if get_repo_config_bool(git_dir, "mgitstatus.ignore"):
            status.is_ignored = True
            return status

        # Check if repo is locked
        if is_repo_locked(git_dir):
            status.is_locked = True
            return status

        try:
            # Refresh index for accurate results
            refresh_git_index(git_dir, repo_path, self.debug)
        except GitError:
            # Continue even if refresh fails
            pass

        # Get repository status
        self._get_branch_status(git_dir, status)
        self._get_working_tree_status(git_dir, repo_path, status)
        self._get_stash_status(git_dir, repo_path, status)

        return status

    def fetch_repository(self, repo_path: str) -> bool:
        """Fetch updates for a repository.

        Args:
            repo_path: Path to the repository

        Returns:
            True if fetch succeeded, False otherwise
        """
        git_dir = os.path.join(repo_path, ".git")
        try:
            fetch_repo(git_dir, repo_path, self.debug)
            return True
        except GitError:
            return False

    def _check_repo_safety(self, git_dir: str, status: RepoStatus) -> bool:
        """Check if repository is safe to access.

        Args:
            git_dir: Path to .git directory
            status: Status object to update

        Returns:
            True if repo is safe to access
        """
        if not os.path.isdir(git_dir):
            # Mark as unsafe so is_ok returns False for nonexistent repos
            status.is_unsafe = True
            return False

        if not check_repo_ownership(git_dir):
            status.is_unsafe = True
            return False

        return True

    def _get_branch_status(self, git_dir: str, status: RepoStatus) -> None:
        """Get branch-related status information.

        Args:
            git_dir: Path to .git directory
            status: Status object to update
        """
        try:
            # Get current branch
            status.current_branch = get_current_branch(git_dir, self.debug)

            # Find all local branches
            refs_dir = os.path.join(git_dir, "refs", "heads")
            branch_refs = self._get_branch_refs(refs_dir)

            # Check each branch for upstream status
            for branch in branch_refs:
                self._check_branch_upstream_status(git_dir, branch, status)

        except GitError:
            # Continue if branch status check fails
            pass

    def _get_branch_refs(self, refs_dir: str) -> list[str]:
        """Get all branch references.

        Args:
            refs_dir: Path to refs/heads directory

        Returns:
            List of branch names
        """
        branch_refs = []

        if not os.path.isdir(refs_dir):
            return branch_refs

        for root, _, files in os.walk(refs_dir):
            for file in files:
                ref_path = os.path.join(root, file)
                if os.path.isfile(ref_path):
                    rel_path = os.path.relpath(ref_path, refs_dir)
                    branch_refs.append(rel_path)

        return branch_refs

    def _check_branch_upstream_status(self, git_dir: str, branch: str, status: RepoStatus) -> None:
        """Check upstream status for a branch.

        Args:
            git_dir: Path to .git directory
            branch: Branch name
            status: Status object to update
        """
        try:
            # Get upstream branch
            upstream = run_git_command(
                git_dir, None, "rev-parse", "--abbrev-ref", "--symbolic-full-name", f"{branch}@{{u}}", debug=self.debug
            )

            if upstream:
                self._check_branch_sync_status(git_dir, branch, upstream, status)
            else:
                # Branch has no upstream - only add if it's not the main branch
                # or if there are remotes configured
                remotes_output = run_git_command(git_dir, None, "remote", debug=self.debug)
                if remotes_output and branch not in status.needs_upstream_branches:
                    status.needs_upstream_branches.append(branch)

        except GitError:
            # If we can't get upstream, only assume it needs one if there are remotes
            try:
                remotes_output = run_git_command(git_dir, None, "remote", debug=self.debug)
                if remotes_output and branch not in status.needs_upstream_branches:
                    status.needs_upstream_branches.append(branch)
            except GitError:
                pass

    def _check_branch_sync_status(self, git_dir: str, branch: str, upstream: str, status: RepoStatus) -> None:
        """Check if branch is in sync with upstream.

        Args:
            git_dir: Path to .git directory
            branch: Local branch name
            upstream: Upstream branch name
            status: Status object to update
        """
        try:
            # Get ahead/behind count
            count_result = run_git_command(
                git_dir, None, "rev-list", "--left-right", "--count", f"{branch}...{upstream}", debug=self.debug
            )

            if count_result:
                ahead_str, behind_str = count_result.split()
                ahead = int(ahead_str)
                behind = int(behind_str)

                if ahead > 0 and branch not in status.needs_push_branches:
                    status.needs_push_branches.append(branch)
                if behind > 0 and branch not in status.needs_pull_branches:
                    status.needs_pull_branches.append(branch)

        except (GitError, ValueError):
            # If we can't determine sync status, be conservative
            pass

    def _get_working_tree_status(self, git_dir: str, repo_path: str, status: RepoStatus) -> None:
        """Get working tree status information.

        Args:
            git_dir: Path to .git directory
            repo_path: Path to repository
            status: Status object to update
        """
        try:
            # Check for unstaged changes
            unstaged = run_git_command(git_dir, repo_path, "diff-index", "HEAD", "--", debug=self.debug)

            # Check for uncommitted changes
            uncommitted = run_git_command(
                git_dir, repo_path, "diff-files", "--ignore-submodules", "--", debug=self.debug
            )

            status.has_uncommitted = bool(unstaged or uncommitted)

            # Check for untracked files
            untracked = run_git_command(
                git_dir, repo_path, "ls-files", "--exclude-standard", "--others", debug=self.debug
            )

            status.has_untracked = bool(untracked.strip())

        except GitError:
            # Conservative approach: assume there might be changes
            pass

    def _get_stash_status(self, git_dir: str, repo_path: str, status: RepoStatus) -> None:
        """Get stash status information.

        Args:
            git_dir: Path to .git directory
            repo_path: Path to repository
            status: Status object to update
        """
        try:
            status.stash_count = get_stash_count(git_dir, repo_path, self.debug)
        except GitError:
            status.stash_count = 0
