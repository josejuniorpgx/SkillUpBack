from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.survey import Survey
from app.repositories.base import BaseRepository


class SurveyRepository(BaseRepository[Survey]):
    """Repository for Survey model"""

    def __init__(self, db: Session):
        super().__init__(Survey, db)

    def get_by_manager_id(self, manager_id: str) -> List[Survey]:
        """Get all surveys for a specific manager"""
        return self.db.query(Survey).filter(Survey.manager_id == manager_id).all()

    def get_active_surveys(self) -> List[Survey]:
        """Get all active surveys"""
        return self.db.query(Survey).filter(Survey.status == "active").all()

    def get_with_team_members(self, survey_id: UUID) -> Optional[Survey]:
        """Get survey with its team members loaded"""
        from app.models.team_member import TeamMember
        return (
            self.db.query(Survey)
            .filter(Survey.id == survey_id)
            .first()
        )

    def mark_as_completed(self, survey_id: UUID) -> bool:
        """Mark survey as completed"""
        survey = self.get_by_id(survey_id)
        if survey:
            survey.status = "completed"
            self.db.commit()
            return True
        return False
