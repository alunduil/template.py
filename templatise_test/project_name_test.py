"""Tests for Project Name."""

import re

import hypothesis
import hypothesis.strategies

import templatise.project_name as sut


def project_names() -> hypothesis.strategies.SearchStrategy[sut.ProjectName]:
    """Strategy for generating `ProjectName`s."""
    return hypothesis.strategies.builds(
        sut.ProjectName,
        name=hypothesis.strategies.text(
            alphabet=hypothesis.strategies.characters(blacklist_categories=["C"])
        ),
    )


class TestProjectName:
    """Test Project Name Type."""

    def test_template_name(self) -> None:
        """Test our handling of the chosen project name."""
        assert sut.ProjectName("template.py").package == "template_py"  # nosec

    def test_hyphenated_name(self) -> None:
        """Test hyphenated project name."""
        assert sut.ProjectName("foo-bar").package == "foo_bar"  # nosec

    @hypothesis.given(name=project_names())  # type: ignore[misc]
    def test_package(self, name: sut.ProjectName) -> None:
        """Test default constructor."""
        assert re.match(r"[a-z_]*", name.package)  # nosec
        assert not re.search(r"__+", name.package)  # nosec
