"""
Advanced example demonstrating custom role getter functions.

This example shows different ways to extract roles:
- From custom headers
- From database lookups
- From external APIs (async)
- With role hierarchies
"""

import asyncio
from typing import List
from fastapi import FastAPI, Request
from fastapi_simple_rbac import RBACMiddleware, require_roles
from fastapi_simple_rbac.utils import extract_roles_from_header, extract_roles_from_jwt

# Create FastAPI app
app = FastAPI(title="FastAPI RBAC Custom Role Getter Example")

# Simulated database of user roles
USER_ROLES_DB = {
    "user123": ["admin", "editor"],
    "user456": ["editor"],
    "user789": ["user"],
    "user000": ["vip", "user"]
}

# Role hierarchy - higher roles inherit lower role permissions
ROLE_HIERARCHY = {
    "admin": ["admin", "editor", "user"],
    "editor": ["editor", "user"],
    "user": ["user"],
    "vip": ["vip", "user"]
}

def get_roles_from_custom_header(request: Request) -> List[str]:
    """
    Extract roles from a custom header.
    
    Expects header format: X-User-Roles: admin,editor,user
    """
    return extract_roles_from_header(request, "X-User-Roles")

def get_roles_from_database(request: Request) -> List[str]:
    """
    Extract roles from a simulated database lookup.
    
    In a real application, this would query your actual database.
    """
    try:
        # Extract user ID from JWT token (without verification for demo)
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return []
        
        # In production, you'd properly decode and verify the JWT
        from jose import jwt
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("sub", "")
        
        # Look up user roles in database
        return USER_ROLES_DB.get(user_id, [])
    
    except Exception:
        # If anything goes wrong, return empty roles
        return []

def get_roles_with_hierarchy(request: Request) -> List[str]:
    """
    Extract roles and expand them based on role hierarchy.
    
    For example, if user has 'admin' role, they also get 'editor' and 'user' roles.
    """
    try:
        # First get base roles from JWT
        base_roles = extract_roles_from_jwt(request, verify_signature=False)
        
        # Expand roles based on hierarchy
        expanded_roles = set()
        for role in base_roles:
            expanded_roles.update(ROLE_HIERARCHY.get(role, [role]))
        
        return list(expanded_roles)
    
    except Exception:
        return []

async def get_roles_from_external_api(request: Request) -> List[str]:
    """
    Async role extraction from external API.
    
    This demonstrates how to use async role getters for external service calls.
    """
    try:
        # Extract user ID from JWT
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return []
        
        from jose import jwt
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("sub", "")
        
        # Simulate async API call
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # In real implementation, you'd make an HTTP request to external service
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"https://auth-service.com/users/{user_id}/roles")
        #     return response.json()["roles"]
        
        # For demo, return simulated data
        return USER_ROLES_DB.get(user_id, [])
    
    except Exception:
        return []

def get_roles_with_fallback(request: Request) -> List[str]:
    """
    Role getter with multiple fallback strategies.
    
    Tries multiple methods in order:
    1. Custom header
    2. JWT token
    3. Default user role
    """
    # Try custom header first
    roles = extract_roles_from_header(request, "X-User-Roles")
    if roles:
        return roles
    
    # Try JWT token
    try:
        roles = extract_roles_from_jwt(request, verify_signature=False)
        if roles:
            return roles
    except Exception:
        pass
    
    # Default fallback - assign basic user role
    return ["user"]

# Example 1: Header-based roles
app1 = FastAPI(title="Header-based RBAC")
app1.add_middleware(RBACMiddleware, role_getter=get_roles_from_custom_header)

@app1.get("/admin")
@require_roles(["admin"])
def header_admin(request: Request):
    return {"message": "Admin access via header", "roles": request.state.user_roles}

# Example 2: Database-based roles
app2 = FastAPI(title="Database-based RBAC")
app2.add_middleware(RBACMiddleware, role_getter=get_roles_from_database)

@app2.get("/admin")
@require_roles(["admin"])
def db_admin(request: Request):
    return {"message": "Admin access via database", "roles": request.state.user_roles}

# Example 3: Hierarchical roles
app3 = FastAPI(title="Hierarchical RBAC")
app3.add_middleware(RBACMiddleware, role_getter=get_roles_with_hierarchy)

@app3.get("/user")
@require_roles(["user"])
def hierarchy_user(request: Request):
    return {"message": "User access (admins also have this)", "roles": request.state.user_roles}

# Example 4: Async external API roles
app4 = FastAPI(title="Async External API RBAC")
app4.add_middleware(RBACMiddleware, role_getter=get_roles_from_external_api)

@app4.get("/admin")
@require_roles(["admin"])
def async_admin(request: Request):
    return {"message": "Admin access via async API", "roles": request.state.user_roles}

# Main app with fallback strategy
app.add_middleware(RBACMiddleware, role_getter=get_roles_with_fallback)

@app.get("/")
def root():
    return {
        "message": "FastAPI RBAC Custom Role Getter Examples",
        "examples": [
            "Header-based: Send X-User-Roles header",
            "Database: Use JWT with user ID",
            "Hierarchy: Roles inherit permissions",
            "Async: External API role lookup",
            "Fallback: Multiple strategies"
        ]
    }

@app.get("/admin")
@require_roles(["admin"])
def admin_endpoint(request: Request):
    return {
        "message": "Admin access granted!",
        "roles": request.state.user_roles,
        "method": "fallback strategy"
    }

@app.get("/editor")
@require_roles(["editor"])
def editor_endpoint(request: Request):
    return {
        "message": "Editor access granted!",
        "roles": request.state.user_roles
    }

@app.get("/user")
@require_roles(["user"])
def user_endpoint(request: Request):
    return {
        "message": "User access granted!",
        "roles": request.state.user_roles
    }

@app.get("/profile")
def profile_endpoint(request: Request):
    roles = getattr(request.state, 'user_roles', [])
    return {
        "message": "User profile",
        "roles": roles,
        "role_count": len(roles),
        "is_admin": "admin" in roles,
        "is_editor": "editor" in roles
    }

if __name__ == "__main__":
    import uvicorn
    
    print("FastAPI RBAC Custom Role Getter Examples")
    print("=" * 50)
    print("\nTesting methods:")
    print("1. Header-based: curl -H 'X-User-Roles: admin,editor' http://localhost:8000/admin")
    print("2. JWT-based: curl -H 'Authorization: Bearer <jwt-token>' http://localhost:8000/admin")
    print("3. No auth: curl http://localhost:8000/user (gets default 'user' role)")
    print("\nSample JWT tokens (unverified for demo):")
    
    # Generate sample tokens for testing
    from jose import jwt
    
    admin_token = jwt.encode({"sub": "user123", "roles": ["admin"]}, "secret", algorithm="HS256")
    editor_token = jwt.encode({"sub": "user456", "roles": ["editor"]}, "secret", algorithm="HS256")
    
    print(f"Admin token: {admin_token}")
    print(f"Editor token: {editor_token}")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 