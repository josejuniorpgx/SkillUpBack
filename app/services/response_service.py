from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.repositories.response import ResponseRepository
from app.repositories.team_member import TeamMemberRepository
from app.repositories.question import QuestionRepository
from app.schemas.response import SurveySubmission, ResponseData


class ResponseService:
    """Service for response submission business logic"""

    def __init__(
            self,
            response_repo: ResponseRepository,
            team_member_repo: TeamMemberRepository,
            question_repo: QuestionRepository
    ):
        self.response_repo = response_repo
        self.team_member_repo = team_member_repo
        self.question_repo = question_repo

    async def submit_survey_response(self, token: str, submission: SurveySubmission) -> ResponseData:
        """
        Submit survey responses for a team member

        Business Logic:
        1. Find team member by token
        2. Validate team member exists and hasn't completed survey
        3. Validate all question IDs exist
        4. Create response records
        5. Mark team member as completed
        6. Return success message
        """

        # Find team member by token
        team_member = self.team_member_repo.get_by_unique_link(token)
        if not team_member:
            raise ValueError("Invalid survey link")

        # Check if already completed
        if team_member.has_completed:
            raise ValueError("Survey has already been completed")

        # Validate team member hasn't submitted responses before
        if self.response_repo.team_member_has_responses(team_member.id):
            raise ValueError("Responses have already been submitted for this survey")

        # Validate all question IDs exist
        all_questions = self.question_repo.get_all_ordered()
        valid_question_ids = {str(q.id) for q in all_questions}

        submitted_question_ids = {response.questionId for response in submission.responses}

        if not submitted_question_ids.issubset(valid_question_ids):
            invalid_ids = submitted_question_ids - valid_question_ids
            raise ValueError(f"Invalid question IDs: {invalid_ids}")

        # Ensure all questions are answered (we have exactly 3)
        if len(submission.responses) != 3:
            raise ValueError("All 3 questions must be answered")

        if submitted_question_ids != valid_question_ids:
            raise ValueError("Must answer all survey questions")

        # Create response records
        responses_data = []
        for response in submission.responses:
            response_dict = {
                "id": uuid4(),
                "team_member_id": team_member.id,
                "question_id": UUID(response.questionId),
                "rating": response.rating
            }
            responses_data.append(response_dict)

        # Create responses in batch
        self.response_repo.create_batch(responses_data)

        # Mark team member as completed
        self.team_member_repo.mark_as_completed(team_member.id)

        return ResponseData(message="Survey submitted successfully")

    async def get_team_member_responses(self, token: str) -> List[dict]:
        """Get existing responses for a team member (if any)"""

        team_member = self.team_member_repo.get_by_unique_link(token)
        if not team_member:
            raise ValueError("Invalid survey link")

        responses = self.response_repo.get_by_team_member(team_member.id)

        return [
            {
                "questionId": str(response.question_id),
                "rating": response.rating,
                "submittedAt": response.submitted_at
            }
            for response in responses
        ]
