"""
Survey endpoints - Creation and Analytics
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_survey_service, get_analytics_service
from app.services.survey_service import SurveyService
from app.services.analytics_service import AnalyticsService
from app.schemas.survey import SurveyCreate, SurveyResponse
from app.schemas.analytics import SurveyAnalyticsResponse
from app.schemas.common import ErrorResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SurveyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new survey",
    description="Create a new leadership feedback survey with team members"
)
async def create_survey(
        survey_data: SurveyCreate,
        survey_service: SurveyService = Depends(get_survey_service)
):
    """
    Create a new survey with team members.

    - **managerId**: Manager identifier
    - **teamMembers**: List of team members (name + email)

    Returns survey ID and unique links for each team member.
    """
    try:
        survey_create_data = await survey_service.create_survey(survey_data)
        return SurveyResponse(data=survey_create_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create survey"
        )


@router.get(
    "/{survey_id}/analytics",
    response_model=SurveyAnalyticsResponse,
    summary="Get survey analytics",
    description="Get comprehensive analytics for a survey including completion rates and question averages"
)
async def get_survey_analytics(
        survey_id: UUID,
        analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get analytics for a survey.

    - **survey_id**: UUID of the survey

    Returns:
    - Completion statistics
    - Average scores per question
    - Overall average score
    """
    try:
        analytics = await analytics_service.get_survey_analytics(survey_id)

        if not analytics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Survey not found"
            )

        return SurveyAnalyticsResponse(data=analytics)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get survey analytics"
        )


@router.get(
    "/{survey_id}/status",
    summary="Get survey status",
    description="Get survey status and team member completion information"
)
async def get_survey_status(
        survey_id: UUID,
        survey_service: SurveyService = Depends(get_survey_service)
):
    """
    Get survey status and team member completion info.

    - **survey_id**: UUID of the survey

    Returns survey status and completion details for each team member.
    """
    try:
        status_data = await survey_service.get_survey_status(survey_id)

        if not status_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Survey not found"
            )

        return {"success": True, "data": status_data}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get survey status"
        )

