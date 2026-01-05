# LLM Learning Planner - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Step 1  │→ │  Step 2  │→ │  Step 3  │→ │  Step 4  │   │
│  │Background│  │ Follow-up│  │   Time   │  │   Plan   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       ↓              ↓              ↓              ↓        │
└───────┼──────────────┼──────────────┼──────────────┼────────┘
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                            │
                    HTTP Requests (JSON)
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       API LAYER                             │
│                                                             │
│  GET  /api/onboarding/step1                                │
│  POST /api/onboarding/step2                                │
│  GET  /api/onboarding/step3                                │
│  POST /api/onboarding/generate-plan                        │
│                                                             │
│  (You control this - FastAPI, Express, etc.)               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    Calls orchestrator
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              LLM ORCHESTRATOR                               │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │  class LearningPlannerOrchestrator                 │    │
│  │                                                     │    │
│  │  - get_background_question()                       │    │
│  │  - get_followup_question(background)               │    │
│  │  - get_time_question()                             │    │
│  │  - generate_learning_plan(bg, goal, time)          │    │
│  └────────────────────────────────────────────────────┘    │
│                            │                                │
│                   Uses prompt templates                     │
│                            ↓                                │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Prompt Templates (prompt_templates.py)            │    │
│  │                                                     │    │
│  │  - get_step1_prompt()                              │    │
│  │  - get_step2_prompt(background)                    │    │
│  │  - get_step3_prompt()                              │    │
│  │  - get_step4_prompt(bg, goal, time)                │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    Structured prompts
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    LLM (CLAUDE)                             │
│                                                             │
│  System Prompt: "You are a structured data generator..."   │
│                                                             │
│  User Prompt: "Generate question for Tech background..."   │
│                                                             │
│  Temperature: 0 (deterministic)                            │
│  Max Tokens: 2000                                           │
│                                                             │
│  Output: Raw JSON only (no chat, no markdown)              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                      Returns JSON
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  VALIDATION LAYER                           │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Pydantic Schemas (llm_response_schemas.py)        │    │
│  │                                                     │    │
│  │  - OnboardingQuestion                              │    │
│  │    * question_id: str                              │    │
│  │    * question_text: str                            │    │
│  │    * options: List[str] (2-6 items)                │    │
│  │                                                     │    │
│  │  - LearningTask                                    │    │
│  │    * day: int (1-7)                                │    │
│  │    * title: str                                    │    │
│  │    * what_to_learn: str                            │    │
│  │    * what_to_do: str                               │    │
│  │    * time_required: str (must contain "minute")    │    │
│  │                                                     │    │
│  │  - LearningPlan                                    │    │
│  │    * plan: List[LearningTask] (exactly 7)          │    │
│  └────────────────────────────────────────────────────┘    │
│                            │                                │
│                    Validates JSON                           │
│                            │                                │
│              ✅ Valid → Return to API                       │
│              ❌ Invalid → Raise ValidationError             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Example: Generating a Learning Plan

```
1. User completes onboarding:
   - Background: "Tech"
   - Focus: "Frontend"
   - Time: "10 minutes"

2. Frontend → API:
   POST /api/onboarding/generate-plan
   {
     "background": "Tech",
     "focus_goal": "Frontend",
     "time": "10 minutes"
   }

3. API → Orchestrator:
   orchestrator.generate_learning_plan(
     background="Tech",
     focus_goal="Frontend",
     time="10 minutes"
   )

4. Orchestrator → Prompt Template:
   prompt = get_step4_prompt("Tech", "Frontend", "10 minutes")

5. Prompt Template → Structured Prompt:
   """
   User profile:
   - Background: Tech
   - Focus/Goal: Frontend
   - Time per day: 10 minutes

   Generate a 7-day personalized AI learning plan.

   Rules:
   - Exactly 7 days
   - One task per day
   - Tasks must fit within 10 minutes
   - Beginner-friendly language
   - Actionable tasks

   Output schema: {...}

   Return JSON only.
   """

6. Orchestrator → LLM:
   llm_client.messages.create(
     model="claude-sonnet-4",
     temperature=0,
     system="You are a structured data generator...",
     messages=[{"role": "user", "content": prompt}]
   )

7. LLM → Raw Response:
   {
     "plan": [
       {
         "day": 1,
         "title": "What is AI?",
         "what_to_learn": "...",
         "what_to_do": "...",
         "time_required": "10 minutes"
       },
       ...
     ]
   }

8. Orchestrator → Validation:
   validate_llm_response("step4", response)

9. Validation → Check:
   ✓ Has exactly 7 days
   ✓ Each day has all required fields
   ✓ time_required contains "minute"
   ✓ Days are numbered 1-7

10. Orchestrator → API:
    return validated_plan.model_dump()

11. API → Frontend:
    {
      "plan": [...]
    }

12. Frontend → Display:
    User sees their personalized 7-day plan
```

## Component Responsibilities

### 1. Frontend (Your Code)
**Responsibility:** User interface and user experience

**Does:**
- Display questions with options
- Collect user selections
- Show loading states
- Display generated plan
- Handle errors gracefully

**Does NOT:**
- Talk directly to LLM
- Generate questions
- Create learning content

### 2. API Layer (Your Code)
**Responsibility:** HTTP interface and business logic

