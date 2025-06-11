from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc

from app.models.question import SurveyQuestion
from app.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[SurveyQuestion]):
    """Repository for SurveyQuestion model"""

    def __init__(self, db: Session):
        super().__init__(SurveyQuestion, db)

    def get_all_ordered(self) -> List[SurveyQuestion]:
        """Get all questions ordered by question_order"""
        return (
            self.db.query(SurveyQuestion)
            .order_by(asc(SurveyQuestion.question_order))
            .all()
        )

    def get_by_order(self, order: int) -> Optional[SurveyQuestion]:
        """Get question by its order number"""
        return (
            self.db.query(SurveyQuestion)
            .filter(SurveyQuestion.question_order == order)
            .first()
        )

    def count_questions(self) -> int:
        """Count total number of questions"""
        return self.db.query(SurveyQuestion).count()

