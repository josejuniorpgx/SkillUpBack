from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class QuestionAnalytics(BaseModel):
    """Analytics for individual question"""
    questionId: str = Field(..., description="Question UUID")
    questionText: str = Field(..., description="Question text")
    averageScore: float = Field(..., ge=1.0, le=5.0, description="Average score for this question")
    responseCount: int = Field(..., ge=0, description="Number of responses for this question")

    model_config = ConfigDict(from_attributes=True)


class ProgressSummary(BaseModel):
    """Survey completion progress summary"""
    completed: int = Field(..., ge=0, description="Number of completed responses")
    pending: int = Field(..., ge=0, description="Number of pending responses")
    completionRate: float = Field(..., ge=0.0, le=100.0, description="Completion rate percentage")


class SurveyAnalytics(BaseModel):
    """Complete survey analytics"""
    surveyId: str = Field(..., description="Survey UUID")
    totalMembers: int = Field(..., ge=0, description="Total number of team members")
    completedResponses: int = Field(..., ge=0, description="Number of completed responses")
    completionRate: float = Field(..., ge=0.0, le=100.0, description="Completion rate percentage")
    questionAnalytics: List[QuestionAnalytics] = Field(..., description="Analytics per question")
    overallAverage: Optional[float] = Field(None, ge=1.0, le=5.0,
                                            description="Overall average score across all questions")


class SurveyAnalyticsResponse(BaseModel):
    """Response wrapper for survey analytics"""
    success: bool = True
    data: SurveyAnalytics
