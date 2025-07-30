"""Middleware tests."""

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from jose import jwt
from fastapi.responses import JSONResponse

from fastapi_simple_rbac import RBACMiddleware, require_roles
from fastapi_simple_rbac.exceptions import RBACException
from fastapi_simple_rbac.utils import extract_roles_from_header
from tests.conftest import auth_headers


class TestMiddleware:
    
    def test_extracts_roles_from_jwt(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=True
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        payload = {"sub": "test-user", "roles": ["admin", "editor"]}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["admin", "editor"]}
    
    def test_handles_missing_token(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=True
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        response = client.get("/test")
        assert response.status_code == 200
        assert response.json() == {"roles": []}
    
    def test_handles_invalid_token(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=True
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        headers = auth_headers("invalid.jwt.token")
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": []}
    
    def test_works_without_signature_verification(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=False
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        # Token signed with different secret should still work
        payload = {"sub": "test-user", "roles": ["admin"]}
        token = jwt.encode(payload, "different-secret", algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["admin"]}


class TestCustomRoleGetters:
    
    def test_sync_role_getter(self):
        app = FastAPI()
        
        def get_roles_from_header(request: Request):
            return extract_roles_from_header(request, "X-User-Roles")
        
        app.add_middleware(RBACMiddleware, role_getter=get_roles_from_header)
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        headers = {"X-User-Roles": "admin,editor"}
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["admin", "editor"]}
    
    def test_async_role_getter(self):
        app = FastAPI()
        
        async def get_roles_async(request: Request):
            return extract_roles_from_header(request, "X-User-Roles")
        
        app.add_middleware(RBACMiddleware, role_getter=get_roles_async)
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        headers = {"X-User-Roles": "user,moderator"}
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["user", "moderator"]}

    def test_custom_role_getter_with_decorator(self):
        app = FastAPI()
        
        def get_roles_from_header(request: Request):
            return extract_roles_from_header(request, "X-Roles")
        
        app.add_middleware(RBACMiddleware, role_getter=get_roles_from_header)
        
        @app.get("/admin")
        @require_roles("admin")
        def admin_endpoint(request: Request):
            return {"message": "Admin access"}
        
        client = TestClient(app)
        
        # Should work with admin role
        headers = {"X-Roles": "admin,user"}
        response = client.get("/admin", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Admin access"}
        
        # Should fail without admin role
        headers = {"X-Roles": "user,editor"}
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403


class TestErrorHandling:
    
    def test_custom_error_handler(self, secret_key):
        def custom_error_handler(request: Request, exception: RBACException):
            return JSONResponse(
                status_code=exception.status_code,
                content={"error": "Custom error", "code": exception.status_code}
            )
        
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            error_handler=custom_error_handler
        )
        
        @app.get("/admin")
        @require_roles("admin")
        def admin_endpoint(request: Request):
            return {"message": "Admin access"}
        
        client = TestClient(app)
        
        # No token should trigger custom error handler
        response = client.get("/admin")
        assert response.status_code == 403
        assert "Custom error" in str(response.json())


class TestJWTConfiguration:
    
    def test_custom_role_claim(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            role_claim="permissions",
            verify_jwt_signature=True
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        payload = {"sub": "test-user", "permissions": ["admin", "editor"]}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["admin", "editor"]}
    
    def test_comma_separated_roles_in_jwt(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=True
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        payload = {"sub": "test-user", "roles": "admin,editor"}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["admin", "editor"]}
    
    def test_single_role_string_in_jwt(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=True
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        payload = {"sub": "test-user", "roles": "admin"}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["admin"]}


class TestEdgeCases:
    
    def test_empty_roles_list(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=True
        )
        
        @app.get("/test")
        def test_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        payload = {"sub": "test-user", "roles": []}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/test", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": []}
    
    def test_malformed_jwt_roles_handled_gracefully(self, secret_key):
        app = FastAPI()
        app.add_middleware(
            RBACMiddleware,
            secret_key=secret_key,
            verify_jwt_signature=True
        )
        
        @app.get("/admin")
        @require_roles("admin")
        def admin_endpoint(request: Request):
            return {"message": "Admin access"}
        
        client = TestClient(app)
        
        # Test with null roles
        payload = {"sub": "test-user", "roles": None}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403
        
        # Test with numeric roles
        payload = {"sub": "test-user", "roles": [123, 456]}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403 