"""
Test suite for the LLM Learning Planner
Demonstrates how the system works end-to-end
"""

import json
from typing import Dict, Any
from llm_response_schemas import (
    OnboardingQuestion,
    LearningPlan,
    LearningTask,
    validate_llm_response
)


def test_step1_validation():
    """Test Step 1: Background question validation"""
    print("=" * 60)
    print("TEST: Step 1 - Background Question Validation")
    print("=" * 60)

    # Valid response
    valid_response = {
        "question_id": "background",
        "question_text": "What's your background?",
        "options": ["Tech", "Product", "Design", "Non-tech"]
    }

    try:
        validated = validate_llm_response("step1", valid_response)
        print("✅ Valid response passed:")
        print(json.dumps(validated.model_dump(), indent=2))
    except Exception as e:
        print(f"❌ Validation failed: {e}")

    # Invalid response - too few options
    print("\n" + "-" * 60)
    print("Testing invalid response (too few options):")
    invalid_response = {
        "question_id": "background",
        "question_text": "What's your background?",
        "options": ["Tech"]  # Only 1 option
    }

    try:
        validated = validate_llm_response("step1", invalid_response)
        print("❌ Should have failed but didn't!")
    except Exception as e:
        print(f"✅ Expected validation error: {e}")

    print()


def test_step2_validation():
    """Test Step 2: Follow-up question validation"""
    print("=" * 60)
    print("TEST: Step 2 - Follow-up Question Validation")
    print("=" * 60)

    # Valid Tech follow-up
    valid_tech_response = {
        "question_id": "tech_focus",
        "question_text": "What best describes your role?",
        "options": ["Backend", "Frontend", "Data", "Mobile", "DevOps"]
    }

    try:
        validated = validate_llm_response("step2", valid_tech_response)
        print("✅ Valid Tech follow-up passed:")
        print(json.dumps(validated.model_dump(), indent=2))
    except Exception as e:
        print(f"❌ Validation failed: {e}")

    print()


def test_step3_validation():
    """Test Step 3: Time commitment validation"""
    print("=" * 60)
    print("TEST: Step 3 - Time Commitment Validation")
    print("=" * 60)

    valid_time_response = {
        "question_id": "time_commitment",
        "question_text": "How much time can you spend daily?",
        "options": ["5 minutes", "10 minutes", "20 minutes"]
    }

    try:
        validated = validate_llm_response("step3", valid_time_response)
        print("✅ Valid time question passed:")
        print(json.dumps(validated.model_dump(), indent=2))
    except Exception as e:
        print(f"❌ Validation failed: {e}")

    print()


def test_step4_validation():
    """Test Step 4: Learning plan validation"""
    print("=" * 60)
    print("TEST: Step 4 - Learning Plan Validation")
    print("=" * 60)

    # Valid 7-day plan
    valid_plan = {
        "plan": [
            {
                "day": i,
                "title": f"Day {i}: AI Fundamentals",
                "what_to_learn": "Learn about the basics of AI and how it applies to your field.",
                "what_to_do": "Write down 3 examples of AI you've encountered today.",
                "time_required": "10 minutes"
            }
            for i in range(1, 8)
        ]
    }

    try:
        validated = validate_llm_response("step4", valid_plan)
        print("✅ Valid 7-day plan passed:")
        print(f"Plan has {len(validated.plan)} days")
        print("\nFirst day:")
        print(json.dumps(validated.plan[0].model_dump(), indent=2))
        print("\nLast day:")
        print(json.dumps(validated.plan[-1].model_dump(), indent=2))
    except Exception as e:
        print(f"❌ Validation failed: {e}")

    # Invalid plan - only 5 days
    print("\n" + "-" * 60)
    print("Testing invalid plan (only 5 days):")
    invalid_plan = {
        "plan": [
            {
                "day": i,
                "title": f"Day {i}",
                "what_to_learn": "Learn something interesting about AI.",
                "what_to_do": "Complete a short exercise.",
                "time_required": "10 minutes"
            }
            for i in range(1, 6)  # Only 5 days
        ]
    }

    try:
        validated = validate_llm_response("step4", invalid_plan)
        print("❌ Should have failed but didn't!")
    except Exception as e:
        print(f"✅ Expected validation error: {e}")

    # Invalid plan - missing time units
    print("\n" + "-" * 60)
    print("Testing invalid plan (missing time units):")
    invalid_plan_time = {
        "plan": [
            {
                "day": i,
                "title": f"Day {i}",
                "what_to_learn": "Learn something interesting about AI.",
                "what_to_do": "Complete a short exercise.",
                "time_required": "10"  # Missing "minutes"
            }
            for i in range(1, 8)
        ]
    }

    try:
        validated = validate_llm_response("step4", invalid_plan_time)
        print("❌ Should have failed but didn't!")
    except Exception as e:
        print(f"✅ Expected validation error: {e}")

    print()


