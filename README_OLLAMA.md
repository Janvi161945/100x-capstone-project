# LLM Learning Planner with Ollama (FREE)

A complete, production-ready learning planner system using **Ollama** - a free, local LLM with zero API costs.

## 🎯 What You Get

- ✅ **Free forever** - No API costs, no subscriptions
- ✅ **Private** - All data stays on your machine
- ✅ **Fast** - No network latency after initial setup
- ✅ **Offline** - Works without internet
- ✅ **Production-ready** - Type-safe, validated, tested

## 🚀 Quick Start (5 Minutes)

### 1. Install Ollama

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** Download from https://ollama.com/download/windows

### 2. Setup

```bash
# Start Ollama server (in one terminal)
ollama serve

# Pull the model (in another terminal)
ollama pull llama3.2

# Install Python dependencies
pip install requests pydantic fastapi uvicorn

# Test it!
python3 test_ollama.py
```

### 3. Run

```bash
# Test the planner
python3 ollama_planner.py

# Or start the API server
python3 api_ollama_example.py
```

Visit http://localhost:8000/docs for API documentation.

## 📁 File Structure

### Ollama-Specific Files (New)
```
ollama_planner.py          # Ollama-based orchestrator
api_ollama_example.py      # FastAPI with Ollama
test_ollama.py             # Ollama setup verification
OLLAMA_SETUP.md            # Detailed Ollama guide
OLLAMA_QUICKSTART.md       # 5-minute quick start
README_OLLAMA.md           # This file
```

### Shared Files (Used by both Anthropic & Ollama)
```
prompt_templates.py        # Prompt templates
llm_response_schemas.py    # Validation schemas
llm_system_prompt.md       # System prompt
test_planner.py            # Schema tests
```

### Original Files (Anthropic/OpenAI)
```
learning_planner.py        # Anthropic-based orchestrator
api_example.py             # FastAPI with Anthropic
```

### Documentation
```
LLM_PLANNER_README.md      # Full system docs
ARCHITECTURE.md            # Architecture guide
QUICKSTART.md              # Original quick start
PLANNER_SYSTEM_SUMMARY.md  # System summary
```

## 🎓 How It Works

```
User completes 4-step onboarding:

Step 1: Background question (Tech/Product/Design/Non-tech)
   ↓
Step 2: Follow-up question (adapts to background)
   ↓
Step 3: Time commitment (5/10/20 minutes)
   ↓
Step 4: Generate 7-day personalized AI learning plan
```

Each step returns **pure JSON** (no chat, no explanations):

```json
{
  "plan": [
    {
      "day": 1,
      "title": "What is AI?",
      "what_to_learn": "Understand AI basics...",
      "what_to_do": "Write 3 examples...",
      "time_required": "10 minutes"
    }
    // ... 6 more days
  ]
}
```

## 💻 Usage Examples

### Python Script

```python
from ollama_planner import OllamaClient, OllamaLearningPlanner

# Setup
client = OllamaClient(model="llama3.2")
planner = OllamaLearningPlanner(client)

# Get questions
q1 = planner.get_background_question()
q2 = planner.get_followup_question("Tech")
q3 = planner.get_time_question()

# Generate plan
plan = planner.generate_learning_plan(
    background="Tech",
    focus_goal="Frontend",
    time="10 minutes"
)

print(plan)
```

### API Server

```bash
# Start server
python3 api_ollama_example.py
```

```bash
# Call endpoints
curl http://localhost:8000/api/onboarding/step1

curl -X POST http://localhost:8000/api/onboarding/generate-plan \
  -H "Content-Type: application/json" \
  -d '{
    "background": "Tech",
    "focus_goal": "Frontend",
    "time": "10 minutes"
  }'
```

## 🔧 Configuration

### Change Model

Edit `api_ollama_example.py` or `ollama_planner.py`:

```python
ollama_client = OllamaClient(
    model="mistral"  # or llama3.1, qwen2.5, phi3
)
```

### Available Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llama3.2** ⭐ | 3GB | ⚡⚡⚡ | ⭐⭐⭐ | **Recommended** |
| llama3.1 | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | Better quality |
| mistral | 4.1GB | ⚡⚡ | ⭐⭐⭐ | Code tasks |
| qwen2.5 | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | Multilingual |
| phi3 | 2.3GB | ⚡⚡⚡⚡ | ⭐⭐ | Fast testing |

Install with: `ollama pull <model-name>`

### Remote Ollama Server

```python
ollama_client = OllamaClient(
    base_url="http://192.168.1.100:11434",
    model="llama3.2"
)
```

## 🧪 Testing

### Test Ollama Setup
```bash
python3 test_ollama.py
```

### Test Planner
```bash
python3 ollama_planner.py
```

