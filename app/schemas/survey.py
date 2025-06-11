from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class TeamMemberInput(BaseModel):
    """Team member data for survey creation (from frontend)"""
    name: str = Field(..., min_length=1, max_length=255, description="Team member full name")
    email: EmailStr = Field(..., description="Team member email address")


class SurveyCreate(BaseModel):
    """Schema for creating a new survey (from frontend)"""
    managerId: str = Field(..., min_length=1, max_length=255, description="Manager identifier")
    teamMembers: List[TeamMemberInput] = Field(..., min_items=1, max_items=10, description="List of team members")


class TeamMemberWithLink(BaseModel):
    """Team member with generated survey link (for API response)"""
    id: str = Field(..., description="Team member UUID")
    name: str = Field(..., description="Team member full name")
    email: EmailStr = Field(..., description="Team member email")
    surveyLink: str = Field(..., description="Unique survey link for this team member")
    hasCompleted: bool = Field(default=False, description="Whether survey is completed")

    model_config = ConfigDict(from_attributes=True)


class SurveyCreateData(BaseModel):
    """Data returned after creating survey"""
    surveyId: str = Field(..., description="Survey UUID")
    teamMembers: List[TeamMemberWithLink] = Field(..., description="Team members with generated links")


class SurveyResponse(BaseModel):
    """Complete survey response schema"""
    success: bool = True
    data: SurveyCreateData


class SurveyQuestion(BaseModel):
    """Survey question schema"""
    id: str = Field(..., description="Question UUID")
    questionText: str = Field(..., description="Question text")
    questionOrder: int = Field(..., description="Question order/position")
    scaleMin: int = Field(default=1, description="Minimum scale value")
    scaleMax: int = Field(default=5, description="Maximum scale value")
    scaleMinLabel: str = Field(default="Poor", description="Label for minimum scale")
    scaleMaxLabel: str = Field(default="Excellent", description="Label for maximum scale")

    model_config = ConfigDict(from_attributes=True)


class SurveyData(BaseModel):
    """Survey data for team member view (GET /survey/{token})"""
    surveyTitle: str = Field(default="Leadership Feedback Survey", description="Survey title")
    description: str = Field(default="Your responses are anonymous and will help improve leadership effectiveness.",
                             description="Survey description")
    teamMemberName: str = Field(..., description="Name of team member taking survey")
    hasCompleted: bool = Field(..., description="Whether this team member has completed the survey")
    questions: List[SurveyQuestion] = Field(..., description="List of survey questions")


class SurveyDataResponse(BaseModel):
    """Response wrapper for survey data"""
    success: bool = True
    data: SurveyData
