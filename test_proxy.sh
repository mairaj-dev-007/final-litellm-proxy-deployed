#!/bin/bash

echo "🧪 Testing LiteLLM Proxy with Domain Filtering"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health check
echo -e "${YELLOW}Test 1: Health Check${NC}"
curl -s http://localhost:4000/health | jq '.' || echo "Health check endpoint"
echo ""

# Test 2: Request from allowed domain (should succeed)
echo -e "${YELLOW}Test 2: Request from ALLOWED domain (app.stickball.biz)${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -H "Origin: https://app.stickball.biz" \
  -d '{
    "model": "gpt-main",
    "messages": [{"role": "user", "content": "Say hello!"}],
    "max_tokens": 10
  }')
  
status_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$status_code" = "200" ]; then
    echo -e "${GREEN}✓ PASSED - Status: $status_code${NC}"
    echo "$body" | jq '.choices[0].message.content' 2>/dev/null || echo "$body"
else
    echo -e "${RED}✗ FAILED - Status: $status_code${NC}"
    echo "$body"
fi
echo ""

# Test 3: Request from disallowed domain (should fail with 403)
echo -e "${YELLOW}Test 3: Request from DISALLOWED domain (evil.com)${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -H "Origin: https://evil.com" \
  -d '{
    "model": "gpt-main",
    "messages": [{"role": "user", "content": "Say hello!"}]
  }')
  
status_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$status_code" = "403" ]; then
    echo -e "${GREEN}✓ PASSED - Correctly blocked! Status: $status_code${NC}"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    echo -e "${RED}✗ FAILED - Should have been blocked! Status: $status_code${NC}"
    echo "$body"
fi
echo ""

# Test 4: Request from localhost (should succeed)
echo -e "${YELLOW}Test 4: Request from localhost (should be allowed)${NC}"
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -H "Origin: http://localhost:3000" \
  -d '{
    "model": "gpt-main",
    "messages": [{"role": "user", "content": "Hello from localhost!"}],
    "max_tokens": 10
  }')
  
status_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$status_code" = "200" ]; then
    echo -e "${GREEN}✓ PASSED - Status: $status_code${NC}"
    echo "$body" | jq '.choices[0].message.content' 2>/dev/null || echo "$body"
else
    echo -e "${RED}✗ FAILED - Status: $status_code${NC}"
    echo "$body"
fi
echo ""

echo "=============================================="
echo "🎉 Testing complete!"
echo ""
echo "Note: For tests that make actual API calls to succeed,"
echo "you need to set a valid OPENAI_API_KEY in your .env file"
