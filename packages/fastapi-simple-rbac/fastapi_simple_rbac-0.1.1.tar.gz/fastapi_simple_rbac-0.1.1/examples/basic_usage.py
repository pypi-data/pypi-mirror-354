"""
Basic RBAC example for FastAPI.

Shows how to protect endpoints with role-based access control.
"""

from fastapi import FastAPI, Request
from fastapi_simple_rbac import RBACMiddleware, require_roles

app = FastAPI(title="Blog API")

# Add RBAC middleware
app.add_middleware(
    RBACMiddleware,
    secret_key="your-secret-key",
    verify_jwt_signature=False,  # Set to True in production
)

@app.get("/")
def home():
    """Public homepage."""
    return {"message": "Welcome to our blog!"}

@app.get("/posts")
def list_posts():
    """Anyone can read posts."""
    return {"posts": ["Post 1", "Post 2", "Post 3"]}

@app.get("/admin/dashboard")
@require_roles("admin")
def admin_dashboard(request: Request):
    """Admin dashboard."""
    return {"message": "Admin dashboard", "user_count": 1337}

@app.post("/posts")
@require_roles(["admin", "editor"], require_all=False)
def create_post(request: Request):
    """Create a new post (admin or editor)."""
    return {"message": "Post created successfully"}

@app.delete("/posts/{post_id}")
@require_roles("admin")
def delete_post(post_id: int, request: Request):
    """Delete a post (admin only)."""
    return {"message": f"Post {post_id} deleted"}

@app.get("/profile")
def profile(request: Request):
    """Show current user info."""
    roles = getattr(request.state, 'user_roles', [])
    return {
        "roles": roles,
        "is_admin": "admin" in roles,
        "can_edit": any(role in roles for role in ["admin", "editor"])
    }

if __name__ == "__main__":
    import uvicorn
    
    print("Blog API starting...")
    print("\nTest with JWT tokens containing roles:")
    print('{"sub": "user123", "roles": ["admin"]}')
    print('{"sub": "user456", "roles": ["editor"]}')
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 