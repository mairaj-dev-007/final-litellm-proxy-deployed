"""
Custom startup script for LiteLLM with domain filtering middleware.
This file is imported by LiteLLM to add custom middleware.
"""
from proxy import domain_filter_middleware

async def load_middlewares(app):
    """Load custom middlewares into the FastAPI app."""
    from starlette.middleware.base import BaseHTTPMiddleware
    
    print("🔒 Loading domain filter middleware...")
    app.add_middleware(BaseHTTPMiddleware, dispatch=domain_filter_middleware)
    print("✅ Domain filter middleware loaded successfully!")
    
    return app
