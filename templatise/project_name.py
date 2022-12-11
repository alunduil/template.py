"""Project Name.

Convenience type for converting names to safe forms for different uses (e.g.,
project names).
"""

import dataclasses
import re
import typing


@dataclasses.dataclass
class ProjectName:
    """Project Name Type.

    Constructed with any arbitrary string and provides convenience properties
    for safe forms for other uses (e.g., package names).
    """

    original: str
    package: str

    def __init__(self, name: str, package_name: typing.Optional[str] = None):
        """Construct a ProjectName."""
        self.original = name
        assert isinstance(name, str)  # nosec
        self.package = _package_name(name) if not package_name else package_name


def _package_name(name: str) -> str:
    intercalated = []
    for character in name:
        if character.isupper():
            intercalated.append("_")
        intercalated.append(character)

    underscored = re.sub(r"\W+", "_", "".join(intercalated))
    return re.sub(r"__+", "_", underscored).lower()
