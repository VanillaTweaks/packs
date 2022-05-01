import re
from dataclasses import dataclass

version_pattern = re.compile(r"^(\d+).(\d+).(\d+)$")


@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int

    def __init__(self, version_string: str):
        version_match = version_pattern.match(version_string)

        if not version_match:
            raise ValueError(
                f"The following version is invalid: {repr(version_string)}"
            )

        self.major, self.minor, self.patch = (
            int(value) for value in version_match.groups()
        )

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield "major", self.major
        yield "minor", self.minor
        yield "patch", self.patch