**Does:**
- Expose REST endpoints
- Validate request payloads
- Call orchestrator methods
- Handle errors and retries
- Log requests/responses
- Implement rate limiting
- Cache common responses

**Does NOT:**
- Know about LLM prompts
- Generate questions or plans
- Parse LLM responses

### 3. Orchestrator (This System)
**Responsibility:** LLM interaction and coordination

**Does:**
- Construct structured prompts
- Call LLM with correct parameters
- Parse LLM responses
- Validate responses against schemas
- Handle markdown code block cleanup
- Return typed data

**Does NOT:**
- Handle HTTP requests
- Store data in database
- Manage user sessions

### 4. Prompt Templates (This System)
**Responsibility:** Prompt generation

**Does:**
- Generate step-specific prompts
- Adapt prompts based on user input
- Include schema definitions
- Enforce JSON-only output

**Does NOT:**
- Call the LLM
- Validate responses
- Handle errors

### 5. LLM (Claude API)
**Responsibility:** Content generation

**Does:**
- Generate questions based on context
- Create personalized learning plans
- Return structured JSON
- Follow system prompt instructions

**Does NOT:**
- Store user data
- Remember previous conversations
- Chat freely
- Add commentary

### 6. Validation Layer (This System)
**Responsibility:** Response validation

**Does:**
- Define expected schemas
- Validate LLM responses
- Enforce data constraints
- Provide clear error messages

**Does NOT:**
- Generate data
- Fix invalid responses
- Call the LLM

## Design Principles

### 1. Separation of Concerns
Each component has a single, well-defined responsibility.

### 2. Deterministic Output
Temperature = 0 ensures consistent results for testing and reliability.

### 3. Type Safety
Pydantic schemas ensure all data is validated and typed.

### 4. Fail Fast
Invalid responses are caught immediately, not passed to users.

### 5. Testability
Each component can be tested independently:
- Mock LLM → test orchestrator
- Mock orchestrator → test API
- Mock API → test frontend

### 6. Observability
Every layer can log, monitor, and debug independently.

## Error Handling Flow

```
Error Source → Detection → Handling → User Experience

LLM returns invalid JSON
  → Orchestrator catches JSONDecodeError
  → API returns 500 error
  → Frontend shows "Something went wrong, please try again"

LLM returns wrong schema
  → Validation layer catches ValidationError
  → API logs error and returns 500
  → Frontend shows "Something went wrong, please try again"

LLM times out
  → Orchestrator catches timeout
  → API retries with exponential backoff
  → If still failing, return 503
  → Frontend shows "Service temporarily unavailable"

Invalid user input
  → API validation catches error
  → API returns 400 error
  → Frontend shows "Please select an option"
```

## Scalability Considerations

### Caching Strategy
```
┌──────────────────────────────────────────────────┐
│ Question 1 (Background)                          │
│ → Cache: Forever (never changes)                 │
│ → Key: "question:step1"                          │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Question 2 (Follow-up)                           │
│ → Cache: 24 hours (rarely changes)               │
│ → Key: "question:step2:{background}"             │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Question 3 (Time)                                │
│ → Cache: Forever (never changes)                 │
│ → Key: "question:step3"                          │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Learning Plan                                    │
│ → Cache: 1 hour (can change)                     │
│ → Key: "plan:{background}:{goal}:{time}"         │
└──────────────────────────────────────────────────┘
```

### Rate Limiting
```
User → API Gateway → Rate Limit (10 req/min/user)
                  → If exceeded: Return 429
                  → Else: Call orchestrator
```

### Async Processing
```
For expensive operations (plan generation):

User → Submit request
    → API returns job ID immediately
    → Background worker calls LLM
    → Stores result in cache
    → User polls for completion
```

## Security Considerations

1. **API Key Management**
   - Store in environment variables
   - Rotate regularly
   - Never commit to git

2. **Input Validation**
   - Validate all user inputs
   - Sanitize before passing to LLM
   - Limit input lengths

3. **Output Sanitization**
   - Parse JSON safely
   - Validate against schema
   - Don't execute code from LLM

4. **Rate Limiting**
   - Prevent abuse
   - Protect API costs
   - User-based limits

## Monitoring

```
Metrics to Track:
├── API Layer
│   ├── Request count
│   ├── Response time
│   ├── Error rate
│   └── Cache hit rate
│
├── LLM Layer
│   ├── Token usage
│   ├── Request count
│   ├── Latency
│   ├── Error rate
│   └── Cost per request
│
└── Validation Layer
    ├── Validation failures
    ├── Schema violations
    └── Retry attempts
```

## Development Workflow

```
1. Local Development
   ├── Use .env file for API key
   ├── Run orchestrator tests
   ├── Run API tests
   └── Test with frontend

2. Staging
   ├── Deploy API + orchestrator
   ├── Use staging API key
   ├── Test full workflow
   └── Monitor logs

3. Production
   ├── Deploy with proper API key
   ├── Enable caching
   ├── Set up monitoring
   ├── Enable rate limiting
   └── Monitor costs
```

This architecture ensures:
- ✅ Clear separation of concerns
- ✅ Easy testing and debugging
- ✅ Scalable and maintainable
- ✅ Type-safe and validated
- ✅ Deterministic behavior
