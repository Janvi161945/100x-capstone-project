# Ollama Quick Start - 5 Minutes

Get your free, local LLM learning planner running in 5 minutes.

## Prerequisites

- Python 3.8+
- 8GB+ RAM
- 5GB+ free disk space

## Setup (4 Steps)

### 1. Install Ollama (2 minutes)

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download/windows

### 2. Start Ollama & Pull Model (2 minutes)

```bash
# Start Ollama (keep this terminal open)
ollama serve

# In a NEW terminal, pull the model
ollama pull llama3.2
```

Wait for download to complete (~3GB).

### 3. Install Python Dependencies (30 seconds)

```bash
cd /home/janvi/capstone-project
pip install requests pydantic fastapi uvicorn
```

### 4. Test It! (30 seconds)

```bash
python3 ollama_planner.py
```

You should see:
```
✅ Connected to Ollama (model: llama3.2)
✅ Step 1: Background question generated
✅ Step 2: Follow-up question generated
✅ Step 3: Time question generated
✅ Step 4: Learning plan generated
```

## Usage

### Option 1: Python Script

```python
from ollama_planner import OllamaClient, OllamaLearningPlanner

# Setup
client = OllamaClient(model="llama3.2")
planner = OllamaLearningPlanner(client)

# Use it
question = planner.get_background_question()
print(question)
```

### Option 2: API Server

```bash
# Start the API
python3 api_ollama_example.py
```

Visit http://localhost:8000/docs for interactive API documentation.

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get background question
curl http://localhost:8000/api/onboarding/step1

# Generate plan
curl -X POST http://localhost:8000/api/onboarding/generate-plan \
  -H "Content-Type: application/json" \
  -d '{
    "background": "Tech",
    "focus_goal": "Frontend",
    "time": "10 minutes"
  }'
```

## Files You Need

| File | Purpose |
|------|---------|
| `ollama_planner.py` | Ollama-based planner |
| `api_ollama_example.py` | FastAPI with Ollama |
| `prompt_templates.py` | Prompt templates |
| `llm_response_schemas.py` | Validation schemas |

## Common Commands

```bash
# Start Ollama server
ollama serve

# Pull a model
ollama pull llama3.2

# List installed models
ollama list

# Test a model
ollama run llama3.2

# Remove a model
ollama rm llama3.2

# Check Ollama version
ollama --version

# View logs
ollama logs
```

## Troubleshooting

### "Could not connect to Ollama"
```bash
# Make sure Ollama is running
ollama serve
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3.2
```

### Slow responses
```bash
# Use a smaller/faster model
ollama pull phi3
```

Then edit `api_ollama_example.py`:
```python
ollama_client = OllamaClient(model="phi3")
```

## Model Options

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| **llama3.2** ⭐ | 3GB | Fast | Good |
| llama3.1 | 4.7GB | Medium | Great |
| phi3 | 2.3GB | Very Fast | OK |
| mistral | 4.1GB | Medium | Good |

**Recommendation:** Use `llama3.2` for the best balance.

## Next Steps

1. ✅ Test the planner: `python3 ollama_planner.py`
2. ✅ Start the API: `python3 api_ollama_example.py`
3. ✅ Build your frontend
4. ✅ Connect to the API endpoints
5. ✅ Deploy!

## Cost

**$0** - Completely free! 🎉

No API keys, no usage limits, no monthly bills.

## Documentation

- **This file** - Quick start (you are here)
- `OLLAMA_SETUP.md` - Detailed setup guide
- `LLM_PLANNER_README.md` - System documentation
- `ARCHITECTURE.md` - System architecture

## Support

- Ollama Docs: https://ollama.com
- GitHub: https://github.com/ollama/ollama
- Discord: https://discord.gg/ollama

---

**You're ready!** Start building with zero API costs.
