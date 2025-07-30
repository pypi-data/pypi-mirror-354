"""Role-based access control decorators for FastAPI."""

import functools
import inspect
from typing import Callable, List, Optional, Union
from fastapi import Request

from .exceptions import InsufficientRoleError, RoleExtractionError


def require_roles(
    roles: Union[str, List[str]],
    require_all: bool = True,
    error_message: Optional[str] = None
) -> Callable:
    """Require specific roles to access an endpoint.
    
    Args:
        roles: Role or list of roles required
        require_all: If True, user must have ALL roles. If False, ANY role works.
        error_message: Custom error message for access denied
    
    Example:
        @app.get("/admin")
        @require_roles("admin")
        def admin_only(request: Request):
            return {"message": "Admin access"}
        
        @app.get("/staff")
        @require_roles(["admin", "editor"], require_all=False)
        def staff_only(request: Request):
            return {"message": "Staff access"}
    """
    role_list = [roles] if isinstance(roles, str) else roles
    
    def decorator(func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                request = _find_request(args, kwargs)
                if not request:
                    raise RoleExtractionError("Request object not found in function arguments")
                
                _check_roles(request, role_list, require_all, error_message)
                return await func(*args, **kwargs)
            
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                request = _find_request(args, kwargs)
                if not request:
                    raise RoleExtractionError("Request object not found in function arguments")
                
                _check_roles(request, role_list, require_all, error_message)
                return func(*args, **kwargs)
            
            return sync_wrapper
    
    return decorator


def require_any_role(
    roles: Union[str, List[str]],
    error_message: Optional[str] = None
) -> Callable:
    """Require ANY of the specified roles (convenience wrapper)."""
    return require_roles(roles, require_all=False, error_message=error_message)


def get_current_user_roles(request: Request) -> List[str]:
    """Get current user roles from request state.
    
    Can be used as a FastAPI dependency:
    
        @app.get("/profile")
        def profile(roles: List[str] = Depends(get_current_user_roles)):
            return {"roles": roles}
    """
    return getattr(request.state, 'user_roles', [])


def create_role_dependency(roles: Union[str, List[str]], require_all: bool = True) -> Callable:
    """Create a FastAPI dependency that enforces role requirements.
    
    Args:
        roles: Required roles
        require_all: Whether all roles are required
    
    Example:
        admin_required = create_role_dependency("admin")
        
        @app.get("/admin", dependencies=[Depends(admin_required)])
        def admin_endpoint():
            return {"message": "Admin access"}
    """
    role_list = [roles] if isinstance(roles, str) else roles
    
    def role_dependency(request: Request) -> None:
        _check_roles(request, role_list, require_all)
    
    return role_dependency


def _find_request(args: tuple, kwargs: dict) -> Optional[Request]:
    """Find Request object in function arguments."""
    for value in kwargs.values():
        if isinstance(value, Request):
            return value
    
    for arg in args:
        if isinstance(arg, Request):
            return arg
    
    return None


def _check_roles(
    request: Request,
    required_roles: List[str],
    require_all: bool = True,
    error_message: Optional[str] = None
) -> None:
    """Check if user has the required roles."""
    if not required_roles:
        return
    
    user_roles = getattr(request.state, 'user_roles', [])
    
    if require_all:
        missing = [role for role in required_roles if role not in user_roles]
        if missing:
            raise InsufficientRoleError(
                required_roles=required_roles,
                user_roles=user_roles,
                message=error_message
            )
    else:
        if not any(role in user_roles for role in required_roles):
            raise InsufficientRoleError(
                required_roles=required_roles,
                user_roles=user_roles,
                message=error_message
            ) 