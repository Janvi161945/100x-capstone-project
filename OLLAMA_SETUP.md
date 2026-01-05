# Ollama Setup Guide - Free, Local LLM

This guide shows you how to use **Ollama** (free, local LLM) instead of paid APIs like Anthropic or OpenAI.

## Why Ollama?

✅ **Free** - No API costs
✅ **Private** - Data stays on your machine
✅ **Fast** - No network latency
✅ **Offline** - Works without internet
✅ **Easy** - Simple installation

## Installation

### Step 1: Install Ollama

#### macOS / Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows
Download from: https://ollama.com/download/windows

#### Verify Installation
```bash
ollama --version
```

### Step 2: Start Ollama Server

```bash
ollama serve
```

You should see:
```
Ollama is running on http://localhost:11434
```

Keep this terminal open (or run in background).

### Step 3: Pull a Model

Download a model to use:

```bash
# Recommended: Llama 3.2 (3GB, fast, good quality)
ollama pull llama3.2

# Alternative options:
ollama pull llama3.1      # 4.7GB, better quality
ollama pull mistral       # 4.1GB, good for code
ollama pull qwen2.5       # 4.7GB, multilingual
ollama pull phi3          # 2.3GB, very fast but lower quality
```

**Recommendation:** Start with `llama3.2` - it's fast and works well.

### Step 4: Test It

```bash
ollama run llama3.2
```

You should see a prompt. Type something and get a response!

Exit with: `/bye`

## Using with the Learning Planner

### Quick Start (3 Commands)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Make sure Ollama is running (in another terminal)
ollama serve

# 3. Test the planner
python3 ollama_planner.py
```

### Python Example

```python
from ollama_planner import OllamaClient, OllamaLearningPlanner

# Initialize Ollama client
ollama_client = OllamaClient(
    base_url="http://localhost:11434",
    model="llama3.2"
)

# Initialize planner
planner = OllamaLearningPlanner(ollama_client=ollama_client)

# Use it
question1 = planner.get_background_question()
print(question1)

plan = planner.generate_learning_plan(
    background="Tech",
    focus_goal="Frontend",
    time="10 minutes"
)
print(plan)
```

### API Server Example

```bash
# Start the FastAPI server with Ollama
python3 api_ollama_example.py

# Or with uvicorn
uvicorn api_ollama_example:app --reload
```

Then visit: http://localhost:8000/docs

## Model Selection Guide

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llama3.2** | 3GB | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | **Recommended - Best balance** |
| llama3.1 | 4.7GB | ⚡⚡ Medium | ⭐⭐⭐⭐ Great | Better quality, slower |
| mistral | 4.1GB | ⚡⚡ Medium | ⭐⭐⭐ Good | Code generation |
| qwen2.5 | 4.7GB | ⚡⚡ Medium | ⭐⭐⭐⭐ Great | Multilingual support |
| phi3 | 2.3GB | ⚡⚡⚡⚡ Very Fast | ⭐⭐ OK | Testing, limited resources |

### Change Model

Edit `api_ollama_example.py`:

```python
ollama_client = OllamaClient(
    model="mistral"  # Change to your preferred model
)
```

## Configuration

### Change Ollama URL

If running Ollama on a different machine:

```python
ollama_client = OllamaClient(
    base_url="http://192.168.1.100:11434",  # Remote Ollama server
    model="llama3.2"
)
```

### Adjust Temperature

For more creative (less deterministic) responses:

```python
# In ollama_planner.py, _call_llm method:
response_text = self.ollama_client.generate(
    prompt=prompt,
    system=self.system_prompt,
    temperature=0.3  # 0 = deterministic, 1 = creative
)
```

## Common Issues

### Issue: "Could not connect to Ollama"

**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, verify:
curl http://localhost:11434/api/version
```

### Issue: "Model not found"

**Solution:**
```bash
# Pull the model first
ollama pull llama3.2

# List available models
ollama list
```

### Issue: Slow generation

**Solutions:**
1. Use a smaller model (phi3, llama3.2)
2. Reduce max tokens
3. Use GPU acceleration (automatic if available)

### Issue: JSON parsing errors

**Solution:** The system has built-in failsafes that:
1. Remove markdown code blocks
2. Extract JSON from mixed text
3. Retry with better prompts

If still failing, try a better model (llama3.1, qwen2.5).

### Issue: Out of memory

