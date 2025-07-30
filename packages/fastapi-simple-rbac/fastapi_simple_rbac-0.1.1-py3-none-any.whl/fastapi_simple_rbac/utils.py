"""
Utility functions for FastAPI Simple RBAC.
"""

import json
from typing import Any, Dict, List, Optional
from fastapi import Request
from jose import jwt, JWTError
from .exceptions import RoleExtractionError
from .types import RoleGetter


def extract_roles_from_jwt(
    request: Request,
    secret_key: Optional[str] = None,
    algorithm: str = "HS256",
    role_claim: str = "roles",
    verify_signature: bool = True
) -> List[str]:
    """
    Extract roles from JWT token in Authorization header.
    
    Args:
        request: FastAPI request object
        secret_key: JWT secret key for verification
        algorithm: JWT algorithm (default: HS256)
        role_claim: JWT claim containing roles (default: 'roles')
        verify_signature: Whether to verify JWT signature
    
    Returns:
        List of role strings
        
    Raises:
        RoleExtractionError: If token is invalid or roles cannot be extracted
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise RoleExtractionError("No Authorization header found")
    
    if not auth_header.startswith("Bearer "):
        raise RoleExtractionError("Authorization header must start with 'Bearer '")
    
    token = auth_header[7:]
    
    try:
        if verify_signature:
            if not secret_key:
                raise RoleExtractionError("Secret key required for JWT verification")
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        else:
            payload = jwt.get_unverified_claims(token)
    except JWTError as e:
        raise RoleExtractionError(f"Invalid JWT token: {str(e)}")
    
    roles = payload.get(role_claim, [])
    return _normalize_roles(roles)


def extract_roles_from_header(request: Request, header_name: str = "X-User-Roles") -> List[str]:
    """Extract roles from a custom header."""
    header_value = request.headers.get(header_name, "")
    if not header_value:
        return []
    
    roles = [role.strip() for role in header_value.split(",") if role.strip()]
    return _normalize_roles(roles)


def create_default_role_getter(
    secret_key: Optional[str] = None,
    algorithm: str = "HS256",
    role_claim: str = "roles",
    verify_signature: bool = False
) -> RoleGetter:
    """Create a JWT-based role getter function."""
    
    def get_roles_from_jwt(request: Request) -> List[str]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return []
        
        token = auth_header[7:]
        
        try:
            if verify_signature and secret_key:
                payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            else:
                payload = jwt.get_unverified_claims(token)
            
            roles = payload.get(role_claim, [])
            return _normalize_roles(roles)
            
        except JWTError:
            return []
    
    return get_roles_from_jwt


def _normalize_roles(roles) -> List[str]:
    """Normalize roles to a consistent format."""
    if not roles:
        return []
    
    if isinstance(roles, str):
        # Handle comma-separated roles in a single string
        return [role.strip() for role in roles.split(",") if role.strip()]
    
    if isinstance(roles, list):
        normalized = []
        for role in roles:
            if isinstance(role, str):
                cleaned = role.strip()
                if cleaned:  # Only add non-empty roles
                    normalized.append(cleaned)
        return normalized
    
    return [] 