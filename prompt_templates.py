"""
Prompt templates for the Learning Planner LLM
Each function returns a structured prompt that enforces JSON-only output
"""

def get_step1_prompt():
    """Step 1: Ask background question"""
    return """Generate the initial onboarding question.

Output schema:
{
  "question_id": "background",
  "question_text": "What's your background?",
  "options": ["Tech", "Product", "Design", "Non-tech"]
}

Return JSON only."""


def get_step2_prompt(background: str):
    """Step 2: Dynamic follow-up based on background"""
    prompts = {
        "Tech": """User background: Tech

Generate the next question to understand their technical role.

Output schema:
{
  "question_id": "string",
  "question_text": "string",
  "options": ["option1", "option2", ...]
}

Return JSON only.""",

        "Product": """User background: Product

Generate the next question to understand their product focus.

Output schema:
{
  "question_id": "string",
  "question_text": "string",
  "options": ["option1", "option2", ...]
}

Return JSON only.""",

        "Design": """User background: Design

Generate the next question to understand their design discipline.

Output schema:
{
  "question_id": "string",
  "question_text": "string",
  "options": ["option1", "option2", ...]
}

Return JSON only.""",

        "Non-tech": """User background: Non-tech

Generate the next question to understand why they want to learn AI.

IMPORTANT: Do NOT include "Others" or "Please specify" options. Only include specific, clear choices.

Output schema:
{
  "question_id": "nontech_goal",
  "question_text": "Why do you want to learn AI?",
  "options": ["Career growth", "Curiosity", "Work efficiency", "Business idea", "Personal development", "Stay current with technology"]
}

Return JSON only."""
    }

    return prompts.get(background, prompts["Non-tech"])


def get_step3_prompt():
    """Step 3: Ask time commitment"""
    return """Generate the time commitment question.

Output schema:
{
  "question_id": "time_commitment",
  "question_text": "How much time can you spend daily?",
  "options": ["5 minutes", "10 minutes", "20 minutes"]
}

Return JSON only."""


def get_step4_prompt(background: str, focus_goal: str, time: str):
    """Step 4: Generate learning plan"""
    return f"""Create a 7-day AI learning plan for this user:
- Background: {background}
- Focus/Goal: {focus_goal}
- Time per day: {time}

CRITICAL: You MUST generate EXACTLY 7 days (day 1 through day 7). No more, no less.

Requirements for each day:
- Beginner-friendly explanations
- Tasks that fit within {time}
- Actionable exercises

Output MUST be valid JSON with this EXACT structure:
{{
  "plan": [
    {{
      "day": 1,
      "title": "Day 1 Title",
      "what_to_learn": "Brief explanation of the concept",
      "what_to_do": "Specific actionable task",
      "time_required": "{time}"
    }},
    {{
      "day": 2,
      "title": "Day 2 Title",
      "what_to_learn": "Brief explanation of the concept",
      "what_to_do": "Specific actionable task",
      "time_required": "{time}"
    }},
    {{
      "day": 3,
      "title": "Day 3 Title",
      "what_to_learn": "Brief explanation of the concept",
      "what_to_do": "Specific actionable task",
      "time_required": "{time}"
    }},
    {{
      "day": 4,
      "title": "Day 4 Title",
      "what_to_learn": "Brief explanation of the concept",
      "what_to_do": "Specific actionable task",
      "time_required": "{time}"
    }},
    {{
      "day": 5,
      "title": "Day 5 Title",
      "what_to_learn": "Brief explanation of the concept",
      "what_to_do": "Specific actionable task",
      "time_required": "{time}"
    }},
    {{
      "day": 6,
      "title": "Day 6 Title",
      "what_to_learn": "Brief explanation of the concept",
      "what_to_do": "Specific actionable task",
      "time_required": "{time}"
    }},
    {{
      "day": 7,
      "title": "Day 7 Title",
      "what_to_learn": "Brief explanation of the concept",
      "what_to_do": "Specific actionable task",
      "time_required": "{time}"
    }}
  ]
}}

Return ONLY the JSON. No explanations. ALL 7 days required."""


# Alternative: More specific follow-up questions by background
FOLLOW_UP_QUESTIONS = {
    "Tech": {
        "question_id": "tech_focus",
        "question_text": "What best describes your role?",
        "options": ["Backend", "Frontend", "Data", "Mobile", "DevOps", "Student"]
    },
    "Product": {
        "question_id": "product_focus",
        "question_text": "What area are you focused on?",
        "options": ["Product Management", "Product Design", "Product Strategy", "Product Analytics"]
    },
    "Design": {
        "question_id": "design_focus",
        "question_text": "What's your design discipline?",
        "options": ["UI/UX", "Visual Design", "Design Research", "Prototyping"]
    },
    "Non-tech": {
        "question_id": "nontech_goal",
        "question_text": "Why do you want to learn AI?",
        "options": ["Career growth", "Curiosity", "Work efficiency", "Business idea", "Personal development", "Stay current with technology"]
    }
}
