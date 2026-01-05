"""
Learning Planner with Ollama (Free, Local LLM)
Uses Ollama to run models locally without API costs
"""

import json
import requests
from typing import Dict, Any, List
from prompt_templates import (
    get_step1_prompt,
    get_step2_prompt,
    get_step3_prompt,
    get_step4_prompt
)


class OllamaClient:
    """
    Simple Ollama client for interacting with locally running Ollama models.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama API base URL (default: http://localhost:11434)
            model: Model to use (default: llama3.2)
                   Options: llama3.2, llama3.1, mistral, qwen2.5, etc.
        """
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str, system: str = None, temperature: float = 0) -> str:
        """
        Generate text using Ollama.

        Args:
            prompt: User prompt
            system: System prompt (optional)
            temperature: Temperature for generation (0 = deterministic)

        Returns:
            Generated text
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
            "format": "json",  # Request JSON output
            "options": {
                "num_predict": 4096  # Allow longer responses (especially for 7-day plans)
            }
        }

        if system:
            payload["system"] = system

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Could not connect to Ollama. Make sure Ollama is running.\n"
                "Install: https://ollama.com\n"
                "Run: ollama serve"
            )
        except Exception as e:
            raise Exception(f"Ollama API error: {e}")


class OllamaLearningPlanner:
    """
    Learning Planner using Ollama (free, local LLM).
    Compatible with the same interface as LearningPlannerOrchestrator.
    """

    def __init__(self, ollama_client: OllamaClient = None):
        """
        Initialize planner with Ollama client.

        Args:
            ollama_client: OllamaClient instance (creates default if not provided)
        """
        self.ollama_client = ollama_client or OllamaClient()
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Load the system prompt that configures LLM behavior"""
        return """You are a structured learning plan generator. You do NOT engage in conversation.

Output ONLY valid JSON. No markdown, no explanations, no text outside JSON.

Follow the exact schema provided in each request."""

    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Call Ollama and parse JSON response.

        Args:
            prompt: The user prompt for this step

        Returns:
            Parsed JSON response
        """
        # Call Ollama
        response_text = self.ollama_client.generate(
            prompt=prompt,
            system=self.system_prompt,
            temperature=0  # Deterministic output
        )

        # Clean response text
        response_text = response_text.strip()

        # Remove markdown code blocks if present (failsafe)
        if response_text.startswith("```"):
            # Split by code block markers
            parts = response_text.split("```")
            if len(parts) >= 2:
                response_text = parts[1]
                # Remove "json" language identifier if present
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

        # Try to parse JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            # If parsing fails, try to extract JSON from the response
            # Sometimes LLMs add text before/after JSON
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass

            raise ValueError(
                f"Could not parse JSON from LLM response.\n"
                f"Error: {e}\n"
                f"Response: {response_text[:500]}..."
            )

    def get_background_question(self) -> Dict[str, Any]:
        """
        Step 1: Get initial background question

        Returns:
            {
                "question_id": "background",
                "question_text": "What's your background?",
                "options": ["Tech", "Product", "Design", "Non-tech"]
            }
        """
        prompt = get_step1_prompt()
        return self._call_llm(prompt)

    def get_followup_question(self, background: str) -> Dict[str, Any]:
        """
        Step 2: Get dynamic follow-up question based on background

        Args:
            background: User's background choice (Tech/Product/Design/Non-tech)

        Returns:
            {
                "question_id": "...",
                "question_text": "...",
                "options": [...]
            }
        """
        prompt = get_step2_prompt(background)
        return self._call_llm(prompt)

    def get_time_question(self) -> Dict[str, Any]:
        """
        Step 3: Get time commitment question

        Returns:
            {
                "question_id": "time_commitment",
                "question_text": "How much time can you spend daily?",
                "options": ["5 minutes", "10 minutes", "20 minutes"]
            }
        """
        prompt = get_step3_prompt()
        return self._call_llm(prompt)

    def generate_learning_plan(
        self,
        background: str,
        focus_goal: str,
        time: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Step 4: Generate personalized learning plan

        Args:
            background: User's background
            focus_goal: User's focus area or goal
            time: Daily time commitment

        Returns:
            {
                "plan": [
                    {
                        "day": 1,
                        "title": "...",
                        "what_to_learn": "...",
                        "what_to_do": "...",
                        "time_required": "..."
                    },
                    ...
                ]
            }
        """
        prompt = get_step4_prompt(background, focus_goal, time)
        return self._call_llm(prompt)


def example_usage():
    """Demonstrates how to use the Ollama planner"""
    print("=" * 60)
    print("Ollama Learning Planner - Example Usage")
    print("=" * 60)
    print()

    try:
        # Initialize Ollama client and planner
        print("Initializing Ollama client...")
        ollama_client = OllamaClient(model="llama3.2")  # or "mistral", "qwen2.5", etc.
        planner = OllamaLearningPlanner(ollama_client=ollama_client)

        print(f"✅ Connected to Ollama (model: {ollama_client.model})")
        print()

        # Step 1: Get background question
        print("Step 1: Getting background question...")
        q1 = planner.get_background_question()
        print("✅ Response:")
        print(json.dumps(q1, indent=2))
        print()

        # Simulate user selecting "Tech"
        user_background = "Tech"
        print(f"User selects: {user_background}")
        print()

        # Step 2: Get follow-up question
        print("Step 2: Getting follow-up question...")
        q2 = planner.get_followup_question(user_background)
        print("✅ Response:")
        print(json.dumps(q2, indent=2))
        print()

        # Simulate user selecting "Frontend"
        user_focus = "Frontend"
        print(f"User selects: {user_focus}")
        print()

        # Step 3: Get time commitment question
        print("Step 3: Getting time commitment question...")
        q3 = planner.get_time_question()
        print("✅ Response:")
        print(json.dumps(q3, indent=2))
        print()

        # Simulate user selecting "10 minutes"
        user_time = "10 minutes"
        print(f"User selects: {user_time}")
        print()

        # Step 4: Generate learning plan
        print("Step 4: Generating learning plan...")
        print("(This may take 30-60 seconds...)")
        plan = planner.generate_learning_plan(user_background, user_focus, user_time)
        print("✅ Response:")
        print(json.dumps(plan, indent=2))
        print()

        print("=" * 60)
        print("SUCCESS! All steps completed.")
        print("=" * 60)

    except ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print()
        print("Quick Fix:")
        print("1. Install Ollama: https://ollama.com")
        print("2. Run: ollama serve")
        print("3. Pull a model: ollama pull llama3.2")
        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    example_usage()
