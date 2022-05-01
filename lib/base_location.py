import re
from dataclasses import dataclass

from lib.version import Version

PRIVATE_PATH = "zz/do_not_run_or_packs_may_break"

VALID_RESOURCE_NAME = re.compile(r"^[a-z0-9_.-]+$")
CONVENTIONAL_RESOURCE_NAME = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


@dataclass
class BaseLocation:
    """
    A representation of a base for Minecraft resource locations (namespaced IDs).

    Examples:

    ```
    namespace = BaseLocation("namespace")
    something_else = BaseLocation("something:else")
    path = BaseLocation(namespace / "path")
    another_path = BaseLocation(namespace / "another/path")
    subpath = BaseLocation(path / "subpath")

    namespace / "resource" == "namespace:resource"
    path / "resource" == "namespace:path/resource"
    subpath / "resource" == "namespace:path/subpath/resource"
    another_path / "another_resource" == "namespace:another/path/another_resource"
    something_else / "directory/resource" == "something:else/directory/resource"

    namespace / "_resource" == f"namespace:{PRIVATE_PATH}/resource"
    namespace / "path/_resource" == f"namespace:{PRIVATE_PATH}/path/resource"
    path / "_resource" == f"namespace:{PRIVATE_PATH}/path/resource"

    namespace.thing_1 == "namespace.thing_1"
    path.thing_2 == "namespace.path.thing_2"

    external_api = BaseLocation("external_pack:api", external=true)

    external_api / "_test" == "external_pack:api/_test"

    str(BaseLocation(base)) == base
    ```
    """

    _namespace: str
    _path: str
    _title: str | None
    _version: Version | None
    _external: bool

    __path_segments: list[str]

    def __check_name(self, name: str):
        if not VALID_RESOURCE_NAME.match(name):
            raise ValueError(f"The following name is invalid: {repr(name)}")

        if not (CONVENTIONAL_RESOURCE_NAME.match(name) or self._external):
            raise ValueError(f"The following name is unconventional: {repr(name)}")

    def __init__(
        self,
        base: str,
        /,
        version: Version | str | None = None,
        *,
        title: str | None = None,
        external: bool = False,
    ):
        self._namespace, _, self._path = base.partition(":")
        self.__path_segments = self._path.split("/")
        self._version = Version(version) if isinstance(version, str) else version
        self._title = title
        self._external = external

        self.__check_name(self._namespace)
        for path_segment in self.__path_segments:
            self.__check_name(path_segment)

    def __truediv__(self, other: str):
        other_segments = other.split("/")

        output_segments = self.__path_segments[:]

        if not self._external:
            if other_segments[-1].startswith("_"):
                other_segments[-1] = other_segments[-1][1:]
                output_segments.insert(0, PRIVATE_PATH)

            for other_segment in other_segments:
                self.__check_name(other_segment)

        output_segments.extend(other_segments)

        return f"{self._namespace}:{'/'.join(output_segments)}"

    def __getattr__(self, key: str):
        if not CONVENTIONAL_RESOURCE_NAME.match(key):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{key}'"
            )

        return ".".join([self._namespace, *self.__path_segments, key])

    def __str__(self):
        return f"{self._namespace}:{self._path}" if self._path else self._namespace

    def __repr__(self):
        return str(self)
