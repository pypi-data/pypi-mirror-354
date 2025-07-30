"""Type definitions for RBAC."""

from typing import Awaitable, Callable, List, Union
from fastapi import Request

# Type alias for role getter functions
RoleGetter = Union[
    Callable[[Request], List[str]],
    Callable[[Request], Awaitable[List[str]]]
]

# Type alias for role lists
RoleList = List[str] 