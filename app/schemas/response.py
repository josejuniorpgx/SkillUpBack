from typing import List
from uuid import UUID
from pydantic import BaseModel, Field, validator


class ResponseSubmit(BaseModel):
    """Individual question response"""
    questionId: str = Field(..., description="Question UUID")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")

    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


class SurveySubmission(BaseModel):
    """Complete survey submission (array of responses)"""
    responses: List[ResponseSubmit] = Field(..., min_items=1, description="List of question responses")

    @validator('responses')
    def validate_responses(cls, v):
        if len(v) != 3:  # We have exactly 3 questions
            raise ValueError('Survey must contain exactly 3 responses')

        # Check for duplicate question IDs
        question_ids = [r.questionId for r in v]
        if len(set(question_ids)) != len(question_ids):
            raise ValueError('Duplicate question responses are not allowed')

        return v


class ResponseData(BaseModel):
    """Response data after submission"""
    message: str = Field(default="Survey submitted successfully", description="Success message")


class SurveySubmissionResponse(BaseModel):
    """Response wrapper for survey submission"""
    success: bool = True
    data: ResponseData
