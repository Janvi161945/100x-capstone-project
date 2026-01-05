# 🚀 AI Learning Planner - Start Here!

Complete setup guide to get your free, local AI learning planner running in 5 minutes.

## What You're Building

A web app that creates personalized 7-day AI learning plans using **Ollama** (free, local LLM).

```
User fills onboarding form (4 steps)
         ↓
Ollama generates personalized plan
         ↓
Beautiful UI displays 7-day plan
```

**Cost:** $0 (completely free!)

## 📋 Prerequisites

- Python 3.8+
- 8GB+ RAM
- 5GB+ disk space
- Modern web browser

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Ollama (2 minutes)

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from: https://ollama.com/download/windows

**Verify:**
```bash
ollama --version
```

### Step 2: Setup Ollama (2 minutes)

**Terminal 1: Start Ollama server**
```bash
ollama serve
```
Keep this running! You should see:
```
Ollama is running on http://localhost:11434
```

**Terminal 2: Pull the model**
```bash
ollama pull llama3.2
```
Wait for download (~3GB). You should see:
```
✓ llama3.2 downloaded successfully
```

### Step 3: Install Python Dependencies (30 seconds)

```bash
cd /home/janvi/capstone-project
pip install requests pydantic fastapi uvicorn
```

### Step 4: Test Setup (30 seconds)

```bash
python3 test_ollama.py
```

You should see all tests pass:
```
✅ PASS - Ollama Connection
✅ PASS - Model Availability
✅ PASS - Simple Generation
✅ PASS - Planner Import
✅ PASS - Basic Planner
```

### Step 5: Start the Application (1 minute)

**Terminal 3: Start the API server**
```bash
python3 api_ollama_example.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 4: Start the frontend**
```bash
cd frontend
python3 -m http.server 3000
```

You should see:
```
Serving HTTP on 0.0.0.0 port 3000
```

### Step 6: Open Your Browser

Visit: **http://localhost:3000**

You should see the AI Learning Planner interface! 🎉

## 🎯 Test the Complete Flow

1. **Select Background:** Choose "Tech"
2. **Select Role:** Choose "Frontend"
3. **Select Time:** Choose "10 minutes"
4. **Wait:** Plan generation takes 30-60 seconds (this is normal!)
5. **View Plan:** See your personalized 7-day plan!

## 📁 Project Structure

```
/home/janvi/capstone-project/
│
├── 🚀 Core System
│   ├── ollama_planner.py          # Ollama orchestrator
│   ├── api_ollama_example.py      # FastAPI server
│   ├── prompt_templates.py        # Prompt templates
│   ├── llm_response_schemas.py    # Validation schemas
│   └── llm_system_prompt.md       # System prompt
│
├── 🧪 Testing
│   ├── test_ollama.py             # Setup verification
│   └── test_planner.py            # Schema tests
│
├── 🎨 Frontend
│   ├── index.html                 # Web interface (all-in-one)
│   └── README.md                  # Frontend docs
│
├── 📖 Documentation
│   ├── START_HERE.md              # This file
│   ├── README_OLLAMA.md           # Main README
│   ├── OLLAMA_QUICKSTART.md       # Quick start
│   ├── OLLAMA_SETUP.md            # Detailed setup
│   ├── OLLAMA_VS_ANTHROPIC.md     # Comparison guide
│   └── ARCHITECTURE.md            # System architecture
│
└── ⚙️ Configuration
    └── requirements.txt            # Python dependencies
```

## 🖥️ Your Terminals at a Glance

You need 4 terminals running:

```
Terminal 1: ollama serve
Terminal 2: (free - used for commands)
Terminal 3: python3 api_ollama_example.py
Terminal 4: cd frontend && python3 -m http.server 3000
```

Then open browser: `http://localhost:3000`

## ✅ Verification Checklist

Before testing, verify:

- [ ] Ollama installed: `ollama --version`
- [ ] Ollama running: `curl http://localhost:11434/api/version`
- [ ] Model pulled: `ollama list` (should show llama3.2)
- [ ] Python deps installed: `pip list | grep pydantic`
- [ ] All tests pass: `python3 test_ollama.py`
- [ ] API running: `curl http://localhost:8000/health`
- [ ] Frontend accessible: Open `http://localhost:3000`

## 🐛 Troubleshooting

### "Could not connect to Ollama"

