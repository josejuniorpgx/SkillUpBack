
# FILE: app/services/survey_service.py
"""
Survey business logic service
"""
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.repositories.survey import SurveyRepository
from app.repositories.team_member import TeamMemberRepository
from app.repositories.question import QuestionRepository
from app.schemas.survey import (
    SurveyCreate,
    SurveyCreateData,
    TeamMemberWithLink,
    SurveyData,
    SurveyQuestion
)
from app.utils.link_generator import generate_unique_token
from app.config import get_settings

settings = get_settings()


class SurveyService:
    """Service for survey-related business logic"""

    def __init__(
            self,
            survey_repo: SurveyRepository,
            team_member_repo: TeamMemberRepository,
            question_repo: QuestionRepository
    ):
        self.survey_repo = survey_repo
        self.team_member_repo = team_member_repo
        self.question_repo = question_repo

    async def create_survey(self, survey_data: SurveyCreate) -> SurveyCreateData:
        """
        Create a new survey with team members

        Business Logic:
        1. Validate we have exactly 3 questions in database
        2. Create survey record
        3. Generate unique links for each team member
        4. Create team member records
        5. Return survey data with links
        """

        # Validate we have the required questions
        question_count = self.question_repo.count_questions()
        if question_count != 3:
            raise ValueError(f"System must have exactly 3 questions, found {question_count}")

        # Create survey
        survey_id = uuid4()
        survey_dict = {
            "id": survey_id,
            "manager_id": survey_data.managerId,
            "title": "Leadership Feedback Survey",
            "description": "Anonymous feedback survey for leadership effectiveness",
            "status": "active"
        }

        created_survey = self.survey_repo.create(survey_dict)

        # Prepare team members data with unique links
        team_members_data = []
        for member in survey_data.teamMembers:
            unique_token = generate_unique_token()
            team_member_dict = {
                "id": uuid4(),
                "survey_id": survey_id,
                "name": member.name,
                "email": member.email,
                "unique_link": unique_token,
                "has_completed": False
            }
            team_members_data.append(team_member_dict)

        # Create team members in batch
        created_team_members = self.team_member_repo.create_batch(team_members_data)

        # Build response data with survey links
        team_members_with_links = []
        for team_member in created_team_members:
            survey_link = f"{settings.FRONTEND_URL}/survey/{team_member.unique_link}"

            team_member_response = TeamMemberWithLink(
                id=str(team_member.id),
                name=team_member.name,
                email=team_member.email,
                surveyLink=survey_link,
                hasCompleted=team_member.has_completed
            )
            team_members_with_links.append(team_member_response)

        return SurveyCreateData(
            surveyId=str(created_survey.id),
            teamMembers=team_members_with_links
        )

    async def get_survey_by_token(self, token: str) -> Optional[SurveyData]:
        """
        Get survey data for a team member by their unique token

        Business Logic:
        1. Find team member by unique link token
        2. Check if survey exists and is active
        3. Get all questions ordered
        4. Return survey data for completion
        """

        # Find team member by token
        team_member = self.team_member_repo.get_by_unique_link(token)
        if not team_member:
            return None

        # Get survey and validate it's active
        survey = self.survey_repo.get_by_id(team_member.survey_id)
        if not survey or survey.status != "active":
            return None

        # Get all questions ordered
        questions = self.question_repo.get_all_ordered()
        if len(questions) != 3:
            raise ValueError("Survey must have exactly 3 questions")

        # Convert questions to response format
        survey_questions = []
        for question in questions:
            survey_question = SurveyQuestion(
                id=str(question.id),
                questionText=question.question_text,
                questionOrder=question.question_order,
                scaleMin=question.scale_min,
                scaleMax=question.scale_max,
                scaleMinLabel=question.scale_min_label,
                scaleMaxLabel=question.scale_max_label
            )
            survey_questions.append(survey_question)

        return SurveyData(
            surveyTitle=survey.title,
            description=survey.description,
            teamMemberName=team_member.name,
            hasCompleted=team_member.has_completed,
            questions=survey_questions
        )

    async def get_survey_status(self, survey_id: UUID) -> Optional[dict]:
        """Get survey status and team member completion info"""

        survey = self.survey_repo.get_by_id(survey_id)
        if not survey:
            return None

        team_members = self.team_member_repo.get_by_survey_id(survey_id)
        completion_stats = self.team_member_repo.get_completion_stats(survey_id)

        team_members_data = []
        for member in team_members:
            team_members_data.append({
                "id": str(member.id),
                "name": member.name,
                "email": member.email,
                "hasCompleted": member.has_completed,
                "completedAt": None  # Could add timestamp if needed
            })

        return {
            "surveyId": str(survey.id),
            "status": survey.status,
            "teamMembers": team_members_data,
            "progressSummary": {
                "completed": completion_stats["completed"],
                "pending": completion_stats["pending"],
                "completionRate": completion_stats["completion_rate"]
            }
        }
