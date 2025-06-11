from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.response import Response
from app.models.question import SurveyQuestion
from app.repositories.base import BaseRepository


class ResponseRepository(BaseRepository[Response]):
    """Repository for Response model"""

    def __init__(self, db: Session):
        super().__init__(Response, db)

    def get_by_team_member(self, team_member_id: UUID) -> list[type[Response]]:
        """Get all responses for a specific team member"""
        return (
            self.db.query(Response)
            .filter(Response.team_member_id == team_member_id)
            .all()
        )

    def get_responses_for_survey(self, survey_id: UUID) -> list[type[Response]]:
        """Get all responses for a survey (via team members)"""
        from app.models.team_member import TeamMember
        return (
            self.db.query(Response)
            .join(TeamMember)
            .filter(TeamMember.survey_id == survey_id)
            .all()
        )

    def create_batch(self, responses_data: List[dict]) -> List[Response]:
        """Create multiple responses in a single transaction"""
        responses = []
        for data in responses_data:
            response = Response(**data)
            self.db.add(response)
            responses.append(response)

        self.db.commit()

        # Refresh all objects
        for response in responses:
            self.db.refresh(response)

        return responses

    def get_analytics_for_survey(self, survey_id: UUID) -> List[Dict]:
        """Get analytics data for a survey"""
        from app.models.team_member import TeamMember

        # Get average scores per question
        analytics = (
            self.db.query(
                Response.question_id,
                SurveyQuestion.question_text,
                func.avg(Response.rating).label("average_score"),
                func.count(Response.id).label("response_count")
            )
            .join(SurveyQuestion, Response.question_id == SurveyQuestion.id)
            .join(TeamMember, Response.team_member_id == TeamMember.id)
            .filter(TeamMember.survey_id == survey_id)
            .group_by(Response.question_id, SurveyQuestion.question_text)
            .all()
        )

        return [
            {
                "question_id": str(row.question_id),
                "question_text": row.question_text,
                "average_score": float(row.average_score),
                "response_count": row.response_count
            }
            for row in analytics
        ]

    def get_overall_average_for_survey(self, survey_id: UUID) -> Optional[float]:
        """Get overall average score for a survey"""
        from app.models.team_member import TeamMember

        result = (
            self.db.query(func.avg(Response.rating))
            .join(TeamMember)
            .filter(TeamMember.survey_id == survey_id)
            .scalar()
        )

        return float(result) if result else None

    def team_member_has_responses(self, team_member_id: UUID) -> bool:
        """Check if team member has already submitted responses"""
        count = (
            self.db.query(Response)
            .filter(Response.team_member_id == team_member_id)
            .count()
        )
        return count > 0
