"""Pre-commit helper functions."""

import sys

from colored import Fore, Style
from sh import ErrorReturnCode_1, pre_commit

from awesome_commit.git import get_git_project_root


def has_pre_commit_config() -> bool:
    """Check if pre-commit is configured in the git project."""
    project_root = get_git_project_root()
    pre_commit_config = project_root / ".pre-commit-config.yaml"
    return pre_commit_config.exists() and pre_commit_config.is_file()


def run_pre_commit():
    """Run pre-commit hooks."""
    if not has_pre_commit_config():
        print(
            f"{Fore.red}No pre-commit configuration found. Skipping pre-commit hooks.{Style.reset}"
        )
        return
    print(f"{Fore.blue}Running pre-commit hooks...{Style.reset}")
    try:
        pre_commit("run", _fg=True)
    except ErrorReturnCode_1:
        print(f"{Fore.red}Pre-commit hooks failed. Exiting.{Style.reset}")
        sys.exit(1)
    print(f"{Fore.blue}Pre-commit hooks passed.{Style.reset}")
