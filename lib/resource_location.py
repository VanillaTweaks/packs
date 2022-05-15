import re
from functools import cache

from lib.version import Version

PRIVATE_PATH = "zz/do_not_run_or_packs_may_break"

VALID_RESOURCE_NAME = re.compile(r"^[a-z0-9_.-]+$")
CONVENTIONAL_RESOURCE_NAME = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


class ResourceLocation:
    """A representation of a Minecraft resource location (namespaced ID) with some extra features.

    >>> namespace = ResourceLocation("namespace")
    >>> something_else = ResourceLocation("something:else")
    >>> path = namespace / "path"
    >>> another_path = "namespace:another/path"
    >>> subpath = path / "subpath"

    >>> str(namespace)
    "namespace"
    >>> str(another_path)
    "namespace:another/path"

    >>> namespace / "resource"
    "namespace:resource"
    >>> path / "resource"
    "namespace:path/resource"
    >>> subpath / "resource"
    "namespace:path/subpath/resource"
    >>> another_path / "another_resource"
    "namespace:another/path/another_resource"
    >>> something_else / "directory/resource"
    "something:else/directory/resource"

    >>> namespace / "_resource"
    f"namespace:{PRIVATE_PATH}/resource"
    >>> namespace / "path/_resource"
    f"namespace:{PRIVATE_PATH}/path/resource"
    >>> path / "_resource"
    f"namespace:{PRIVATE_PATH}/path/resource"

    >>> namespace.thing_1
    "namespace.thing_1"
    >>> path.thing_2
    "namespace.path.thing_2"

    >>> external_api = ResourceLocation("external_pack:api", external=true)
    >>> external_api / "_test"
    "external_pack:api/_test"
    """

    # TODO: handle versioning for LL (specifically, creating a versioned path. ex: `rx.playerdb:impl/v2.0.1/<internals>`)
    #  also consider how child base locations are created depending on that version (i.e. in __truediv__)

    _version: Version | None
    _title: str | None
    _external: bool
    _namespace: str
    _path: str = ""

    def __init__(
        self,
        base: str,
        /,
        *,
        version: Version | str | None = None,
        title: str | None = None,
        external: bool = False,
    ):
        self.namespace, colon, self.path = base.partition(":")
        self.version = Version(version) if isinstance(version, str) else version
        self.title = title
        self.external = external

        self._check_name(self.namespace)

        if colon:
            for path_segment in self._get_path_segments():
                self._check_name(path_segment)

    def _check_name(self, name: str):
        if not VALID_RESOURCE_NAME.match(name):
            raise ValueError(f"The following name is invalid: {repr(name)}")

        if not (CONVENTIONAL_RESOURCE_NAME.match(name) or self.external):
            raise ValueError(f"The following name is unconventional: {repr(name)}")

    @cache
    def _get_path_segments(self) -> tuple[str, ...]:
        if self.path == "":
            return ()

        path_segments = self.path.split("/")

        if not self.external:
            if path_segments[-1].startswith("_"):
                path_segments[-1] = path_segments[-1].removesuffix("_")
                path_segments.insert(0, PRIVATE_PATH)

        return tuple(path_segments)

    def __truediv__(self, other: str):
        path = f"{self.path}/{other}" if self.path else other

        return ResourceLocation(f"{self.namespace}:{path}", external=self._external)

    def __getattr__(self, key: str):
        if not CONVENTIONAL_RESOURCE_NAME.match(key):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{key}'"
            )

        return ".".join([self.namespace, *self._get_path_segments(), key])

    def __getitem__(self, key: str):
        return getattr(self, f"_{key}")

    def __str__(self):
        if self.path:
            path = "/".join(self._get_path_segments())
            return f"{self.namespace}:{path}"

        return self.namespace

    def __eq__(self, other: object):
        return str(self) == str(other)

    def __repr__(self):
        return f"{type(self).__name__}({self})"

    def __hash__(self):
        return hash(str(self))