def test_full_workflow():
    """Test complete onboarding workflow"""
    print("=" * 60)
    print("TEST: Full Onboarding Workflow")
    print("=" * 60)

    workflow = {
        "step1": {
            "question_id": "background",
            "question_text": "What's your background?",
            "options": ["Tech", "Product", "Design", "Non-tech"]
        },
        "step2": {
            "question_id": "tech_focus",
            "question_text": "What best describes your role?",
            "options": ["Backend", "Frontend", "Data", "Mobile"]
        },
        "step3": {
            "question_id": "time_commitment",
            "question_text": "How much time can you spend daily?",
            "options": ["5 minutes", "10 minutes", "20 minutes"]
        },
        "step4": {
            "plan": [
                {
                    "day": 1,
                    "title": "What is AI?",
                    "what_to_learn": "Understand what AI means in simple terms and how it differs from traditional programming.",
                    "what_to_do": "Write down 3 examples where you've encountered AI in your daily life.",
                    "time_required": "10 minutes"
                },
                {
                    "day": 2,
                    "title": "AI in Frontend Development",
                    "what_to_learn": "Learn how AI tools like GitHub Copilot and ChatGPT can assist frontend developers.",
                    "what_to_do": "Try using ChatGPT to explain a React concept you find challenging.",
                    "time_required": "10 minutes"
                },
                {
                    "day": 3,
                    "title": "Prompt Engineering Basics",
                    "what_to_learn": "Understand how to write effective prompts to get better responses from AI.",
                    "what_to_do": "Write 3 different prompts for the same coding question and compare the results.",
                    "time_required": "10 minutes"
                },
                {
                    "day": 4,
                    "title": "AI Code Review",
                    "what_to_learn": "Learn how AI can help review your code and suggest improvements.",
                    "what_to_do": "Paste a recent code snippet into ChatGPT and ask for a code review.",
                    "time_required": "10 minutes"
                },
                {
                    "day": 5,
                    "title": "AI Design Tools",
                    "what_to_learn": "Explore AI-powered design and prototyping tools for frontend work.",
                    "what_to_do": "Research one AI design tool (like Figma AI) and note what it can do.",
                    "time_required": "10 minutes"
                },
                {
                    "day": 6,
                    "title": "AI Limitations",
                    "what_to_learn": "Understand what AI can't do well and when to rely on your own expertise.",
                    "what_to_do": "Ask an AI tool a complex frontend question and verify if the answer is correct.",
                    "time_required": "10 minutes"
                },
                {
                    "day": 7,
                    "title": "Your AI-Powered Workflow",
                    "what_to_learn": "Design a personal workflow for integrating AI into your development process.",
                    "what_to_do": "Create a simple plan: 3 specific ways you'll use AI in your next project.",
                    "time_required": "10 minutes"
                }
            ]
        }
    }

    print("\n📋 Simulating user journey:")
    print("1. User selects: Tech")
    print("2. User selects: Frontend")
    print("3. User selects: 10 minutes")
    print("4. System generates personalized plan\n")

    # Validate each step
    for step_name, response in workflow.items():
        try:
            validated = validate_llm_response(step_name, response)
            print(f"✅ {step_name} validated successfully")
        except Exception as e:
            print(f"❌ {step_name} validation failed: {e}")
            return

    print("\n🎉 Complete workflow validated successfully!")
    print("\nGenerated Plan Summary:")
    plan_data = workflow["step4"]
    for task in plan_data["plan"]:
        print(f"  Day {task['day']}: {task['title']} ({task['time_required']})")

    print()


def test_json_parsing():
    """Test JSON parsing with markdown code blocks (failsafe)"""
    print("=" * 60)
    print("TEST: JSON Parsing with Markdown")
    print("=" * 60)

    # Sometimes LLMs wrap JSON in markdown
    markdown_wrapped_json = '''```json
{
  "question_id": "background",
  "question_text": "What's your background?",
  "options": ["Tech", "Product", "Design", "Non-tech"]
}
```'''

    print("Testing markdown-wrapped JSON:")
    print(markdown_wrapped_json)

    # Simulate the cleaning logic from learning_planner.py
    response_text = markdown_wrapped_json.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    try:
        parsed = json.loads(response_text)
        validated = validate_llm_response("step1", parsed)
        print("\n✅ Successfully parsed and validated markdown-wrapped JSON")
    except Exception as e:
        print(f"\n❌ Failed: {e}")

    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LLM LEARNING PLANNER - TEST SUITE")
    print("=" * 60 + "\n")

    # Run all tests
    test_step1_validation()
    test_step2_validation()
    test_step3_validation()
    test_step4_validation()
    test_json_parsing()
    test_full_workflow()

    print("=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)
