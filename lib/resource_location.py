import re

from lib.version import Version

PRIVATE_PATH = "zz/do_not_run_or_packs_may_break"

VALID_RESOURCE_NAME = re.compile(r"^[a-z0-9_.-]+$")
CONVENTIONAL_RESOURCE_NAME = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


class ResourceLocation:
    """A representation of a Minecraft resource location (namespaced ID) with some extra
    features.

    >>> namespace = ResourceLocation("namespace")
    >>> something_else = ResourceLocation("something:else")
    >>> path = namespace / "path"
    >>> another_path = ResourceLocation("namespace:another/path")
    >>> subpath = path / "subpath"

    >>> str(namespace)
    "namespace"
    >>> str(another_path)
    "namespace:another/path"
    >>> something_else["namespace"]
    "something"
    >>> another_path["path"]
    "another/path"

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

    _namespace: str
    # A tuple of the components of the resource location's actual path.
    _path_components: tuple[str, ...] = ()
    # The resource location's path, possibly with abstractions/shorthands.
    _abstract_path: str | None = None
    # The resource location's actual path.
    _path: str | None = None
    _version: Version | None
    _title: str | None
    _external: bool

    def __init__(
        self,
        base: str,
        /,
        *,
        version: Version | str | None = None,
        title: str | None = None,
        external: bool = False,
    ):
        self._namespace, colon, abstract_path = base.partition(":")
        self._version = Version(version) if isinstance(version, str) else version
        self._title = title
        self._external = external

        self._check_name(self._namespace)

        if colon:
            self._abstract_path = abstract_path

            path_components = abstract_path.split("/")

            if not external:
                # The underscore has to be on the last path component so that whether a
                #  resource location is private must be explicitly set each time rather
                #  than stored in a parent resource location and then forgotten about.
                if path_components[-1].startswith("_"):
                    path_components[-1] = path_components[-1].removeprefix("_")
                    path_components = PRIVATE_PATH.split("/") + path_components

            self._path_components = tuple(path_components)

            for path_component in self._path_components:
                self._check_name(path_component)

            self._path = "/".join(path_components)

    def _check_name(self, name: str):
        if not VALID_RESOURCE_NAME.match(name):
            raise ValueError(f"The following name is invalid: {repr(name)}")

        if not (CONVENTIONAL_RESOURCE_NAME.match(name) or self.external):
            raise ValueError(f"The following name is unconventional: {repr(name)}")

    def _get_ast_json_value_(self):
        return str(self)

    def __truediv__(self, other: object):
        path = f"{self._abstract_path}/{other}" if self._abstract_path else other

        return ResourceLocation(f"{self._namespace}:{path}", external=self._external)

    def __getattr__(self, key: str):
        if not CONVENTIONAL_RESOURCE_NAME.match(key):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{key}'"
            )

        return ".".join([self._namespace, *self._path_components, key])

    def __getitem__(self, key: str):
        return getattr(self, f"_{key}")

    def __str__(self):
        if self._path is None:
            return self._namespace

        return f"{self._namespace}:{self._path}"

    def __eq__(self, other: object):
        return str(self) == str(other)

    def __repr__(self):
        return f"{type(self).__name__}({repr(str(self))})"

    def __hash__(self):
        return hash(str(self))
