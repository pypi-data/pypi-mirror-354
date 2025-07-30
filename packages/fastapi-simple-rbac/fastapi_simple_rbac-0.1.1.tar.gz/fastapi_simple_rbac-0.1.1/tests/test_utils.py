"""
Tests for RBAC utility functions.
"""

import pytest
from fastapi import Request
from jose import jwt
from unittest.mock import Mock

from fastapi_simple_rbac.utils import (
    extract_roles_from_jwt,
    extract_roles_from_header,
    create_default_role_getter
)
from fastapi_simple_rbac.exceptions import RoleExtractionError


class TestExtractRolesFromJWT:
    """Test JWT role extraction utility."""
    
    def test_extract_roles_with_valid_jwt(self):
        """Test extracting roles from valid JWT token."""
        secret_key = "test-secret"
        payload = {"sub": "user123", "roles": ["admin", "editor"]}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        
        # Mock request with Authorization header
        request = Mock(spec=Request)
        request.headers = {"Authorization": f"Bearer {token}"}
        
        roles = extract_roles_from_jwt(
            request=request,
            secret_key=secret_key,
            verify_signature=True
        )
        
        assert roles == ["admin", "editor"]
    
    def test_extract_roles_without_verification(self):
        """Test extracting roles without JWT signature verification."""
        payload = {"sub": "user123", "roles": ["user"]}
        token = jwt.encode(payload, "any-secret", algorithm="HS256")
        
        # Mock request
        request = Mock(spec=Request)
        request.headers = {"Authorization": f"Bearer {token}"}
        
        roles = extract_roles_from_jwt(
            request=request,
            verify_signature=False
        )
        
        assert roles == ["user"] 