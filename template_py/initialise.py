"""Main module for initialise."""
import concurrent.futures
import datetime
import logging
import pathlib
import typing

import click
import click_log

import template_py.actions as _actions
import template_py.configuration as _configuration
import template_py.git as _git
import template_py.project_name as _project_name

_LOGGER = logging.getLogger(__name__)
click_log.basic_config(_LOGGER)


@click.command()  # type: ignore[misc]
@click_log.simple_verbosity_option(_LOGGER)  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "-n",
    "--project-name",
    type=_project_name.ProjectName,
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
    prompt=True,
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
@click.option(  # type: ignore[misc]
    "--timeout",
    type=click.FloatRange(min=0.0),
    required=True,
    default=datetime.timedelta(minutes=10).total_seconds(),
    show_default=True,
    help="Timeout in seconds for project initialisation activities.  Does not include any time waiting for prompts.",
)
def main(  # pylint: disable=R0913
    project_name: _project_name.ProjectName,
    author: str,
    email: str,
    licence: str,
    path: pathlib.Path,
    timeout: float,
) -> None:
    """Initialise a new project using the current checked out repository.

    .. warning::
       THIS WILL DESTROY THE CURRENT CONTENTS OF YOUR CHECKED OUT REPOSITORY!
    """
    configuration = _configuration.Configuration(
        project_path=path,
        project_name=project_name,
        author=author,
        email=email,
        licence=licence,
    )

    files = [
        path / ".devcontainer" / "devcontainer.json",
        path / ".gihub" / "workflows" / "poetry.yml",
        path / "pyproject.toml",
    ]
    modules = [
        path / configuration.project_name.package,
        path / f"{configuration.project_name.package}_test",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures: typing.List[
            concurrent.futures.Future[None]  # pylint: disable=E1136
        ] = []
        futures.extend(
            executor.submit(_actions.convert_file, configuration, file)
            for file in files
        )
        futures.extend(
            executor.submit(_actions.convert_module, configuration, module)
            for module in modules
        )
        futures.append(
            executor.submit(_actions.convert_licence, configuration, path / "LICENSE")
        )
        concurrent.futures.wait(
            futures, timeout=timeout, return_when=concurrent.futures.FIRST_EXCEPTION
        )
