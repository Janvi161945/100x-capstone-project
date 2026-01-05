# 🚀 AI Learning Planner - Start Here!

Complete setup guide to get your free, local AI learning planner with **progress tracking** running in 5 minutes.

## What You're Building

A complete web app that creates personalized 7-day AI learning plans using **Ollama** (free, local LLM) **with progress tracking!**

```
User fills onboarding form (4 steps)
         ↓
Ollama generates personalized plan
         ↓
Interactive learning tracker
         ↓
Track progress day-by-day
         ↓
Celebrate completion! 🎉
```
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
cd ~/capstone-project
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

**Option A: Automatic (Recommended) ⭐**
```bash
./start_app.sh
and open http://localhost:3000 in browser
```
This starts everything automatically!

***Option B: Manual***

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

## 🎯 Test the Complete Flow (Updated!)

### Onboarding (4 Steps)
1. **Select Background:** Choose "Tech", "Product", "Design", or "Non-tech"
2. **Select Focus:** Based on your background (e.g., "Frontend" for Tech)
3. **Select Time:** Choose "5 minutes", "10 minutes", or "20 minutes"
4. **Wait:** Plan generation takes 30-60 seconds (this is normal!)

### Learning Tracker (NEW!)
5. **View Plan Preview:** See your personalized 7-day plan
6. **Start Learning Journey:** Click "Start Learning Journey →" button
7. **Track Progress:** You'll see the tracker page with:
   - Progress overview (days completed, current day, remaining)
   - Visual progress bar
   - All 7 days displayed as interactive cards
8. **Mark Complete:** Click "Mark as Complete" as you finish each day
9. **Celebrate:** Get a celebration screen when you finish all 7 days! 🎉

## 📁 Project Structure

```
/home/janvi/capstone-project/
│
├── 🚀 Quick Start Scripts
│   ├── start_app.sh              # ONE-CLICK START!
│   ├── stop_app.sh               # One-click stop
│   └── START_HERE.md             # This file
│
├── 🔧 Core System
│   ├── ollama_planner.py         # Ollama orchestrator
│   ├── api_ollama_example.py     # FastAPI server (with CORS)
│   ├── prompt_templates.py       # Prompt templates (updated!)
│   ├── llm_response_schemas.py   # Validation schemas
│   └── llm_system_prompt.md      # System prompt
│
├── 🧪 Testing
│   ├── test_ollama.py            # Setup verification
│   └── test_planner.py           # Schema tests
│
├── 🎨 Frontend (Updated!)
│   ├── index.html                # Onboarding wizard
│   ├── tracker.html              # Learning tracker (NEW!)
│   ├── README.md                 # Frontend docs
│   └── UPDATES.md                # Latest changes (NEW!)
│
├── 📖 Documentation
│   ├── START_HERE.md             # This file (updated!)
│   ├── README_OLLAMA.md          # Main README
│   ├── OLLAMA_QUICKSTART.md      # Quick start
│   ├── OLLAMA_SETUP.md           # Detailed setup
│   ├── OLLAMA_VS_ANTHROPIC.md    # Comparison guide
│   └── ARCHITECTURE.md           # System architecture
│
└── ⚙️ Configuration
    └── requirements.txt           # Python dependencies
```

## 🖥️ Your Terminals at a Glance

### Automatic (Easy!)
```bash
./start_app.sh  # Starts everything
```

### Manual (4 terminals)
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
- [ ] Tracker accessible: Open `http://localhost:3000/tracker.html`

## 🌟 User Experience Flow

```
┌─────────────────────────────────┐
│   1. Onboarding (4 steps)       │
│   Choose background, focus, time│
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   2. Plan Generation (30-60s)   │
│   Ollama creates your plan      │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   3. Plan Preview               │
│   See all 7 days                │
│   [Start Learning Journey →]    │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   4. Learning Tracker           │
│   ┌─────────────────────────┐   │
│   │ Progress: 2/7 (29%)     │   │
│   └─────────────────────────┘   │
│   Day 1: ✓ Completed           │
│   Day 2: ✓ Completed           │
│   Day 3: [Start This Day]      │ ← Current
│   Day 4: [Mark as Complete]    │
│   ...                           │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│   5. Celebration! 🎉            │
│   All 7 days completed!         │
│   [Start New Plan]              │
└─────────────────────────────────┘
```


## 💬 Support

**If you get stuck:**

1. Run diagnostics: `python3 test_ollama.py`
2. Check API health: `curl http://localhost:8000/health`
3. Check Ollama: `curl http://localhost:11434/api/version`
4. Check browser console: Press F12 in browser
5. Read detailed guides in documentation folder
6. Check `frontend/UPDATES.md` for latest changes

## 🎯 Common Commands

```bash
# Quick start everything
./start_app.sh

# Quick stop everything
./stop_app.sh

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

# Test plan generation
curl -X POST http://localhost:8000/api/onboarding/generate-plan \
  -H "Content-Type: application/json" \
  -d '{"background":"Tech","focus_goal":"Frontend","time":"10 minutes"}'

# Check what's using port 8000
lsof -i :8000

# Clear browser storage (resets progress)
# Browser Console: localStorage.clear()
```

## 🎮 Try These Flows

### Flow 1: Complete Journey
1. Create plan → 2. Start tracker → 3. Complete Day 1 → 4. Close browser
5. Reopen tracker → 6. Progress still there! ✅

### Flow 2: Different Backgrounds
- Try "Tech" → "Frontend"
- Try "Non-tech" → "Personal development"
- Try "Product" → "Product Management"
- Try "Design" → "UI/UX"

### Flow 3: Completion
1. Create plan
2. Mark all 7 days as complete (one by one)
3. See celebration screen! 🎉

---

**Ready to go?** Open `http://localhost:3000` and start your learning journey! 🚀

**Need help?** Check the documentation files or run `python3 test_ollama.py` for diagnostics.

**Track your progress:** Visit `http://localhost:3000/tracker.html` anytime!
