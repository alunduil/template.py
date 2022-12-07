"""Test Initialise Command."""
import logging
import pathlib

import click.testing

import templatise.initialise as sut

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

        result = runner.invoke(
            cli=sut.main,
            args=["--project-name", "sentinel", "--path", str(project_path)],
        )

        assert result.exit_code == 0  # nosec
