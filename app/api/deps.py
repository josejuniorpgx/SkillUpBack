"""
API dependencies for dependency injection
"""
from typing import Generator
from fastapi import Depends  # <-- ADD THIS IMPORT
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.repositories.survey import SurveyRepository
from app.repositories.team_member import TeamMemberRepository
from app.repositories.question import QuestionRepository
from app.repositories.response import ResponseRepository
from app.services.survey_service import SurveyService
from app.services.response_service import ResponseService
from app.services.analytics_service import AnalyticsService



def get_db() -> Generator:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_survey_repository(db: Session = Depends(get_db)) -> SurveyRepository:
    """Get survey repository"""
    return SurveyRepository(db)


def get_team_member_repository(db: Session = Depends(get_db)) -> TeamMemberRepository:
    """Get team member repository"""
    return TeamMemberRepository(db)


def get_question_repository(db: Session = Depends(get_db)) -> QuestionRepository:
    """Get question repository"""
    return QuestionRepository(db)


def get_response_repository(db: Session = Depends(get_db)) -> ResponseRepository:
    """Get response repository"""
    return ResponseRepository(db)


def get_survey_service(
        survey_repo: SurveyRepository = Depends(get_survey_repository),
        team_member_repo: TeamMemberRepository = Depends(get_team_member_repository),
        question_repo: QuestionRepository = Depends(get_question_repository)
) -> SurveyService:
    """Get survey service with injected repositories"""
    return SurveyService(survey_repo, team_member_repo, question_repo)


def get_response_service(
        response_repo: ResponseRepository = Depends(get_response_repository),
        team_member_repo: TeamMemberRepository = Depends(get_team_member_repository),
        question_repo: QuestionRepository = Depends(get_question_repository)
) -> ResponseService:
    """Get response service with injected repositories"""
    return ResponseService(response_repo, team_member_repo, question_repo)


def get_analytics_service(
        survey_repo: SurveyRepository = Depends(get_survey_repository),
        team_member_repo: TeamMemberRepository = Depends(get_team_member_repository),
        response_repo: ResponseRepository = Depends(get_response_repository)
) -> AnalyticsService:
    """Get analytics service with injected repositories"""
    return AnalyticsService(survey_repo, team_member_repo, response_repo)

