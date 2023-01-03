"""File Change Actions."""

import logging
import pathlib
import shutil
import tempfile

import toml
import toml_sort

import templatise.configuration as _configuration
import templatise.licence as _licence

_LOGGER = logging.getLogger(__name__)


def convert_pyproject_toml(
    configuration: _configuration.Configuration, path: pathlib.Path
) -> None:
    """Convert pyproject.toml according to the configuration."""
    if path.name != "pyproject.toml":
        raise ValueError(
            f"convert_pyproject_toml is only for pyproject.toml files, not {path}; use convert_file instead."
        )

    pyproject_toml = toml.load(path)
    pyproject_toml["tool"]["poetry"]["name"] = configuration.sub(
        pyproject_toml["tool"]["poetry"]["name"]
    )
    pyproject_toml["tool"]["poetry"]["version"] = "0.1.0"
    pyproject_toml["tool"]["poetry"]["description"] = ""
    pyproject_toml["tool"]["poetry"]["authors"] = [
        configuration.sub(author)
        for author in pyproject_toml["tool"]["poetry"]["authors"]
    ]
    pyproject_toml["tool"]["poetry"]["repository"] = configuration.sub(
        pyproject_toml["tool"]["poetry"]["repository"]
    )
    pyproject_toml["tool"]["poetry"]["keywords"] = []
    pyproject_toml["tool"]["poetry"]["classifiers"] = [
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
    del pyproject_toml["tool"]["poetry"]["scripts"]
    pyproject_toml["tool"]["pytest"]["ini_options"]["addopts"] = configuration.sub(
        pyproject_toml["tool"]["pytest"]["ini_options"]["addopts"]
    )
    pyproject_toml["tool"]["pytest"]["ini_options"]["testpaths"] = [
        configuration.sub(path)
        for path in pyproject_toml["tool"]["pytest"]["ini_options"]["testpaths"]
    ]
    pyproject_toml["tool"]["vulture"]["paths"] = [
        configuration.sub(path) for path in pyproject_toml["tool"]["vulture"]["paths"]
    ]

    pretty = toml_sort.TomlSort(
        toml.dumps(pyproject_toml),
        sort_config=toml_sort.tomlsort.SortConfiguration(inline_arrays=True),
    ).sorted()
    pretty = "\n".join(line.rstrip() for line in pretty.splitlines()).rstrip() + "\n"

    with tempfile.NamedTemporaryFile("w") as result:
        result.write(pretty)
        result.flush()
        shutil.copy(result.name, path)


def convert_file(
    configuration: _configuration.Configuration, path: pathlib.Path
) -> None:
    """Convert file according to the configuration."""
    if path.name == "pyproject.toml":
        raise ValueError(
            f"convert_file should not be used on {path}; use convert_pyproject_toml instead."
        )

    with tempfile.NamedTemporaryFile("w") as result:
        result.write(configuration.sub(path.read_text()))
        result.flush()
        shutil.copy(result.name, path)


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
