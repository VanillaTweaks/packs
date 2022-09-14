import re
from dataclasses import dataclass

VERSION_PATTERN = re.compile(r"^(\d+).(\d+).(\d+)$")


@dataclass(frozen=True, order=True)
class Version:
    """Model for semantic versioning."""

    major: int
    minor: int
    patch: int

    def __init__(self, version_string: str):
        version_match = VERSION_PATTERN.match(version_string)

        if not version_match:
            raise ValueError(
                f"The following version is invalid: {repr(version_string)}"
            )

        major, minor, patch = (int(value) for value in version_match.groups())

        object.__setattr__(self, "major", major)
        object.__setattr__(self, "minor", minor)
        object.__setattr__(self, "patch", patch)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self):
        return f'Version("{self}")'

    def __iter__(self):
        yield "major", self.major
        yield "minor", self.minor
        yield "patch", self.patch
