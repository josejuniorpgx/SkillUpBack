from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class TeamMember(BaseModel):
    """
    Represents a team member participating in a survey.

    This class defines the attributes and relationships related to a team member in the
    context of a survey system. It includes details about the team member, their survey
    association, responses, and completion status. It also provides functionality to
    mark a member as having completed the survey and generate their unique survey link.

    :ivar name: Full name of the team member.
    :type name: str
    :ivar email: Email address of the team member.
    :type email: str
    :ivar unique_link: Unique link for accessing the survey for this team member.
    :type unique_link: str
    :ivar has_completed: Indicates if the survey has been completed by the member.
    :type has_completed: bool
    :ivar completed_at: Timestamp when the survey was completed, or None if not completed.
    :type completed_at: Optional[datetime]
    :ivar survey_id: Foreign key referencing the associated survey's ID.
    :type survey_id: UUID
    :ivar survey: Relationship to the associated Survey object.
    :type survey: Survey
    :ivar responses: List of responses submitted by this team member.
    :type responses: List[Response]
    """
    __tablename__ = "team_members"

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    # Unique link to access the survey
    unique_link = Column(String(255), unique=True, nullable=False, index=True)

    has_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    survey_id = Column(
        UUID(as_uuid=True),
        ForeignKey("surveys.id", ondelete="CASCADE"),
        nullable=False
    )
    survey = relationship("Survey", back_populates="team_members")

    responses = relationship(
        "Response",
        back_populates="team_member",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<TeamMember(id={self.id}, name={self.name}, has_completed={self.has_completed})>"

    def mark_as_completed(self):
        """Mark the team member's survey as completed."""
        from datetime import datetime
        self.has_completed = True
        self.completed_at = datetime.utcnow()

    @property
    def survey_link(self) -> str:
        """
        Generates a survey link for specific user based on a unique identifier.

        This property constructs a personalized survey URL by appending
        a user's unique link to a predefined base URL.

        :rtype: str
        :return: The complete survey link as a string.
        """
        # todo: Replace with actual base URL from settings or environment
        base_url = "http://localhost:3000"
        return f"{base_url}/survey/{self.unique_link}"