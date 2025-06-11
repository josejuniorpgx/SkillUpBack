# app/models/survey.py
from sqlalchemy import Column, String, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.models.base import BaseModel


class SurveyStatus(str, Enum):
    """
    Represents the status of a survey.

    This enumeration provides predefined statuses that a survey can have.
    It includes options such as active, completed, and draft. The class
    is based on both string and Enum to allow for easy usage and comparison.

    :cvar ACTIVE: Represents an actively ongoing survey status.
    :cvar COMPLETED: Represents a survey that has been completed.
    :cvar DRAFT: Represents a survey that is in draft status.
    """
    ACTIVE = "active"
    COMPLETED = "completed"
    DRAFT = "draft"


class Survey(BaseModel):
    """
    Represents a survey for collecting feedback, typically for leadership effectiveness.

    A `Survey` object is designed to handle feedback collection for managers with team
    members. The survey includes attributes such as a manager identifier, descriptive
    information, status, and relationships with team members. It provides properties to
    calculate the team size, the number of completed responses, and survey completion rate.

    :ivar manager_id: Identifier for the manager who owns the survey.
    :type manager_id: str
    :ivar title: Title of the survey.
    :type title: str
    :ivar description: Detailed description of the survey purpose and anonymity assurance.
    :type description: str
    :ivar status: Current status of the survey.
    :type status: SurveyStatus
    :ivar team_members: List of team members associated with this survey.
    :type team_members: list
    """
    __tablename__ = "surveys"

    manager_id = Column(String(255), nullable=False, index=True)
    title = Column(
        String(255),
        nullable=False,
        default="Leadership Feedback Survey"
    )
    description = Column(
        Text,
        default="Your honest feedback will help improve leadership effectiveness. All responses are anonymous."
    )


    status = Column(
        SQLEnum(SurveyStatus),
        default=SurveyStatus.ACTIVE,
        nullable=False
    )

    team_members = relationship(
        "TeamMember",
        back_populates="survey",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Survey(id={self.id}, manager_id={self.manager_id}, status={self.status})>"

    @property
    def total_members(self) -> int:
        """Total number of team members in the survey"""
        return len(self.team_members)

    @property
    def completed_responses(self) -> int:
        """Number of team members who have completed the survey"""
        return len([member for member in self.team_members if member.has_completed])

    @property
    def completion_rate(self) -> float:
        """Final completion rate of the survey as a percentage"""
        if self.total_members == 0:
            return 0.0
        return (self.completed_responses / self.total_members) * 100