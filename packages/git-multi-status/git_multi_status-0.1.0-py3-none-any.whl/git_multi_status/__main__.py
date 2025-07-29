# MIT license

import os
import time

import typer
from typing_extensions import Annotated

from . import __version__
from .config import Config
from .display import StatusDisplay
from .repo_finder import find_git_repositories
from .status_checker import StatusChecker

app = typer.Typer(
    help="git-multi-status shows uncommitted, untracked and unpushed changes in multiple Git repositories."
)


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        print(__version__)
        raise typer.Exit()


@app.command()
def main(
    dir: Annotated[str, typer.Argument(..., help="Dir to scan")] = ".",
    warn_not_repo: Annotated[bool, typer.Option("-w", help="Warn about dirs that are not Git repositories")] = False,
    exclude_ok: Annotated[bool, typer.Option("-e", "--no-ok", help="Exclude repos that are 'ok'")] = False,
    do_fetch: Annotated[bool, typer.Option("-f", help="Do a 'git fetch' on each repo (slow for many repos)")] = False,
    throttle: Annotated[
        int, typer.Option("--throttle", help="Wait SEC seconds between each 'git fetch' (-f option)")
    ] = 0,
    depth: Annotated[
        int, typer.Option("-d", "--depth", help="Scan depth: 0=no recursion, -1=unlimited, >0=max depth")
    ] = 2,
    flatten: Annotated[bool, typer.Option("--flatten", help="Show only one status per line")] = False,
    show_branch: Annotated[bool, typer.Option("-b", help="Show currently checked out branch")] = False,
    no_push: Annotated[bool, typer.Option("--no-push", help="Limit output: hide push status")] = False,
    no_pull: Annotated[bool, typer.Option("--no-pull", help="Limit output: hide pull status")] = False,
    no_upstream: Annotated[bool, typer.Option("--no-upstream", help="Limit output: hide upstream status")] = False,
    no_uncommitted: Annotated[
        bool, typer.Option("--no-uncommitted", help="Limit output: hide uncommitted changes")
    ] = False,
    no_untracked: Annotated[bool, typer.Option("--no-untracked", help="Limit output: hide untracked files")] = False,
    no_stashes: Annotated[bool, typer.Option("--no-stashes", help="Limit output: hide stashes")] = False,
    _: Annotated[bool, typer.Option("-v", "--version", callback=version_callback, is_eager=True)] = None,
    debug: Annotated[bool, typer.Option("--debug", help="Enable debug output")] = False,
) -> None:
    """
    git-multi-status shows uncommitted, untracked and unpushed changes in multiple Git repositories.
    """
    # Create configuration
    config = Config(
        directory=os.path.abspath(dir),
        exclude_ok=exclude_ok,
        do_fetch=do_fetch,
        throttle=throttle,
        depth=depth,
        flatten=flatten,
        show_branch=show_branch,
        no_push=no_push,
        no_pull=no_pull,
        no_upstream=no_upstream,
        no_uncommitted=no_uncommitted,
        no_untracked=no_untracked,
        no_stashes=no_stashes,
        warn_not_repo=warn_not_repo,
        debug=debug,
    )

    # Initialize components
    status_checker = StatusChecker(debug=debug)
    display = StatusDisplay(config)

    # Find repositories
    repos = list(find_git_repositories(config.directory, config.depth, config.warn_not_repo))

    all_repos_ok = True

    # Process each repository
    for repo_path in repos:
        # Fetch if requested
        if config.do_fetch:
            status_checker.fetch_repository(repo_path)
            if config.throttle > 0:
                time.sleep(config.throttle)

        # Check repository status
        status = status_checker.check_repository(repo_path)
        if status:
            display.display_status(status)
            all_repos_ok = all_repos_ok and status.is_ok

    # Exit with appropriate code
    raise typer.Exit(code=0 if all_repos_ok else 1)


if __name__ == "__main__":
    app()