**Problem:** Ollama server not running

**Fix:**
```bash
# Terminal 1
ollama serve
```

### "Model not found"

**Problem:** Model not downloaded

**Fix:**
```bash
ollama pull llama3.2
```

### "Could not connect to API"

**Problem:** API server not running

**Fix:**
```bash
python3 api_ollama_example.py
```

### Frontend shows error

**Problem:** Wrong URL or API not running

**Fix:**
1. Make sure API is running on port 8000
2. Access frontend via `http://localhost:3000` (not `file://`)
3. Check browser console for errors (F12)

### Plan generation takes forever

**Expected:** 30-60 seconds with Ollama (this is normal for local LLMs)

**If > 2 minutes:**
1. Check Ollama logs in Terminal 1
2. Try restarting Ollama: `pkill ollama && ollama serve`
3. Use faster model: `ollama pull phi3`

## 🎨 Frontend Features

Your web interface includes:

✅ **Modern UI** - Beautiful gradient design
✅ **Progress Bar** - Visual step tracking
✅ **Responsive** - Works on mobile & desktop
✅ **Loading States** - Clear feedback during API calls
✅ **Error Handling** - User-friendly error messages
✅ **Plan Display** - Beautiful 7-day plan cards

## 🔄 Restart Everything

If something goes wrong, restart all services:

```bash
# Kill all processes
pkill ollama
pkill -f api_ollama
pkill -f "http.server"

# Restart in order
# Terminal 1:
ollama serve

# Terminal 3:
python3 api_ollama_example.py

# Terminal 4:
cd frontend && python3 -m http.server 3000

# Browser:
http://localhost:3000
```

## 📊 Performance Expectations

| Step | Time |
|------|------|
| Step 1 (Background) | 5-10 seconds |
| Step 2 (Follow-up) | 5-10 seconds |
| Step 3 (Time) | 5-10 seconds |
| Step 4 (Plan) | 30-60 seconds ⏱️ |

**Note:** Step 4 takes longer because Ollama generates a complete 7-day plan locally.

## 💡 Tips for Best Experience

1. **Cache Questions:** Steps 1-3 can be cached since they rarely change
2. **Patient Users:** Warn users that plan generation takes 30-60 seconds
3. **Better Model:** For better quality, use `ollama pull llama3.1` (slower but better)
4. **Faster Model:** For faster responses, use `ollama pull phi3` (faster but lower quality)

## 🚀 Next Steps

After successfully testing:

1. **Customize Prompts:** Edit `prompt_templates.py`
2. **Enhance UI:** Modify `frontend/index.html`
3. **Add Features:** See `frontend/README.md` for ideas
4. **Deploy:** See deployment guides in documentation

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **START_HERE.md** | This file - quick setup |
| **README_OLLAMA.md** | Complete system documentation |
| **OLLAMA_QUICKSTART.md** | Alternative quick start |
| **OLLAMA_SETUP.md** | Detailed setup with troubleshooting |
| **OLLAMA_VS_ANTHROPIC.md** | Free vs paid comparison |
| **ARCHITECTURE.md** | System design & architecture |
| **frontend/README.md** | Frontend documentation |

## 🎉 Success!

If you can:
- ✅ See the frontend at `http://localhost:3000`
- ✅ Complete the 4-step flow
- ✅ Generate a 7-day learning plan
- ✅ See the plan displayed beautifully

**Congratulations!** Your AI Learning Planner is working! 🎊

Now you have a completely free, local, privacy-focused AI learning planner with zero API costs.

## 💬 Support

**If you get stuck:**

1. Run diagnostics: `python3 test_ollama.py`
2. Check API health: `curl http://localhost:8000/health`
3. Check Ollama: `curl http://localhost:11434/api/version`
4. Check browser console: Press F12 in browser
5. Read detailed guides in documentation folder

## 🎯 Common Commands

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Check if API is running
curl http://localhost:8000/health

# List installed models
ollama list

# Pull a different model
ollama pull mistral

# Restart Ollama
pkill ollama && ollama serve

# Test API endpoint directly
curl http://localhost:8000/api/onboarding/step1

# Check what's using port 8000
lsof -i :8000
```

---

**Ready to go?** Open `http://localhost:3000` and create your first learning plan! 🚀

**Need help?** Check the documentation files or run `python3 test_ollama.py` for diagnostics.
