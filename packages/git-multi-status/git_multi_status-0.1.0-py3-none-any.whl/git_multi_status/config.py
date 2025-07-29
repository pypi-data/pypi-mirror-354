"""Configuration models for git-multi-status."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration for git-multi-status operations."""

    # Display options
    exclude_ok: bool = False
    flatten: bool = False
    show_branch: bool = False
    warn_not_repo: bool = False

    # Filter options
    no_push: bool = False
    no_pull: bool = False
    no_upstream: bool = False
    no_uncommitted: bool = False
    no_untracked: bool = False
    no_stashes: bool = False

    # Fetch options
    do_fetch: bool = False
    throttle: int = 0

    # Search options
    depth: int = 2

    # Debug
    debug: bool = False

    # Directory to scan
    directory: str = "."


@dataclass
class RepoStatus:
    """Status information for a git repository."""

    path: str
    current_branch: Optional[str] = None
    needs_push_branches: list[str] = None
    needs_pull_branches: list[str] = None
    needs_upstream_branches: list[str] = None
    has_uncommitted: bool = False
    has_untracked: bool = False
    stash_count: int = 0
    is_locked: bool = False
    is_ignored: bool = False
    is_unsafe: bool = False

    def __post_init__(self):
        """Initialize mutable default values."""
        if self.needs_push_branches is None:
            self.needs_push_branches = []
        if self.needs_pull_branches is None:
            self.needs_pull_branches = []
        if self.needs_upstream_branches is None:
            self.needs_upstream_branches = []

    @property
    def is_ok(self) -> bool:
        """Check if repository is in a clean state."""
        return (
            not self.needs_push_branches
            and not self.needs_pull_branches
            and not self.needs_upstream_branches
            and not self.has_uncommitted
            and not self.has_untracked
            and self.stash_count == 0
            and not self.is_locked
            and not self.is_unsafe
        )
