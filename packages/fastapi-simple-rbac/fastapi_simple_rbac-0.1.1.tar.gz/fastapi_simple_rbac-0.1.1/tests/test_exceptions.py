"""
Tests for RBAC exceptions.
"""

import pytest
from fastapi_simple_rbac.exceptions import (
    RBACException,
    InsufficientRoleError,
    RoleExtractionError
)


class TestRBACException:
    """Test the base RBACException class."""
    
    def test_rbac_exception_creation(self):
        """Test creating RBACException with message and status code."""
        exception = RBACException("Test error", status_code=400)
        
        assert str(exception) == "Test error"
        assert exception.message == "Test error"
        assert exception.status_code == 400
    
    def test_rbac_exception_default_status_code(self):
        """Test RBACException with default status code."""
        exception = RBACException("Test error")
        
        assert exception.status_code == 500
        assert exception.message == "Test error"


class TestInsufficientRoleError:
    """Test the InsufficientRoleError exception."""
    
    def test_insufficient_role_error_with_user_roles(self):
        """Test InsufficientRoleError with user roles provided."""
        required_roles = ["admin", "editor"]
        user_roles = ["user"]
        
        exception = InsufficientRoleError(
            required_roles=required_roles,
            user_roles=user_roles
        )
        
        assert exception.status_code == 403
        assert exception.required_roles == required_roles
        assert exception.user_roles == user_roles
        assert "Required: ['admin', 'editor']" in exception.message
        assert "have: ['user']" in exception.message
    
    def test_insufficient_role_error_without_user_roles(self):
        """Test InsufficientRoleError without user roles."""
        required_roles = ["admin"]
        
        exception = InsufficientRoleError(required_roles=required_roles)
        
        assert exception.status_code == 403
        assert exception.required_roles == required_roles
        assert exception.user_roles == []
        assert "Required roles: ['admin']" in exception.message
        assert "user has roles" not in exception.message
    
    def test_insufficient_role_error_with_custom_message(self):
        """Test InsufficientRoleError with custom message."""
        required_roles = ["admin"]
        custom_message = "You need admin access!"
        
        exception = InsufficientRoleError(
            required_roles=required_roles,
            message=custom_message
        )
        
        assert exception.message == custom_message
        assert exception.status_code == 403
    
    def test_insufficient_role_error_empty_required_roles(self):
        """Test InsufficientRoleError with empty required roles."""
        exception = InsufficientRoleError(required_roles=[])
        
        assert exception.required_roles == []
        assert exception.status_code == 403


class TestRoleExtractionError:
    """Test the RoleExtractionError exception."""
    
    def test_role_extraction_error_default_message(self):
        """Test RoleExtractionError with default message."""
        exception = RoleExtractionError()
        
        assert exception.message == "Failed to extract roles from request"
        assert exception.status_code == 401
    
    def test_role_extraction_error_custom_message(self):
        """Test RoleExtractionError with custom message."""
        custom_message = "JWT token is invalid"
        exception = RoleExtractionError(custom_message)
        
        assert exception.message == custom_message
        assert exception.status_code == 401
    
    def test_role_extraction_error_inheritance(self):
        """Test that RoleExtractionError inherits from RBACException."""
        exception = RoleExtractionError("Test error")
        
        assert isinstance(exception, RBACException)
        assert isinstance(exception, Exception) 