"""
Custom LiteLLM proxy with domain filtering middleware.
This wraps the standard LiteLLM proxy and adds domain-based access control.
"""
import os
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from urllib.parse import urlparse
from typing import Optional

# Import LiteLLM proxy server
from litellm.proxy.proxy_server import app, initialize

# Load allowed domains
ALLOWED_DOMAINS = os.getenv("ALLOWED_DOMAINS", "app.stickball.biz,musketeers.dev").split(",")
ALLOWED_DOMAINS = [domain.strip() for domain in ALLOWED_DOMAINS]

print(f"🔒 Domain filter enabled. Allowed domains: {ALLOWED_DOMAINS}")

def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL string."""
    if not url:
        return None
    
    if "://" in url:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.hostname
    else:
        domain = url.split("/")[0]
    
    if domain and ":" in domain:
        domain = domain.split(":")[0]
    
    return domain

@app.middleware("http")
async def domain_filter_middleware(request: Request, call_next):
    """Filter requests based on origin/referer domain."""
    
    # Skip domain check for health and docs endpoints
    if request.url.path in ["/health", "/health/readiness", "/health/liveliness", "/", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    host = request.headers.get("host")
    
    domain = None
    if origin:
        domain = extract_domain(origin)
    elif referer:
        domain = extract_domain(referer)
    elif host:
        domain = extract_domain(host)
    
    print(f"📍 Request from domain: {domain} | Path: {request.url.path}")
    
    # Check if domain is allowed
    if domain and domain not in ALLOWED_DOMAINS:
        print(f"🚫 BLOCKED - Domain '{domain}' not in allowed list: {ALLOWED_DOMAINS}")
        return JSONResponse(
            status_code=403,
            content={"error": {"message": f"Forbidden: Domain '{domain}' not allowed", "type": "domain_error", "code": "403"}}
        )
    
    # Strict mode check
    if not domain and os.getenv("STRICT_DOMAIN_CHECK", "false").lower() == "true":
        print(f"🚫 BLOCKED - No domain found and strict mode enabled")
        return JSONResponse(
            status_code=403,
            content={"error": {"message": "Forbidden: No valid domain found in request", "type": "domain_error", "code": "403"}}
        )
    
    print(f"✅ ALLOWED - Domain '{domain}' is authorized")
    return await call_next(request)

print("✨ Domain filtering middleware registered successfully!")
