"""
Simple RBAC for FastAPI applications.

Provides decorators and middleware for role-based access control with minimal setup.
"""

from .decorators import require_roles, require_any_role, get_current_user_roles, create_role_dependency
from .exceptions import RBACException, InsufficientRoleError, RoleExtractionError
from .middleware import RBACMiddleware
from .types import RoleGetter

__version__ = "0.1.0"
__author__ = "Farid Darabi"
__email__ = "farid.darabi@gmail.com"

__all__ = [
    "require_roles",
    "require_any_role", 
    "get_current_user_roles",
    "create_role_dependency",
    "RBACMiddleware",
    "RBACException",
    "InsufficientRoleError",
    "RoleExtractionError",
    "RoleGetter",
] 