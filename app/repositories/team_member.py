from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.team_member import TeamMember
from app.repositories.base import BaseRepository


class TeamMemberRepository(BaseRepository[TeamMember]):
    """Repository for TeamMember model"""

    def __init__(self, db: Session):
        super().__init__(TeamMember, db)

    def get_by_unique_link(self, unique_link: str) -> Optional[TeamMember]:
        """Get team member by their unique survey link"""
        return self.db.query(TeamMember).filter(TeamMember.unique_link == unique_link).first()

    def get_by_survey_id(self, survey_id: UUID) -> List[TeamMember]:
        """Get all team members for a specific survey"""
        return self.db.query(TeamMember).filter(TeamMember.survey_id == survey_id).all()

    def mark_as_completed(self, team_member_id: UUID) -> bool:
        """Mark team member survey as completed"""
        team_member = self.get_by_id(team_member_id)
        if team_member:
            team_member.has_completed = True
            self.db.commit()
            return True
        return False

    def get_completion_stats(self, survey_id: UUID) -> dict:
        """Get completion statistics for a survey"""
        total = self.db.query(TeamMember).filter(TeamMember.survey_id == survey_id).count()
        completed = (
            self.db.query(TeamMember)
            .filter(TeamMember.survey_id == survey_id, TeamMember.has_completed == True)
            .count()
        )

        completion_rate = (completed / total * 100) if total > 0 else 0

        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "completion_rate": completion_rate
        }

    def create_batch(self, team_members_data: List[dict]) -> List[TeamMember]:
        """Create multiple team members in a single transaction"""
        team_members = []
        for data in team_members_data:
            team_member = TeamMember(**data)
            self.db.add(team_member)
            team_members.append(team_member)

        self.db.commit()

        # Refresh all objects to get their IDs
        for team_member in team_members:
            self.db.refresh(team_member)

        return team_members
