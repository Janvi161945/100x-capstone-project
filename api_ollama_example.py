"""
FastAPI Example using Ollama (Free, Local LLM)
This shows how to integrate the Ollama-based learning planner with your API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import json

# Import the Ollama orchestrator
from ollama_planner import OllamaClient, OllamaLearningPlanner
from llm_response_schemas import validate_llm_response

app = FastAPI(
    title="Learning Planner API (Ollama)",
    description="Personalized AI learning planner using free, local Ollama LLM"
)

# Add CORS middleware to allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama planner globally
# You can configure the model here
ollama_client = OllamaClient(
    base_url="http://localhost:11434",
    model="llama3.2"  # Options: llama3.2, llama3.1, mistral, qwen2.5, etc.
)
planner = OllamaLearningPlanner(ollama_client=ollama_client)


# Request/Response models for API
class Step2Request(BaseModel):
    background: str


class Step4Request(BaseModel):
    background: str
    focus_goal: str
    time: str


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Learning Planner API (Ollama)",
        "llm": "Ollama (Free, Local)",
        "model": ollama_client.model,
        "endpoints": {
            "step1": "GET /api/onboarding/step1",
            "step2": "POST /api/onboarding/step2",
            "step3": "GET /api/onboarding/step3",
            "generate_plan": "POST /api/onboarding/generate-plan"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Ollama connection
        test_response = ollama_client.generate(
            prompt="Say 'ok'",
            system="Respond with exactly: ok",
            temperature=0
        )
        return {
            "status": "healthy",
            "ollama": "connected",
            "model": ollama_client.model
        }
    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Please start Ollama: ollama serve"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/onboarding/step1")
async def get_background_question() -> Dict[str, Any]:
    """
    Step 1: Get background question

    Returns:
        {
            "question_id": "background",
            "question_text": "What's your background?",
            "options": ["Tech", "Product", "Design", "Non-tech"]
        }
    """
    try:
        # Call LLM to generate question
        response = planner.get_background_question()

        # Validate response before returning
        validated = validate_llm_response("step1", response)

        return validated.model_dump()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Please start Ollama: ollama serve"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/onboarding/step2")
async def get_followup_question(request: Step2Request) -> Dict[str, Any]:
    """
    Step 2: Get dynamic follow-up question based on background

    Request body:
        {
            "background": "Tech"
        }

    Returns:
        {
            "question_id": "tech_focus",
            "question_text": "What best describes your role?",
            "options": ["Backend", "Frontend", "Data", "Mobile", "Student"]
        }
    """
    try:
        # Call LLM to generate follow-up question
        response = planner.get_followup_question(request.background)

        # Validate response
        validated = validate_llm_response("step2", response)

        return validated.model_dump()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Please start Ollama: ollama serve"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/onboarding/step3")
async def get_time_question() -> Dict[str, Any]:
    """
    Step 3: Get time commitment question

    Returns:
        {
            "question_id": "time_commitment",
            "question_text": "How much time can you spend daily?",
            "options": ["5 minutes", "10 minutes", "20 minutes"]
        }
    """
    try:
        # Call LLM to generate question
        response = planner.get_time_question()

        # Validate response
        validated = validate_llm_response("step3", response)

        return validated.model_dump()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Please start Ollama: ollama serve"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/onboarding/generate-plan")
async def generate_learning_plan(request: Step4Request) -> Dict[str, Any]:
    """
    Step 4: Generate personalized 7-day learning plan

    Request body:
        {
            "background": "Tech",
            "focus_goal": "Frontend",
            "time": "10 minutes"
        }

    Returns:
        {
            "plan": [
                {
                    "day": 1,
                    "title": "What is AI?",
                    "what_to_learn": "Understand what AI means...",
                    "what_to_do": "Write 3 examples...",
                    "time_required": "10 minutes"
                },
                ...
            ]
        }
    """
    try:
        # Call LLM to generate learning plan
        response = planner.generate_learning_plan(
            request.background,
            request.focus_goal,
            request.time
        )

        # Validate response
        validated = validate_llm_response("step4", response)

        return validated.model_dump()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Please start Ollama: ollama serve"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("Starting Learning Planner API with Ollama")
    print("=" * 60)
    print(f"Model: {ollama_client.model}")
    print(f"Ollama URL: {ollama_client.base_url}")
    print()
    print("Make sure Ollama is running:")
    print("  1. ollama serve")
    print(f"  2. ollama pull {ollama_client.model}")
    print()
    print("API will be available at: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print("=" * 60)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8000)
