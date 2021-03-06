import re
from dataclasses import InitVar, dataclass, field

VERSION_PATTERN = re.compile(r"^(\d+).(\d+).(\d+)$")


@dataclass(order=True)
class Version:
    """Model for semantic versioning."""

    version_string: InitVar[str]

    major: int = field(init=False)
    minor: int = field(init=False)
    patch: int = field(init=False)

    def __init__(self, version_string: str):
        version_match = VERSION_PATTERN.match(version_string)

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
        return f'Version("{str(self)}")'

    def __iter__(self):
        yield "major", self.major
        yield "minor", self.minor
        yield "patch", self.patch
