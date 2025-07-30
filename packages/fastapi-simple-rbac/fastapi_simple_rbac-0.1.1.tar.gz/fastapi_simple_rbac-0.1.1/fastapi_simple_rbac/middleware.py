"""RBAC middleware for FastAPI."""

import inspect
from typing import Callable, List, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from .exceptions import RBACException, RoleExtractionError
from .types import RoleGetter
from .utils import create_default_role_getter


class RBACMiddleware(BaseHTTPMiddleware):
    """Middleware that extracts user roles and makes them available to route handlers."""
    
    def __init__(
        self,
        app,
        role_getter: Optional[RoleGetter] = None,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        role_claim: str = "roles",
        verify_jwt_signature: bool = False,
        error_handler: Optional[Callable[[Request, RBACException], Response]] = None
    ):
        super().__init__(app)
        
        if role_getter is None:
            self.role_getter = create_default_role_getter(
                secret_key=secret_key,
                algorithm=algorithm,
                role_claim=role_claim,
                verify_signature=verify_jwt_signature
            )
        else:
            self.role_getter = role_getter
        
        self.error_handler = error_handler or self._default_error_handler
        self._is_async = inspect.iscoroutinefunction(self.role_getter)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Extract roles and process the request."""
        try:
            if self._is_async:
                roles = await self.role_getter(request)
            else:
                roles = self.role_getter(request)
            
            request.state.user_roles = roles or []
            
        except Exception as e:
            request.state.user_roles = []
            
            # Only handle critical errors, not missing auth
            if isinstance(e, RoleExtractionError) and "Authorization header" not in str(e):
                return self.error_handler(request, e)
        
        try:
            return await call_next(request)
        except RBACException as e:
            return self.error_handler(request, e)
    
    def _default_error_handler(self, request: Request, exception: RBACException) -> Response:
        """Default error response for RBAC failures."""
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "error": "Access denied",
                "message": exception.message,
            }
        ) 