### Test Schemas
```bash
python3 test_planner.py
```

### Test API
```bash
# Start server
python3 api_ollama_example.py

# Test health
curl http://localhost:8000/health

# Test endpoints
curl http://localhost:8000/api/onboarding/step1
```

## 🐛 Troubleshooting

### "Could not connect to Ollama"

```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/version
```

### "Model not found"

```bash
# Install the model
ollama pull llama3.2

# List installed models
ollama list
```

### Slow responses

```bash
# Use a faster model
ollama pull phi3
```

Then update the code to use `phi3`.

### JSON parsing errors

The system has built-in failsafes. If still failing:
1. Try a better model: `ollama pull llama3.1`
2. Check Ollama logs: `ollama logs`
3. Restart Ollama: `pkill ollama && ollama serve`

## 📊 Performance

### Speed

| Operation | Time |
|-----------|------|
| Step 1 (Background question) | 5-10 seconds |
| Step 2 (Follow-up) | 5-10 seconds |
| Step 3 (Time question) | 5-10 seconds |
| Step 4 (Learning plan) | 30-60 seconds |

**Tip:** Cache steps 1-3 to serve them instantly.

### Resource Usage

- **RAM:** 4-8GB (depending on model)
- **CPU:** Moderate during generation
- **Disk:** 3-5GB (for model)
- **Network:** None (after initial setup)

## 💰 Cost Comparison

| Provider | Setup | Per Request | 1000 Users/Month |
|----------|-------|-------------|------------------|
| **Ollama** | $0 | $0 | **$0** 🎉 |
| Anthropic | $0 | ~$0.005 | ~$20 |
| OpenAI | $0 | ~$0.01 | ~$40 |

**Ollama is completely free!**

## 🚀 Production Deployment

### Option 1: Single Server

```bash
# Install Ollama on server
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2

# Start services
ollama serve &
python3 api_ollama_example.py
```

### Option 2: Docker

```dockerfile
FROM python:3.10-slim

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN ollama pull llama3.2

CMD ["sh", "-c", "ollama serve & sleep 5 && python3 api_ollama_example.py"]
```

### Option 3: Separate Ollama Server

```python
# On App Server
ollama_client = OllamaClient(
    base_url="http://ollama-server:11434",
    model="llama3.2"
)
```

## 📈 Scaling

### For < 100 users
- Single server with Ollama
- Cache steps 1-3
- Good enough!

### For 100-1000 users
- Dedicated Ollama server
- App server(s) with load balancer
- Redis cache for questions
- Background job queue for plan generation

### For > 1000 users
- Consider upgrading to Anthropic/OpenAI for:
  - Faster responses
  - Better quality
  - Less infrastructure management

## 📚 Documentation

- **`OLLAMA_QUICKSTART.md`** - 5-minute quick start
- **`OLLAMA_SETUP.md`** - Detailed setup guide
- **`LLM_PLANNER_README.md`** - Full system documentation
- **`ARCHITECTURE.md`** - System architecture
- **This file** - Ollama-specific README

## 🔗 Resources

### Ollama
- Website: https://ollama.com
- GitHub: https://github.com/ollama/ollama
- Models: https://ollama.com/library
- Discord: https://discord.gg/ollama

### This Project
- Run tests: `python3 test_ollama.py`
- Check health: `curl http://localhost:8000/health`
- API docs: http://localhost:8000/docs

## ✅ Checklist

Before going to production:

- [ ] Ollama installed and running
- [ ] Model pulled (`ollama pull llama3.2`)
- [ ] Tests pass (`python3 test_ollama.py`)
- [ ] API works (`python3 api_ollama_example.py`)
- [ ] Caching implemented (for steps 1-3)
- [ ] Error handling tested
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Auto-restart on failure

## 🎉 Next Steps

1. ✅ **Verify setup:** `python3 test_ollama.py`
2. ✅ **Test planner:** `python3 ollama_planner.py`
3. ✅ **Start API:** `python3 api_ollama_example.py`
4. ✅ **Build frontend:** Connect to API endpoints
5. ✅ **Deploy:** Use Docker or direct installation
6. ✅ **Scale:** Add caching, background jobs as needed

## 💡 Pro Tips

1. **Cache common questions** - Steps 1-3 rarely change
2. **Use background jobs** - Plan generation takes 30-60s
3. **Monitor resource usage** - Ollama uses RAM
4. **Pre-pull models** - Download before deployment
5. **Start small** - Use Ollama initially, upgrade later if needed

---

**You're all set!** You now have a completely free, production-ready learning planner with zero API costs. 🚀

For questions or issues, check `OLLAMA_SETUP.md` or run `python3 test_ollama.py`.
