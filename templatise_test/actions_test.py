"""Tests for actions."""
import pathlib
import shutil

import pytest
import pytest_golden.plugin

import templatise.actions as sut
import templatise.configuration as _configuration
import templatise.git as _git
import templatise.project_name as _project_name


@pytest.mark.golden_test("actions_test_fixtures/convert_file_*.yaml")  # type: ignore[misc]
def test_golden_convert_file(
    project_path: pathlib.Path,
    golden: pytest_golden.plugin.GoldenTestFixture,
) -> None:
    """Test golden convert_file."""
    golden["configuration"]["project_path"] = project_path
    golden["configuration"]["project_name"] = _project_name.ProjectName(
        golden["configuration"]["project_name"]
    )
    configuration = _configuration.Configuration(
        **golden["configuration"],
    )
    assert isinstance(configuration.project_name, _project_name.ProjectName)  # nosec
    file_path = project_path / "sentinel"
    shutil.copy(_git.project_root() / golden["input_path"], file_path)
    sut.convert_file(configuration, file_path)
    result = file_path.read_text()
    assert result, f"convert_file({golden['input_path']}) is empty."  # nosec
    assert result == golden.out["output"]  # nosec


@pytest.mark.golden_test("actions_test_fixtures/convert_pyproject_toml.yaml")  # type: ignore[misc]
def test_golden_pyproject_toml(
    project_path: pathlib.Path,
    golden: pytest_golden.plugin.GoldenTestFixture,
) -> None:
    """Test golden convert_pyproject_toml."""
    golden["configuration"]["project_path"] = project_path
    golden["configuration"]["project_name"] = _project_name.ProjectName(
        golden["configuration"]["project_name"]
    )
    configuration = _configuration.Configuration(
        **golden["configuration"],
    )
    assert isinstance(configuration.project_name, _project_name.ProjectName)  # nosec
    file_path = project_path / "pyproject.toml"
    shutil.copy(_git.project_root() / golden["input_path"], file_path)
    sut.convert_pyproject_toml(configuration, file_path)
    result = file_path.read_text()
    assert result, f"convert_pyproject_toml({golden['input_path']}) is empty."  # nosec
    assert result == golden.out["output"]  # nosec


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
        sut.convert_module(configuration, project_path / "templatise")
        assert not (project_path / "templatise").exists()  # nosec
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
        sut.convert_module(configuration, project_path / "templatise_test")
        assert not (project_path / "templatise_test").exists()  # nosec
        assert (project_path / "sentinel_test").exists()  # nosec
        assert (project_path / "sentinel_test" / "__init__.py").exists()  # nosec
