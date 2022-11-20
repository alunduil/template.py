"""Project Name.

Convenience type for converting names to safe forms for different uses (e.g.,
project names).
"""

import dataclasses
import re


@dataclasses.dataclass
class ProjectName:
    """Project Name Type.

    Constructed with any arbitrary string and provides convenience properties
    for safe forms for other uses (e.g., package names).
    """

    original: str
    package: str

    def __init__(self, name: str):
        """Construct a ProjectName."""
        self.original = name
        self.package = _package_name(name)


def _package_name(name: str) -> str:
    intercalated = []
    for character in name:
        if character.isupper():
            intercalated.append("_")
        intercalated.append(character)

    underscored = re.sub(r"\W+", "_", "".join(intercalated))
    return re.sub(r"__+", "_", underscored).lower()
