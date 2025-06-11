
# FILE: app/api/v1/endpoints/responses.py
"""
Response endpoints - Survey completion and submission
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_survey_service, get_response_service
from app.services.survey_service import SurveyService
from app.services.response_service import ResponseService
from app.schemas.survey import SurveyDataResponse
from app.schemas.response import SurveySubmission, SurveySubmissionResponse

router = APIRouter()


@router.get(
    "/{token}",
    response_model=SurveyDataResponse,
    summary="Get survey for completion",
    description="Load survey data for a team member using their unique token"
)
async def get_survey_by_token(
        token: str,
        survey_service: SurveyService = Depends(get_survey_service)
):
    """
    Get survey data for completion by team member.

    - **token**: Unique survey token for the team member

    Returns:
    - Survey title and description
    - Team member name
    - Completion status
    - List of questions to answer
    """
    try:
        survey_data = await survey_service.get_survey_by_token(token)

        if not survey_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Survey not found or invalid link"
            )

        return SurveyDataResponse(data=survey_data)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load survey"
        )


@router.post(
    "/{token}/response",
    response_model=SurveySubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit survey responses",
    description="Submit survey responses for a team member"
)
async def submit_survey_response(
        token: str,
        submission: SurveySubmission,
        response_service: ResponseService = Depends(get_response_service)
):
    """
    Submit survey responses.

    - **token**: Unique survey token for the team member
    - **responses**: Array of question responses with ratings 1-5

    Must include exactly 3 responses (one for each question).
    Ratings must be between 1 and 5.
    """
    try:
        response_data = await response_service.submit_survey_response(token, submission)

        return SurveySubmissionResponse(data=response_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit survey response"
        )


@router.get(
    "/{token}/responses",
    summary="Get team member responses",
    description="Get existing responses for a team member (if any)"
)
async def get_team_member_responses(
        token: str,
        response_service: ResponseService = Depends(get_response_service)
):
    """
    Get existing responses for a team member.

    - **token**: Unique survey token for the team member

    Returns list of submitted responses (empty if not completed).
    """
    try:
        responses = await response_service.get_team_member_responses(token)

        return {"success": True, "data": {"responses": responses}}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get responses"
        )
