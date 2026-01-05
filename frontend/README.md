# Frontend - AI Learning Planner

A simple, modern web interface to test the Ollama-based learning planner.

## Features

✅ Clean, modern UI with gradient background
✅ 4-step onboarding flow with progress tracking
✅ Responsive design (works on mobile & desktop)
✅ Real-time API integration
✅ Beautiful learning plan display
✅ Error handling and loading states

## Quick Start

### 1. Start the API Server

```bash
# Make sure Ollama is running
ollama serve

# In another terminal, start the API
cd /home/janvi/capstone-project
python3 api_ollama_example.py
```

The API should be running at: `http://localhost:8000`

### 2. Open the Frontend

Simply open the HTML file in your browser:

**Option A: Direct file open**
```bash
# Open in default browser
xdg-open /home/janvi/capstone-project/frontend/index.html

# Or manually navigate to:
file:///home/janvi/capstone-project/frontend/index.html
```

**Option B: Simple HTTP server (recommended)**
```bash
cd /home/janvi/capstone-project/frontend
python3 -m http.server 3000
```

Then visit: `http://localhost:3000`

### 3. Test the Flow

1. **Step 1:** Select your background (Tech/Product/Design/Non-tech)
2. **Step 2:** Select your focus area (adapts based on step 1)
3. **Step 3:** Select daily time commitment (5/10/20 minutes)
4. **Step 4:** Wait 30-60 seconds while your personalized plan generates
5. **View Plan:** See your 7-day learning plan!

## Screenshots

### Step 1: Background Question
```
┌─────────────────────────────────────┐
│      AI Learning Planner            │
│  Get your personalized 7-day plan   │
│                                     │
│  Progress: [●]─[○]─[○]─[○]          │
│                                     │
│  What's your background?            │
│                                     │
│  [ Tech                          ]  │
│  [ Product                       ]  │
│  [ Design                        ]  │
│  [ Non-tech                      ]  │
│                                     │
│                    [Next →]         │
└─────────────────────────────────────┘
```

### Step 4: Learning Plan
```
┌─────────────────────────────────────┐
│  ✅ Your Plan is Ready!              │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [1] What is AI?             │   │
│  │ Learn: AI basics...         │   │
│  │ Do: Write 3 examples...     │   │
│  │ ⏱️ 10 minutes               │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [2] AI in Frontend...       │   │
│  │ ...                         │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Create Another Plan]              │
└─────────────────────────────────────┘
```

## File Structure

```
frontend/
├── index.html          # Main HTML file (everything in one file)
└── README.md           # This file
```

**Note:** All CSS and JavaScript are embedded in `index.html` for simplicity. No external dependencies needed!

## How It Works

### API Integration

The frontend calls these endpoints:

1. **GET** `/api/onboarding/step1`
   - Gets background question
   - Response: `{question_id, question_text, options}`

2. **POST** `/api/onboarding/step2`
   - Body: `{background: "Tech"}`
   - Gets follow-up question
   - Response: `{question_id, question_text, options}`

3. **GET** `/api/onboarding/step3`
   - Gets time commitment question
   - Response: `{question_id, question_text, options}`

4. **POST** `/api/onboarding/generate-plan`
   - Body: `{background, focus_goal, time}`
   - Generates learning plan (30-60 seconds)
   - Response: `{plan: [{day, title, what_to_learn, what_to_do, time_required}, ...]}`

### State Management

```javascript
let currentStep = 1;
let answers = {
    background: null,
    focus: null,
    time: null
};
```

Simple state tracking - no framework needed!

## Customization

### Change Colors

Edit the CSS in `index.html`:

```css
/* Line 15: Main gradient background */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Line 116: Primary button color */
.btn-primary {
    background: #667eea;  /* Change this */
}
```

### Change API URL

Edit the JavaScript in `index.html`:

```javascript
// Line 289
const API_URL = 'http://localhost:8000';  // Change this
```

### Add Logo

Add an image above the header:

