"""Tests for Configuration."""

import pathlib

import templatise.configuration as sut
import templatise.project_name as _project_name


class TestConfigurationPostInit:  # pylint: disable=R0903
    """Test Post Initialisation of Configuration."""

    def test_construction(self, project_path: pathlib.Path) -> None:
        """Test basic construction of a configuration."""
        project_name = _project_name.ProjectName("sentinel")
        result = sut.Configuration(
            project_path=project_path,
            project_name=project_name,
            author="unknown",
            email="unroutable",
            licence="unlicense",
        )
        assert result.project_path == project_path  # nosec
        assert result.project_name == project_name  # nosec
        assert result.author == "unknown"  # nosec
        assert result.email == "unroutable"  # nosec
        assert result.licence == "unlicense"  # nosec
        assert result._template is not None  # nosec pylint: disable=W0212
        assert (  # nosec
            result.project_path
            == result._template.project_path  # pylint: disable=W0212
        )
        assert (  # nosec
            result.project_name
            != result._template.project_name  # pylint: disable=W0212
        )
        assert result.author != result._template.author  # nosec pylint: disable=W0212
        assert result.email != result._template.email  # nosec pylint: disable=W0212
