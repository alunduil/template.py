"""Test Initialise Command."""

import logging
import pathlib
import subprocess  # nosec
import typing
import unittest.mock

import click.testing
import requests

import templatise.initialise as sut
import templatise.licence

_LOGGER = logging.getLogger(__name__)


class TestMain:
    """Test Main Command."""

    def test_help(self) -> None:
        """Test --help."""
        runner = click.testing.CliRunner()
        result = runner.invoke(cli=sut.main, args=["--help"])
        assert result.exit_code == 0  # nosec

    def test_mock_initialisation(self, project_path: pathlib.Path) -> None:
        """Test the whole process with a copy of the working tree."""
        runner = click.testing.CliRunner()

        # Mock the license download to avoid network calls
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"licenseText": "Mock license text for testing"}'

        with unittest.mock.patch.object(
            templatise.licence.requests, "get", return_value=mock_response
        ):
            result = runner.invoke(
                cli=sut.main,
                args=[
                    "--project-name",
                    "sentinel",
                    "--path",
                    str(project_path),
                    "--verbosity",
                    "DEBUG",
                ],
            )

        _LOGGER.debug("result.output:\n%s", result.output)
        _LOGGER.debug("result.exception: %s", result.exception)
        _LOGGER.debug("result.exc_info: %s", result.exc_info)

        assert result.exit_code == 0  # nosec

        assert not (project_path / "templatise").exists()  # nosec
        assert not (project_path / "templatise_test").exists()  # nosec

        assert (project_path / "sentinel").exists()  # nosec
        assert (project_path / "sentinel_test").exists()  # nosec

        grep = _grep(
            patterns=["template.py", "template_py"],
            paths=[project_path],
            options=["--invert-match", "--recursive", "--quiet"],
        )
        assert grep.returncode == 0  # nosec


def _grep(
    patterns: typing.List[str],
    paths: typing.List[pathlib.Path],
    options: typing.Optional[typing.List[str]] = None,
):  # type: (...) -> subprocess.CompletedProcess[str]
    if not options:
        options = []

    result = subprocess.run(  # pylint: disable=W1510 # nosec
        ["grep", *options, *[f"-e {pattern}" for pattern in patterns], *paths],
        capture_output=True,
        text=True,
    )

    return result