**Solutions:**
1. Use smaller model: `ollama pull phi3`
2. Close other applications
3. Restart Ollama: `ollama serve`

## Performance Comparison

### Anthropic Claude (Paid API)
- ✅ Best quality
- ✅ Fast API calls
- ❌ Costs money (~$0.005/request)
- ❌ Requires internet
- ❌ Data sent to cloud

### Ollama (Free, Local)
- ✅ Free forever
- ✅ Private (data stays local)
- ✅ Works offline
- ⚡ Slower (30-60 seconds for plan generation)
- ⚠️ Quality depends on model

## Optimization Tips

### 1. Cache Questions (Save Time)

Steps 1-3 rarely change, so cache them:

```python
# Cache in memory or Redis
CACHED_QUESTIONS = {
    "step1": planner.get_background_question(),
    "step3": planner.get_time_question()
}

# Use cached version
question1 = CACHED_QUESTIONS["step1"]
```

### 2. Use Background Processing

For plan generation (slow operation):

```python
from fastapi import BackgroundTasks

@app.post("/api/onboarding/generate-plan")
async def generate_plan_async(request: Step4Request, background_tasks: BackgroundTasks):
    job_id = create_job_id()

    # Generate plan in background
    background_tasks.add_task(
        generate_and_cache_plan,
        job_id,
        request.background,
        request.focus_goal,
        request.time
    )

    return {"job_id": job_id, "status": "processing"}
```

### 3. Pre-pull Models

Before deploying:

```bash
# Pull all models you might use
ollama pull llama3.2
ollama pull llama3.1
ollama pull mistral
```

### 4. Run Ollama as Service

#### Linux (systemd)
```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

#### macOS (launchd)
Ollama auto-starts after installation.

#### Windows
Configure as Windows Service.

## Testing

### Test Ollama Connection

```bash
curl http://localhost:11434/api/version
```

Expected output:
```json
{"version":"0.x.x"}
```

### Test Model

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Say hello",
  "stream": false
}'
```

### Test Learning Planner

```bash
python3 ollama_planner.py
```

Expected: See all 4 steps complete successfully.

### Test API

```bash
# Start API
python3 api_ollama_example.py

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/onboarding/step1
```

## Production Deployment

### Docker Setup

```dockerfile
FROM python:3.10-slim

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy your app
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Pull model
RUN ollama pull llama3.2

# Run both Ollama and API
CMD ollama serve & sleep 5 && python3 api_ollama_example.py
```

### Environment Variables

```bash
# .env file
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

```python
# In code
import os

ollama_client = OllamaClient(
    base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
    model=os.getenv("OLLAMA_MODEL", "llama3.2")
)
```

## Cost Comparison

### Ollama (Free)
- Setup: $0
- Per request: $0
- Monthly (1000 users): $0
- **Total: $0**

### Anthropic Claude (Paid)
- Setup: $0
- Per request: ~$0.005
- Monthly (1000 users, 4 requests each): ~$20
- **Total: ~$20/month**

### OpenAI GPT-4 (Paid)
- Setup: $0
- Per request: ~$0.01
- Monthly (1000 users, 4 requests each): ~$40
- **Total: ~$40/month**

## Migration Path

Start with Ollama for development, upgrade to paid API for production:

1. **Development:** Use Ollama (free)
2. **MVP/Testing:** Use Ollama (free)
3. **Production (< 1000 users):** Continue with Ollama
4. **Production (> 1000 users):** Consider Anthropic/OpenAI for:
   - Better quality
   - Faster responses
   - Less server resources

## Support

### Ollama Documentation
- Website: https://ollama.com
- GitHub: https://github.com/ollama/ollama
- Models: https://ollama.com/library

### Troubleshooting
1. Check Ollama is running: `curl http://localhost:11434/api/version`
2. Check model is installed: `ollama list`
3. Check logs: `ollama logs`
4. Restart Ollama: `pkill ollama && ollama serve`

### Community
- Discord: https://discord.gg/ollama
- GitHub Issues: https://github.com/ollama/ollama/issues

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull a model (`ollama pull llama3.2`)
3. ✅ Test the planner (`python3 ollama_planner.py`)
4. ✅ Start the API (`python3 api_ollama_example.py`)
5. ✅ Integrate with your frontend
6. ✅ Deploy to production

---

**You're all set!** You now have a completely free, local LLM-powered learning planner with zero API costs.
