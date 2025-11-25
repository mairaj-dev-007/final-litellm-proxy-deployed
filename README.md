# LiteLLM Reverse Proxy with Domain Filtering

A LiteLLM reverse proxy setup with custom domain filtering middleware to restrict API access based on allowed domains.

## Features

- 🔒 Domain-based access control
- 🐘 PostgreSQL database integration
- 🐳 Docker and Docker Compose support
- 🔧 Environment-based configuration
- 📝 Request logging and monitoring

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Copy the environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your configuration:**
   - Set your `OPENAI_API_KEY`
   - Update `ALLOWED_DOMAINS` if needed
   - Adjust database credentials if desired

3. **Start the services:**
   ```bash
   docker-compose up -d
   ```

4. **Check the logs:**
   ```bash
   docker-compose logs -f litellm
   ```

5. **Access the proxy:**
   - API endpoint: http://localhost:4000
   - Swagger UI: http://localhost:4000/docs

### Option 2: Running Locally with Python

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Start PostgreSQL** (if not using Docker):
   ```bash
   # Install and start PostgreSQL on your system
   # Create a database named 'litellm_db'
   ```

4. **Run the proxy:**
   ```bash
   litellm --config config.yaml
   ```

## Configuration

### Allowed Domains

Edit the `ALLOWED_DOMAINS` in your `.env` file:

```env
ALLOWED_DOMAINS=app.stickball.biz,musketeers.dev,localhost,127.0.0.1
```

### Strict Domain Check

Enable strict mode to reject requests without domain information:

```env
STRICT_DOMAIN_CHECK=true
```

## Testing the Proxy

```bash
# Test with allowed domain
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -H "Origin: https://app.stickball.biz" \
  -d '{
    "model": "gpt-main",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Test with disallowed domain (should return 403)
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -H "Origin: https://unauthorized-domain.com" \
  -d '{
    "model": "gpt-main",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Stopping the Services

```bash
docker-compose down
```

To also remove the database volume:
```bash
docker-compose down -v
```

## Troubleshooting

- **Port already in use:** Change the port in `docker-compose.yml` (e.g., `4001:4000`)
- **Database connection issues:** Ensure PostgreSQL is running and credentials match
- **Middleware not loading:** Check the logs for import errors

## Project Structure

```
.
├── proxy.py              # Custom domain filtering middleware
├── config.yaml           # LiteLLM configuration
├── docker-compose.yml    # Docker Compose setup
├── Dockerfile           # Custom Docker image
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```
