"""Fixtures for pytest."""
import logging
import pathlib
import shutil

import pytest

import template_py.git as _git

_LOGGER = logging.getLogger(__name__)


@pytest.fixture  # type: ignore[misc]
def project_path(tmp_path: pathlib.Path) -> pathlib.Path:
    """Fixture for pytest providing a populated project directory copy."""
    result = tmp_path / "template.py"
    shutil.copytree(_git.project_root(), result)
    return result
