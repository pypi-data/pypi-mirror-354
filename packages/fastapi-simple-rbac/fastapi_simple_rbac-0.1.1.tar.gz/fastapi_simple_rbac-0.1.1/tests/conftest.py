"""Test fixtures and configuration."""

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from jose import jwt

from fastapi_simple_rbac import RBACMiddleware, require_roles


@pytest.fixture
def secret_key():
    return "test-secret-key-12345"


@pytest.fixture
def app():
    return FastAPI()


@pytest.fixture
def app_with_rbac(secret_key):
    app = FastAPI()
    
    app.add_middleware(
        RBACMiddleware,
        secret_key=secret_key,
        verify_jwt_signature=True
    )
    
    @app.get("/public")
    def public():
        return {"message": "Public access"}
    
    @app.get("/admin")
    @require_roles("admin")
    def admin_only(request: Request):
        return {"message": "Admin access"}
    
    @app.get("/editor")
    @require_roles("editor")
    def editor_only(request: Request):
        return {"message": "Editor access"}
    
    @app.get("/admin-or-editor")
    @require_roles(["admin", "editor"], require_all=False)
    def admin_or_editor(request: Request):
        return {"message": "Admin or editor access"}
    
    @app.get("/admin-and-editor")
    @require_roles(["admin", "editor"], require_all=True)
    def admin_and_editor(request: Request):
        return {"message": "Admin and editor access"}
    
    return app


@pytest.fixture
def client(app_with_rbac):
    return TestClient(app_with_rbac)


@pytest.fixture
def make_token(secret_key):
    """Factory to create JWT tokens with roles."""
    def _make_token(roles, **extra_claims):
        payload = {
            "sub": "test-user",
            "roles": roles,
            **extra_claims
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")
    
    return _make_token


@pytest.fixture
def admin_token(make_token):
    return make_token(["admin"])


@pytest.fixture
def editor_token(make_token):
    return make_token(["editor"])


@pytest.fixture
def admin_editor_token(make_token):
    return make_token(["admin", "editor"])


@pytest.fixture
def user_token(make_token):
    return make_token(["user"])


@pytest.fixture
def no_roles_token(make_token):
    return make_token([])


def auth_headers(token: str) -> dict:
    """Helper to create auth headers."""
    return {"Authorization": f"Bearer {token}"} 