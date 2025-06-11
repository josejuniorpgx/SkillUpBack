# app/models/response.py
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import BaseModel


class Response(BaseModel):
    """
    Representation of a Response in the survey system.

    This class models a Response entity used to store data about a team's answers
    to survey questions. It includes the rating provided by team members, the
    timestamp when the response was submitted, and relationships with the
    TeamMember and SurveyQuestion entities. Constraints are applied to ensure
    the rating stays within a defined range. The `Response` class also provides
    utility methods to access related data and validate its rating.

    :ivar rating: Rating provided as part of the response. Must be between 1 and 5.
    :type rating: int
    :ivar submitted_at: Timestamp indicating when the response was submitted.
    :type submitted_at: datetime
    :ivar team_member_id: Identifier of the team member who submitted the response.
    :type team_member_id: UUID
    :ivar team_member: Relationship with the TeamMember entity, representing the
        team member who submitted the response.
    :type team_member: TeamMember
    :ivar question_id: Identifier of the survey question the response corresponds to.
    :type question_id: UUID
    :ivar question: Relationship with the SurveyQuestion entity, representing the
        associated survey question.
    :type question: SurveyQuestion
    """
    __tablename__ = "responses"

    rating = Column(
        Integer,
        nullable=False,
    )

    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    team_member_id = Column(
        UUID(as_uuid=True),
        ForeignKey("team_members.id", ondelete="CASCADE"),
        nullable=False
    )
    team_member = relationship("TeamMember", back_populates="responses")

    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("survey_questions.id", ondelete="CASCADE"),
        nullable=False
    )
    question = relationship("SurveyQuestion", back_populates="responses")

    __table_args__ = (
        CheckConstraint(
            'rating >= 1 AND rating <= 5',
            name='check_rating_range'
        ),
    )

    def __repr__(self):
        return f"<Response(id={self.id}, team_member_id={self.team_member_id}, question_id={self.question_id}, rating={self.rating})>"

    @property
    def survey_id(self):
        """
        Provides an interface to retrieve the survey ID associated with a team member. The property
        evaluates whether a ``team_member`` exists and fetches the ``survey_id`` accordingly. If the
        team member is not set, the property returns ``None``.

        :rtype: Optional[Any]
        :return: The survey ID associated with the team member or None if no team member is set.
        """
        return self.team_member.survey_id if self.team_member else None

    def is_valid_rating(self) -> bool:
        """
        Determines whether the rating is valid.

        This method checks if the `rating` attribute of the object falls within
        the valid range of 1 to 5, inclusive. It ensures that the rating meets
        the expected constraints for validity.

        :return: True if the rating is between 1 and 5 inclusive, False otherwise.
        :rtype: bool
        """
        return 1 <= self.rating <= 5