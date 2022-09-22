from pydantic import BaseModel, validator

from lib.version import Version


class PackConfig(BaseModel, frozen=True):
    """A representation of the information in `pack.yaml`."""

    title: str
    version: Version
    description: str
    listed: bool

    @validator("version", pre=True)
    def convert_version(cls, value: str):
        return Version(value)
