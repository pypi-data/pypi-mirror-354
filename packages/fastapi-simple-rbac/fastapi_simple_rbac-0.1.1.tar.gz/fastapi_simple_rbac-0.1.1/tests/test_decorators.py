"""Decorator tests."""

import pytest
from fastapi import FastAPI, Request, Depends
from fastapi.testclient import TestClient
from jose import jwt

from fastapi_simple_rbac import require_roles, require_any_role, RBACMiddleware, get_current_user_roles, create_role_dependency
from tests.conftest import auth_headers


class TestRequireRoles:
    
    def test_admin_access_with_admin_token(self, client, admin_token):
        headers = auth_headers(admin_token)
        response = client.get("/admin", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Admin access"}
    
    def test_admin_access_without_token(self, client):
        response = client.get("/admin")
        assert response.status_code == 403
        assert "Access denied" in response.json()["message"]
    
    def test_admin_access_with_wrong_role(self, client, editor_token):
        headers = auth_headers(editor_token)
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403
        assert "Access denied" in response.json()["message"]
    
    def test_editor_access_with_editor_token(self, client, editor_token):
        headers = auth_headers(editor_token)
        response = client.get("/editor", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Editor access"}
    
    def test_admin_or_editor_with_admin_token(self, client, admin_token):
        headers = auth_headers(admin_token)
        response = client.get("/admin-or-editor", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Admin or editor access"}
    
    def test_admin_or_editor_with_editor_token(self, client, editor_token):
        headers = auth_headers(editor_token)
        response = client.get("/admin-or-editor", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Admin or editor access"}
    
    def test_admin_or_editor_with_user_token(self, client, user_token):
        headers = auth_headers(user_token)
        response = client.get("/admin-or-editor", headers=headers)
        assert response.status_code == 403
    
    def test_admin_and_editor_with_both_roles(self, client, admin_editor_token):
        headers = auth_headers(admin_editor_token)
        response = client.get("/admin-and-editor", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Admin and editor access"}
    
    def test_admin_and_editor_with_only_admin(self, client, admin_token):
        headers = auth_headers(admin_token)
        response = client.get("/admin-and-editor", headers=headers)
        assert response.status_code == 403
    
    def test_admin_and_editor_with_only_editor(self, client, editor_token):
        headers = auth_headers(editor_token)
        response = client.get("/admin-and-editor", headers=headers)
        assert response.status_code == 403
    
    def test_public_endpoint_without_token(self, client):
        response = client.get("/public")
        assert response.status_code == 200
        assert response.json() == {"message": "Public access"}

    def test_no_roles_results_in_403(self, client, no_roles_token):
        headers = auth_headers(no_roles_token)
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403
        assert "Access denied" in response.json()["message"]


class TestRequireAnyRole:
    
    def test_require_any_role_decorator(self, secret_key, make_token):
        app = FastAPI()
        app.add_middleware(RBACMiddleware, secret_key=secret_key, verify_jwt_signature=True)
        
        @app.get("/any-role")
        @require_any_role(["admin", "editor"])
        def any_role_endpoint(request: Request):
            return {"message": "Access granted"}
        
        client = TestClient(app)
        
        # Should work with admin
        admin_token = make_token(["admin"])
        headers = auth_headers(admin_token)
        response = client.get("/any-role", headers=headers)
        assert response.status_code == 200
        
        # Should work with editor
        editor_token = make_token(["editor"])
        headers = auth_headers(editor_token)
        response = client.get("/any-role", headers=headers)
        assert response.status_code == 200
        
        # Should fail with user
        user_token = make_token(["user"])
        headers = auth_headers(user_token)
        response = client.get("/any-role", headers=headers)
        assert response.status_code == 403


class TestCustomErrorMessages:
    
    def test_custom_error_message(self, secret_key, make_token):
        app = FastAPI()
        app.add_middleware(RBACMiddleware, secret_key=secret_key, verify_jwt_signature=True)
        
        @app.get("/custom-error")
        @require_roles("admin", error_message="You need admin privileges!")
        def custom_error_endpoint(request: Request):
            return {"message": "Success"}
        
        client = TestClient(app)
        
        user_token = make_token(["user"])
        headers = auth_headers(user_token)
        response = client.get("/custom-error", headers=headers)
        assert response.status_code == 403
        assert "You need admin privileges!" in response.json()["message"]


class TestAsyncEndpoints:
    
    def test_async_endpoint_with_roles(self, secret_key, make_token):
        app = FastAPI()
        app.add_middleware(RBACMiddleware, secret_key=secret_key, verify_jwt_signature=True)
        
        @app.get("/async-admin")
        @require_roles("admin")
        async def async_admin_endpoint(request: Request):
            return {"message": "Async admin access"}
        
        client = TestClient(app)
        
        # Should work with admin
        admin_token = make_token(["admin"])
        headers = auth_headers(admin_token)
        response = client.get("/async-admin", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Async admin access"}
        
        # Should fail with user
        user_token = make_token(["user"])
        headers = auth_headers(user_token)
        response = client.get("/async-admin", headers=headers)
        assert response.status_code == 403


class TestMalformedRoles:
    
    def test_malformed_jwt_roles_handled_gracefully(self, secret_key):
        app = FastAPI()
        app.add_middleware(RBACMiddleware, secret_key=secret_key, verify_jwt_signature=True)
        
        @app.get("/admin")
        @require_roles("admin")
        def admin_endpoint(request: Request):
            return {"message": "Admin access"}
        
        @app.get("/test-roles")
        def test_roles_endpoint(request: Request):
            return {"roles": getattr(request.state, 'user_roles', [])}
        
        client = TestClient(app)
        
        # Test with null roles
        payload = {"sub": "test-user", "roles": None}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403
        
        response = client.get("/test-roles", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": []}
        
        # Test with numeric roles
        payload = {"sub": "test-user", "roles": [123, 456]}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403
        
        response = client.get("/test-roles", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": []}
        
        # Test with empty string roles
        payload = {"sub": "test-user", "roles": [""]}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = auth_headers(token)
        
        response = client.get("/admin", headers=headers)
        assert response.status_code == 403


class TestFastAPIDependencies:
    
    def test_dependency_injection_with_role_enforcement(self, secret_key, make_token):
        app = FastAPI()
        app.add_middleware(RBACMiddleware, secret_key=secret_key, verify_jwt_signature=True)
        
        admin_required = create_role_dependency("admin")
        
        @app.get("/admin-dep", dependencies=[Depends(admin_required)])
        def admin_with_dependency():
            return {"message": "Admin access via dependency"}
        
        @app.get("/profile")
        def get_profile(roles: list = Depends(get_current_user_roles)):
            return {"roles": roles}
        
        client = TestClient(app)
        
        # Test dependency enforcement
        admin_token = make_token(["admin"])
        headers = auth_headers(admin_token)
        response = client.get("/admin-dep", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Admin access via dependency"}
        
        # Test role injection
        response = client.get("/profile", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"roles": ["admin"]}
        
        # Test dependency failure
        user_token = make_token(["user"])
        headers = auth_headers(user_token)
        response = client.get("/admin-dep", headers=headers)
        assert response.status_code == 403 