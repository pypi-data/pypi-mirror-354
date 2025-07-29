"""Display utilities for git-multi-status."""

from rich.console import Console
from rich.text import Text

from .config import Config, RepoStatus

console = Console()


class StatusDisplay:
    """Handle display of repository status information."""

    def __init__(self, config: Config):
        """Initialize display handler.

        Args:
            config: Application configuration
        """
        self.config = config

    def display_status(self, status: RepoStatus) -> None:
        """Display status for a repository.

        Args:
            status: Repository status to display
        """
        # Handle special cases first
        if status.is_unsafe:
            self._print_status(status.path, "", "Unsafe ownership, owned by someone else. Skipping.", "purple bold")
            return

        if status.is_locked:
            self._print_status(status.path, "", "Locked. Skipping.", "red bold")
            return

        if status.is_ignored:
            return

        # Skip OK repos if requested
        if status.is_ok and self.config.exclude_ok:
            return

        # Get branch display
        branch_display = ""
        if self.config.show_branch and status.current_branch:
            branch_display = f" ({status.current_branch})"

        # Build status messages
        status_parts = self._build_status_parts(status)

        if self.config.flatten:
            # Display each status on its own line
            for status_text, style in status_parts:
                self._print_status(status.path, branch_display, status_text, style)
        # Display all statuses on one line
        elif status_parts:
            self._print_combined_status(status.path, branch_display, status_parts)

    def _build_status_parts(self, status: RepoStatus) -> list[tuple[str, str]]:
        """Build list of status parts to display.

        Args:
            status: Repository status

        Returns:
            List of (status_text, style) tuples
        """
        parts = []

        # Push status
        if status.needs_push_branches and not self.config.no_push:
            branches = ",".join(status.needs_push_branches)
            parts.append((f"Needs push ({branches})", "yellow bold"))

        # Pull status
        if status.needs_pull_branches and not self.config.no_pull:
            branches = ",".join(status.needs_pull_branches)
            parts.append((f"Needs pull ({branches})", "blue bold"))

        # Upstream status
        if status.needs_upstream_branches and not self.config.no_upstream:
            branches = ",".join(status.needs_upstream_branches)
            parts.append((f"Needs upstream ({branches})", "purple bold"))

        # Uncommitted changes
        if status.has_uncommitted and not self.config.no_uncommitted:
            parts.append(("Uncommitted changes", "red bold"))

        # Untracked files
        if status.has_untracked and not self.config.no_untracked:
            parts.append(("Untracked files", "cyan bold"))

        # Stashes
        if status.stash_count > 0 and not self.config.no_stashes:
            parts.append((f"{status.stash_count} stashes", "yellow bold"))

        # OK status
        if not parts:  # No issues found
            parts.append(("ok", "green bold"))

        return parts

    def _print_status(self, path: str, branch: str, status_text: str, style: str) -> None:
        """Print a single status line.

        Args:
            path: Repository path
            branch: Branch display text
            status_text: Status message
            style: Rich style for the status
        """
        text = Text()
        text.append(f"{path}{branch}: ")
        text.append(status_text, style=style)
        console.print(text)

    def _print_combined_status(self, path: str, branch: str, status_parts: list[tuple[str, str]]) -> None:
        """Print combined status on one line.

        Args:
            path: Repository path
            branch: Branch display text
            status_parts: List of (status_text, style) tuples
        """
        text = Text()
        text.append(f"{path}{branch}: ")

        for i, (status_text, style) in enumerate(status_parts):
            text.append(status_text, style=style)
            if i < len(status_parts) - 1:
                text.append(" ")

        console.print(text)
