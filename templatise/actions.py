"""File Change Actions."""

import pathlib
import shutil
import tempfile

import templatise.configuration as _configuration
import templatise.licence as _licence


def convert_file(
    configuration: _configuration.Configuration, path: pathlib.Path
) -> None:
    """Convert file according to the configuration."""
    with tempfile.NamedTemporaryFile("w") as result:
        result.write(configuration.sub(path.read_text()))
        result.flush()
        shutil.copy(result.name, path)


def convert_module(
    configuration: _configuration.Configuration, path: pathlib.Path
) -> None:
    """Convert modules according to the configuration."""
    result = path.parent / configuration.sub(path.name) / "__init__.py"
    result.parent.mkdir()
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
