"""File Change Actions."""

import logging
import pathlib
import shutil
import tempfile

import toml

import templatise.configuration as _configuration
import templatise.licence as _licence

_LOGGER = logging.getLogger(__name__)


def convert_file(
    configuration: _configuration.Configuration, path: pathlib.Path
) -> None:
    """Convert file according to the configuration."""
    with tempfile.NamedTemporaryFile("w") as result:
        result.write(configuration.sub(path.read_text()))
        result.flush()
        if path.name == "pyproject.toml":
            _tweak_pyproject_toml(result)
        shutil.copy(result.name, path)


def _tweak_pyproject_toml(handle: "tempfile._TemporaryFileWrapper[str]") -> None:
    """Tweak elements of the pyproject.toml file."""
    pyproject = toml.load(handle)
    pyproject["tool"]["poetry"]["classifiers"] = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
    ]
    toml.dump(pyproject, handle)


def convert_module(
    configuration: _configuration.Configuration, path: pathlib.Path
) -> None:
    """Convert modules according to the configuration."""
    result = path.parent / configuration.sub(path.name) / "__init__.py"
    result.parent.mkdir(parents=True)
    result.touch()
    shutil.rmtree(path)


def convert_licence(
    configuration: _configuration.Configuration, path: pathlib.Path
) -> None:
    """Convert licence according to the configuration."""
    if (
        configuration.template is not None
        and configuration.licence != configuration.template.licence
    ):
        path.write_text(_licence.text(configuration.licence))
