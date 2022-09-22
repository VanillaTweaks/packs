from collections.abc import Callable
from typing import TypeVar

Unknown = object

Function = Callable[..., Unknown]
FunctionType = TypeVar("FunctionType", bound=Function)
