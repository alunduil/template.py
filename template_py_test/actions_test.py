"""Tests for actions."""
import pathlib

import pytest
import pytest_golden.plugin

import template_py.actions as sut
import template_py.configuration as _configuration
import template_py.project_name as _project_name


@pytest.mark.golden_test("actions_test_fixtures/convert_file_*.yaml")  # type: ignore[misc]
def test_golden_convert_file(
    project_path: pathlib.Path,
    golden: pytest_golden.plugin.GoldenTestFixture,
) -> None:
    """Test golden convert_file."""
    configuration = _configuration.Configuration(
        project_path=project_path,
        **golden["configuration"],
    )
    assert isinstance(configuration.project_name, _project_name.ProjectName)  # nosec
    file_path = project_path / "sentinel"
    file_path.write_text(golden["input"])
    sut.convert_file(configuration, file_path)
    assert file_path.read_text() == golden.out["output"]  # nosec


class TestConvertModule:
    """Tests for convert_module."""

    def test_convert_module(self, project_path: pathlib.Path) -> None:
        """Test convert template_py module."""
        configuration = _configuration.Configuration(
            project_path=project_path,
            project_name=_project_name.ProjectName("sentinel"),
            author="unknown",
            email="unroutable",
            licence="unlicense",
        )
        sut.convert_module(configuration, project_path / "template_py")
        assert not (project_path / "template_py").exists()  # nosec
        assert (project_path / "sentinel").exists()  # nosec
        assert (project_path / "sentinel" / "__init__.py").exists()  # nosec

    def test_convert_test_module(self, project_path: pathlib.Path) -> None:
        """Test convert template_py_test module."""
        configuration = _configuration.Configuration(
            project_path=project_path,
            project_name=_project_name.ProjectName("sentinel"),
            author="unknown",
            email="unroutable",
            licence="unlicense",
        )
        sut.convert_module(configuration, project_path / "template_py_test")
        assert not (project_path / "template_py_test").exists()  # nosec
        assert (project_path / "sentinel_test").exists()  # nosec
        assert (project_path / "sentinel_test" / "__init__.py").exists()  # nosec