```html
<div class="header">
    <img src="logo.png" alt="Logo" style="width: 80px; margin-bottom: 20px;">
    <h1>AI Learning Planner</h1>
    ...
</div>
```

## Troubleshooting

### "Could not connect to server"

**Problem:** Frontend can't reach the API

**Solutions:**
1. Make sure API is running: `python3 api_ollama_example.py`
2. Check API is on port 8000: `curl http://localhost:8000/health`
3. Check browser console for CORS errors
4. Try using the HTTP server method instead of direct file open

### CORS Errors

**Problem:** Browser blocks API requests

**Solution:** Use the HTTP server method:
```bash
cd frontend
python3 -m http.server 3000
```
Then visit `http://localhost:3000` instead of `file://`

### Slow Plan Generation

**Problem:** Step 4 takes too long

**Expected:** 30-60 seconds with Ollama (this is normal)

**Solutions:**
1. Use a faster model: `ollama pull phi3`
2. Wait patiently - local LLMs are slower than cloud APIs
3. The loading message tells users to wait

### Questions Look Wrong

**Problem:** LLM returns unexpected format

**Solution:**
1. Check API logs for errors
2. Verify Ollama is running: `ollama list`
3. Test API directly: `curl http://localhost:8000/api/onboarding/step1`
4. Try regenerating with a better model: `ollama pull llama3.1`

## Browser Compatibility

✅ Chrome/Edge (recommended)
✅ Firefox
✅ Safari
✅ Mobile browsers

**No external dependencies** - works everywhere!

## Features Breakdown

### UI Components

- **Progress Bar** - Shows current step (1-4)
- **Step Indicators** - Visual feedback (○ = pending, ● = active, ✓ = completed)
- **Option Cards** - Click to select, hover effects
- **Loading Spinner** - Shows during API calls
- **Error Messages** - Auto-hide after 5 seconds
- **Day Cards** - Beautiful plan display

### UX Features

- **Disabled State** - Next button disabled until selection
- **Back Navigation** - Go back to previous steps
- **Responsive** - Works on mobile and desktop
- **Animations** - Smooth transitions and hover effects
- **Auto-scroll** - Smooth scrolling through plan

### Error Handling

- API connection errors
- Request timeouts
- Invalid responses
- User-friendly error messages

## Performance

- **Load Time:** < 100ms (single HTML file)
- **API Calls:** 4 total (one per step)
- **Bundle Size:** ~13KB (no external dependencies)
- **Mobile:** Fully responsive

## Next Steps

### Enhancements You Could Add

1. **Save Plans** - Store plans in localStorage
2. **Share Plans** - Generate shareable links
3. **Print Plans** - Add print stylesheet
4. **Dark Mode** - Toggle dark/light theme
5. **Animations** - Add more micro-interactions
6. **Analytics** - Track user behavior
7. **Multiple Languages** - i18n support

### Integration

To integrate with a real app:

1. Extract CSS to `styles.css`
2. Extract JS to `app.js`
3. Add a bundler (Vite, Webpack)
4. Add a framework (React, Vue) if needed
5. Add state management (Redux, Zustand)
6. Add routing for multi-page

But for testing, this single-file version is perfect! 🎉

## Testing Checklist

- [ ] API server is running
- [ ] Ollama is running
- [ ] Model is pulled (`ollama pull llama3.2`)
- [ ] Frontend loads without errors
- [ ] Step 1 shows background options
- [ ] Selecting an option enables Next button
- [ ] Step 2 adapts to background selection
- [ ] Step 3 shows time options
- [ ] Step 4 generates plan (wait 30-60s)
- [ ] Plan displays all 7 days correctly
- [ ] "Create Another Plan" button works

## Support

For issues:
1. Check browser console (F12)
2. Check API logs in terminal
3. Verify Ollama status: `curl http://localhost:11434/api/version`
4. Test API directly: `curl http://localhost:8000/health`

---

**Enjoy testing your AI Learning Planner!** 🚀
