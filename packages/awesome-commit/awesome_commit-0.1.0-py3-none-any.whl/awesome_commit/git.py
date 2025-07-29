import subprocess
import sys
from pathlib import Path

from loguru import logger
from sh import ErrorReturnCode_1, ErrorReturnCode_128, git

git = git.bake("--no-pager")


def is_git_repository() -> bool:
    """Check if the current directory is a git repository."""
    try:
        git("status")
        return True
    except ErrorReturnCode_128:
        return False


def get_git_changes():
    """Get git staged changes."""
    logger.debug("Getting git staged changes")
    return git("diff", "--cached")


def commit_changes(commit_message):
    """Commit changes with the given message."""
    logger.info("Committing changes")
    try:
        # Use _fg=True to push the execution to the foreground to
        # allow the user to see pre-commit output.
        git("commit", "-m", commit_message, _fg=True)
    except ErrorReturnCode_1:
        sys.exit(1)


def get_last_commit_messages(num: int) -> str:
    """Get the last n commit messages."""
    logger.debug(f"Getting the last {num} commit messages")
    try:
        return git("log", "-n", str(num), "--pretty=full")
    except ErrorReturnCode_128:
        logger.error("Error getting last commit messages")
        return ""


def show_diff():
    """Show the git diff."""
    subprocess.call("git diff --cached", shell=True)


def git_has_staged_changes() -> bool:
    """Check if there are any staged changes in the git repository."""
    try:
        changes = git("diff", "--cached", "--exit-code")
        return bool(changes.strip())
    except ErrorReturnCode_1:
        # If there are staged changes, git will return a non-zero exit code
        return True
    except ErrorReturnCode_128 as e:
        logger.error("Error checking for staged changes")
        raise RuntimeError(
            "Unable to check for staged changes. Are you in a git repository?"
        ) from e


def get_git_project_root() -> Path:
    """Get the root directory ofPath the git project."""
    try:
        return Path(git("rev-parse", "--show-toplevel").strip())
    except ErrorReturnCode_128 as e:
        logger.error("Error getting git project root")
        raise RuntimeError(
            "Unable to locate git project root. Are you in a git repository?"
        ) from e
