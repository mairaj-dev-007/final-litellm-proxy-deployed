# Quick Start Guide

Your LiteLLM reverse proxy with domain filtering is now running! 🎉

## What I've Implemented

### ✅ Improvements Made:

1. **Fixed Middleware Implementation**
   - Changed from deprecated `ProxyMiddleware` class to standard FastAPI middleware
   - Added proper domain extraction using `urlparse`
   - Improved error handling and logging

2. **Environment-Based Configuration**
   - Domains can be configured via `ALLOWED_DOMAINS` environment variable
   - Added `STRICT_DOMAIN_CHECK` option for enhanced security
   - Simplified setup without database requirement

3. **Local Development Setup**
   - Fixed Docker Compose for local development
   - Removed database dependency for simpler setup
   - Created `.env.example` template

4. **Better Error Handling**
   - Clear logging of domain checks
   - Helpful error messages
   - Proper 403 responses for unauthorized domains

## Current Status

✅ **Running** on http://localhost:4000

View logs:
```bash
docker compose logs -f
```

## How to Use

### 1. Configure Your API Key

Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

Then restart:
```bash
docker compose restart
```

### 2. Make API Requests

The proxy filters requests based on the `Origin`, `Referer`, or `Host` headers.

**Example - Allowed Domain:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -H "Origin: https://app.stickball.biz" \
  -d '{
    "model": "gpt-main",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

**Example - Blocked Domain:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -H "Origin: https://unauthorized-site.com" \
  -d '{
    "model": "gpt-main",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```
This will return a `403 Forbidden` error.

### 3. Add More Allowed Domains

Edit `.env`:
```bash
ALLOWED_DOMAINS=app.stickball.biz,musketeers.dev,localhost,yournewdomain.com
```

Restart to apply:
```bash
docker compose restart
```

### 4. View the Swagger UI

Visit http://localhost:4000/docs in your browser

## Managing the Service

```bash
# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f litellm

# Restart after config changes
docker compose restart

# Rebuild after code changes
docker compose up -d --build
```

## Key Features

- 🔒 **Domain Filtering**: Only allows requests from specified domains
- 🌐 **Multiple Domain Support**: Configure multiple allowed domains
- 🔍 **Request Logging**: See which domains are making requests
- ⚙️ **Environment Configuration**: Easy setup via .env file
- 🐳 **Docker Support**: Simple deployment with Docker Compose

## Configuration Options

In your `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `ALLOWED_DOMAINS` | Comma-separated list of allowed domains | `app.stickball.biz,musketeers.dev,localhost,127.0.0.1` |
| `STRICT_DOMAIN_CHECK` | Reject requests with no domain info | `false` |
| `LITELLM_MASTER_KEY` | Master key for proxy authentication | `sk-1234` |

## Troubleshooting

**Port already in use?**
Edit `docker-compose.yml` and change the port:
```yaml
ports:
  - "4001:4000"  # Change 4001 to any available port
```

**Check if running:**
```bash
curl http://localhost:4000/health
```

**View detailed logs:**
```bash
docker compose logs -f
```

## Security Notes

- The proxy checks the `Origin`, `Referer`, and `Host` headers
- Health check endpoints (`/health`) skip domain validation
- Set `STRICT_DOMAIN_CHECK=true` to reject requests without domain headers
- Always use HTTPS in production
- Keep your `OPENAI_API_KEY` secret

## Next Steps

1. ✅ Set your actual OpenAI API key in `.env`
2. ✅ Test with allowed and disallowed domains
3. 📝 Configure your allowed domains list
4. 🚀 Deploy to your production environment

Enjoy your secure LiteLLM proxy! 🚀
