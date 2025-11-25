from fastapi import Request, HTTPException
from urllib.parse import urlparse
import os
from typing import Optional
import litellm

# Load allowed domains from environment or use defaults
ALLOWED_DOMAINS = os.getenv("ALLOWED_DOMAINS", "app.stickball.biz,musketeers.dev").split(",")
ALLOWED_DOMAINS = [domain.strip() for domain in ALLOWED_DOMAINS]

print(f"Domain filter enabled. Allowed domains: {ALLOWED_DOMAINS}")

def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL string."""
    if not url:
        return None
    
    # Remove protocol if present
    if "://" in url:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.hostname
    else:
        domain = url.split("/")[0]
    
    # Remove port if present
    if domain and ":" in domain:
        domain = domain.split(":")[0]
    
    return domain

async def domain_filter_middleware(request: Request, call_next):
    """Middleware to filter requests based on origin/referer domain."""
    
    # Skip domain check for health check endpoints
    if request.url.path in ["/health", "/health/readiness", "/health/liveliness"]:
        return await call_next(request)
    
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    host = request.headers.get("host")
    
    domain = None
    
    # Try to extract domain from origin first, then referer, then host
    if origin:
        domain = extract_domain(origin)
    elif referer:
        domain = extract_domain(referer)
    elif host:
        domain = extract_domain(host)
    
    # Log the request for debugging
    print(f"Request from domain: {domain} (origin: {origin}, referer: {referer}, host: {host})")
    
    # Check if domain is allowed
    if domain and domain not in ALLOWED_DOMAINS:
        print(f"Domain {domain} not in allowed list: {ALLOWED_DOMAINS}")
        raise HTTPException(
            status_code=403, 
            detail=f"Forbidden: Domain '{domain}' not allowed"
        )
    
    # If no domain found but we have strict mode, reject
    if not domain and os.getenv("STRICT_DOMAIN_CHECK", "false").lower() == "true":
        print("No domain found and strict mode enabled")
        raise HTTPException(
            status_code=403,
            detail="Forbidden: No valid domain found in request"
        )
    
    return await call_next(request)


# LiteLLM callback approach
async def check_domain_before_call(
    kwargs,  # kwargs to completion
    completion_response,  # response from completion
    start_time,
    end_time,
):
    """Pre-request callback to check domain."""
    request = kwargs.get("litellm_call_id_headers", {})
    print(f"🔍 Checking request: {request}")
    return kwargs

# Register the callback
litellm.success_callback = [check_domain_before_call]
litellm.failure_callback = [check_domain_before_call]
