"""Main module for initialise."""
import logging
import pathlib

import click
import click_log

import templatise.actions as _actions
import templatise.configuration as _configuration
import templatise.git as _git
import templatise.project_name as _project_name

_LOGGER = logging.getLogger(__name__)
click_log.basic_config(_LOGGER)


@click.command()  # type: ignore[misc]
@click_log.simple_verbosity_option(_LOGGER)  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "-n",
    "--project-name",
    required=True,
    metavar="NAME",
    envvar="PROJECT_NAME",
    show_envvar=True,
    prompt=True,
    help="Name of the new project.",
)
@click.option(  # type: ignore[misc]
    "--author",
    required=True,
    default=lambda: _git.config("user.name"),
    prompt=True,
    show_default="configured git user.name",
    help="Name of the author of the project.",
)
@click.option(  # type: ignore[misc]
    "--email",
    required=True,
    default=lambda: _git.config("user.email"),
    prompt=True,
    show_default="configured git user.email",
    help="Email of the author of the project.",
)
@click.option(  # type: ignore[misc]
    "--licence",
    required=True,
    default=lambda: "unlicense",
    prompt=f"Licence; {click.style('use https://choosealicense.com/ to help choose',italic=True)}",
    show_default="unlicence",
    help="Licence of the project.",
)
@click.option(  # type: ignore[misc]
    "--path",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    required=True,
    default=pathlib.Path.cwd(),
    help="Project path.  Only used for testing.",
    hidden=True,
)
def main(  # pylint: disable=R0913
    project_name: str,
    author: str,
    email: str,
    licence: str,
    path: pathlib.Path,
) -> None:
    """Initialise a new project using the current checked out repository.

    .. warning::
       THIS WILL DESTROY THE CURRENT CONTENTS OF YOUR CHECKED OUT REPOSITORY!
    """
    configuration = _configuration.Configuration(
        project_path=path,
        project_name=_project_name.ProjectName(project_name),
        author=author,
        email=email,
        licence=licence,
    )

    assert configuration.template is not None  # nosec

    _LOGGER.info("convert licence")
    _actions.convert_licence(configuration, path / "LICENSE")

    _LOGGER.info("convert pyproject.toml")
    _actions.convert_pyproject_toml(configuration, path / "pyproject.toml")

    files = [
        path / ".devcontainer" / "devcontainer.json",
        path / ".github" / "workflows" / "poetry.yml",
    ]

    for file in files:
        _LOGGER.info("convert file %s", file)
        _actions.convert_file(configuration, file)

    modules = [
        path / configuration.template.project_name.package,
        path / f"{configuration.template.project_name.package}_test",
    ]

    for module in modules:
        _LOGGER.info("convert module %s", module)
        _actions.convert_module(configuration, module)
