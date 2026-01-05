"""
Pydantic schemas for validating LLM responses
Ensures the LLM returns data in the expected format
"""

from typing import List
from pydantic import BaseModel, Field, field_validator


class OnboardingQuestion(BaseModel):
    """Schema for onboarding questions (Steps 1-3)"""
    question_id: str = Field(..., description="Unique identifier for the question")
    question_text: str = Field(..., description="The question to display to user")
    options: List[str] = Field(..., min_length=2, max_length=6, description="Answer options")

    @field_validator('options')
    @classmethod
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError('Must have at least 2 options')
        if len(v) > 6:
            raise ValueError('Must have at most 6 options')
        return v


class LearningTask(BaseModel):
    """Schema for a single day's learning task"""
    day: int = Field(..., ge=1, le=7, description="Day number (1-7)")
    title: str = Field(..., min_length=3, max_length=100, description="Task title")
    what_to_learn: str = Field(..., min_length=10, max_length=300, description="What the user will learn (1-2 lines)")
    what_to_do: str = Field(..., min_length=10, max_length=300, description="Actionable task for the user")
    time_required: str = Field(..., description="Time needed (e.g., '10 minutes')")

    @field_validator('time_required')
    @classmethod
    def validate_time(cls, v):
        # Ensure time is mentioned
        if 'minute' not in v.lower():
            raise ValueError('time_required must specify minutes')
        return v


class LearningPlan(BaseModel):
    """Schema for complete 7-day learning plan"""
    plan: List[LearningTask] = Field(..., min_length=7, max_length=7, description="7 days of learning tasks")

    @field_validator('plan')
    @classmethod
    def validate_plan_days(cls, v):
        if len(v) != 7:
            raise ValueError('Plan must have exactly 7 days')

        # Check that days are sequential 1-7
        days = [task.day for task in v]
        if sorted(days) != list(range(1, 8)):
            raise ValueError('Plan must have days 1-7 in order')

        return v


# Expected schemas for each step
STEP_SCHEMAS = {
    "step1": OnboardingQuestion,
    "step2": OnboardingQuestion,
    "step3": OnboardingQuestion,
    "step4": LearningPlan
}


def validate_llm_response(step: str, response_json: dict):
    """
    Validate LLM response against expected schema

    Args:
        step: Which step (step1, step2, step3, step4)
        response_json: The JSON response from LLM

    Returns:
        Validated Pydantic model instance

    Raises:
        ValidationError if response doesn't match schema
    """
    schema = STEP_SCHEMAS.get(step)
    if not schema:
        raise ValueError(f"Invalid step: {step}")

    return schema(**response_json)


# Example validation
if __name__ == "__main__":
    # Valid question
    q1 = OnboardingQuestion(
        question_id="background",
        question_text="What's your background?",
        options=["Tech", "Product", "Design", "Non-tech"]
    )
    print("Valid question:", q1.model_dump())

    # Valid learning plan
    plan = LearningPlan(
        plan=[
            LearningTask(
                day=i,
                title=f"Day {i} Title",
                what_to_learn="Learn about AI basics and how it works.",
                what_to_do="Write 3 examples of AI in daily life.",
                time_required="10 minutes"
            )
            for i in range(1, 8)
        ]
    )
    print("\nValid plan:", plan.model_dump())

    # This will fail - only 5 days
    try:
        invalid_plan = LearningPlan(
            plan=[
                LearningTask(
                    day=i,
                    title=f"Day {i}",
                    what_to_learn="Learn something",
                    what_to_do="Do something",
                    time_required="10 minutes"
                )
                for i in range(1, 6)  # Only 5 days
            ]
        )
    except Exception as e:
        print(f"\nExpected validation error: {e}")
