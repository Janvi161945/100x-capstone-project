#!/bin/bash

# AI Learning Planner - Stop Script
# This script stops all running services

echo "=========================================="
echo "  AI Learning Planner - Stop Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Stop Frontend (port 3000)
echo "Stopping frontend server..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    kill $(lsof -t -i:3000) 2>/dev/null
    echo -e "${GREEN}✅ Frontend server stopped${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend server was not running${NC}"
fi

# Stop API (port 8000)
echo "Stopping API server..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    kill $(lsof -t -i:8000) 2>/dev/null
    echo -e "${GREEN}✅ API server stopped${NC}"
else
    echo -e "${YELLOW}⚠️  API server was not running${NC}"
fi

# Stop Ollama (optional - you might want to keep it running)
echo ""
read -p "Do you want to stop Ollama server? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Stopping Ollama server..."
    pkill ollama 2>/dev/null
    echo -e "${GREEN}✅ Ollama server stopped${NC}"
else
    echo -e "${YELLOW}⚠️  Ollama server kept running${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}  ✅ Services stopped successfully!${NC}"
echo "=========================================="
echo ""
echo "To start again, run:"
echo "  ./start_app.sh"
echo ""
