"""Git Interactions."""

import os
import pathlib
import shlex
import subprocess  # nosec
import typing


def config(name: str) -> str:
    """Run `git config`."""
    result = subprocess.run(  # nosec pylint: disable=W1510
        _config_command(name),
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _config_command(name: str) -> typing.List[str]:
    if os.name != "posix":
        raise RuntimeError(
            f"Usage is only supported on 'posix' environmnts, not {os.name}"
        )
    return ["git", "config", shlex.quote(name)]


def project_root() -> pathlib.Path:
    """Path to project root as git sees it."""
    result = subprocess.run(  # nosec
        _project_root_command(),
        capture_output=True,
        text=True,
        check=True,
    )
    return pathlib.Path(result.stdout.strip())


def _project_root_command() -> typing.List[str]:
    return ["git", "rev-parse", "--show-toplevel"]
