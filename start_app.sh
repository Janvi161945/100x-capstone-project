#!/bin/bash

# AI Learning Planner - Startup Script
# This script starts all necessary services

echo "=========================================="
echo "  AI Learning Planner - Startup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Ollama is installed
echo "Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama is not installed${NC}"
    echo ""
    echo "Install Ollama:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ Ollama is installed${NC}"

# Check if Ollama is running
echo "Checking if Ollama is running..."
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama is already running${NC}"
else
    echo -e "${YELLOW}⚠️  Ollama is not running${NC}"
    echo "Starting Ollama server..."
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3

    if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start Ollama${NC}"
        echo "Check ollama.log for errors"
        exit 1
    fi
fi

# Check if model is installed
echo "Checking if llama3.2 model is installed..."
if ollama list | grep -q llama3.2; then
    echo -e "${GREEN}✅ llama3.2 model is installed${NC}"
else
    echo -e "${YELLOW}⚠️  llama3.2 model not found${NC}"
    echo "Pulling llama3.2 model (this may take a few minutes)..."
    ollama pull llama3.2
    echo -e "${GREEN}✅ Model installed${NC}"
fi

# Check Python dependencies
echo "Checking Python dependencies..."
if python3 -c "import requests, pydantic, fastapi, uvicorn" 2>/dev/null; then
    echo -e "${GREEN}✅ All Python dependencies are installed${NC}"
else
    echo -e "${YELLOW}⚠️  Some Python dependencies are missing${NC}"
    echo "Installing dependencies..."
    pip install -q requests pydantic fastapi uvicorn
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

# Start API server
echo "Starting API server..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use${NC}"
    echo "Killing existing process..."
    kill $(lsof -t -i:8000) 2>/dev/null
    sleep 2
fi

nohup python3 api_ollama_example.py > api.log 2>&1 &
API_PID=$!
sleep 3

# Check if API is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API server started (PID: $API_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start API server${NC}"
    echo "Check api.log for errors"
    exit 1
fi

# Start frontend server
echo "Starting frontend server..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 3000 is already in use${NC}"
    echo "Killing existing process..."
    kill $(lsof -t -i:3000) 2>/dev/null
    sleep 2
fi

cd frontend
nohup python3 -m http.server 3000 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 2

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend server started (PID: $FRONTEND_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start frontend server${NC}"
    echo "Check frontend.log for errors"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}  ✅ All services started successfully!${NC}"
echo "=========================================="
echo ""
echo "📊 Service Status:"
echo "  • Ollama:   http://localhost:11434"
echo "  • API:      http://localhost:8000"
echo "  • Frontend: http://localhost:3000"
echo ""
echo "🌐 Open your browser and visit:"
echo -e "  ${GREEN}http://localhost:3000${NC}"
echo ""
echo "📝 Logs:"
echo "  • Ollama:   ollama.log"
echo "  • API:      api.log"
echo "  • Frontend: frontend.log"
echo ""
echo "🛑 To stop all services, run:"
echo "  ./stop_app.sh"
echo ""
echo "✨ Enjoy your AI Learning Planner!"
echo ""
