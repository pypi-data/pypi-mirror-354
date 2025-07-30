"""RBAC exceptions."""

from typing import List, Optional


class RBACException(Exception):
    """Base exception for RBAC errors."""
    
    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InsufficientRoleError(RBACException):
    """Raised when user lacks required roles."""
    
    def __init__(
        self, 
        required_roles: List[str], 
        user_roles: Optional[List[str]] = None,
        message: Optional[str] = None
    ) -> None:
        self.required_roles = required_roles
        self.user_roles = user_roles or []
        
        if message is None:
            if self.user_roles:
                message = f"Access denied. Required: {required_roles}, have: {self.user_roles}"
            else:
                message = f"Access denied. Required roles: {required_roles}"
        
        super().__init__(message, status_code=403)


class RoleExtractionError(RBACException):
    """Raised when roles cannot be extracted from request."""
    
    def __init__(self, message: str = "Failed to extract roles from request") -> None:
        super().__init__(message, status_code=401) 