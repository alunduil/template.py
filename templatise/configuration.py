"""File Action Configuration."""

import dataclasses
import pathlib
import typing

import toml

import templatise.project_name as _project_name


@dataclasses.dataclass
class Configuration:
    """File Action Configuration.

    .. note::
       This is implemented as two pieces to more easily handle re-use and the
       termination of recursion.
    """

    project_path: pathlib.Path
    project_name: _project_name.ProjectName
    author: str
    email: str
    licence: str
    template: typing.Optional["Configuration"] = dataclasses.field(init=False)

    def __init__(  # pylint: disable=R0913
        self,
        project_path: pathlib.Path,
        project_name: _project_name.ProjectName,
        author: str,
        email: str,
        licence: str,
    ):
        """Construct a Configuration."""
        self.project_path = project_path
        self.project_name = project_name
        self.author = author
        self.email = email
        self.licence = licence

        # Create the template.
        project_name = _project_name.ProjectName("template.py", "templatise")

        if self.project_name == project_name:
            # Short-circuit the recursion by ensuring we only have one level of
            # template.
            return

        project_path = self.project_path

        with (project_path / "pyproject.toml").open(
            encoding="utf-8"
        ) as pyproject_toml_fh:
            pyproject = toml.load(pyproject_toml_fh)

        assert project_name.package == pyproject["tool"]["poetry"]["name"]  # nosec

        author, email = pyproject["tool"]["poetry"]["authors"][0].split(" <")

        self.template = Configuration(
            project_path=self.project_path,
            project_name=project_name,
            author=author,
            email=email.strip(">"),
            licence=pyproject["tool"]["poetry"]["license"],
        )

    def sub(self, text: str) -> str:
        """Substitute template parameters in given string."""
        if self.template is None:
            raise NotImplementedError(
                "sub is only available on Configurations with an internal template."
            )
        result = text
        result = result.replace(
            self.template.project_name.original, self.project_name.original
        )
        result = result.replace(
            self.template.project_name.package, self.project_name.package
        )
        result = result.replace(self.template.author, self.author)
        result = result.replace(self.template.email, self.email)
        result = result.replace(self.template.licence, self.licence)
        return result
