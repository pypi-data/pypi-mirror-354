"""Git Multi Status - Check status of multiple git repositories."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("git-multi-status")
except PackageNotFoundError:
    __version__ = "dev"

__all__ = ["__version__"]
