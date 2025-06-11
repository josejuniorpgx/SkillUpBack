from typing import List, Optional
from uuid import UUID

from app.repositories.survey import SurveyRepository
from app.repositories.team_member import TeamMemberRepository
from app.repositories.response import ResponseRepository
from app.schemas.analytics import (
    SurveyAnalytics,
    QuestionAnalytics,
    ProgressSummary
)


class AnalyticsService:
    """Service for analytics and reporting business logic"""

    def __init__(
            self,
            survey_repo: SurveyRepository,
            team_member_repo: TeamMemberRepository,
            response_repo: ResponseRepository
    ):
        self.survey_repo = survey_repo
        self.team_member_repo = team_member_repo
        self.response_repo = response_repo

    async def get_survey_analytics(self, survey_id: UUID) -> Optional[SurveyAnalytics]:
        """
        Calculate comprehensive analytics for a survey

        Business Logic:
        1. Validate survey exists
        2. Get completion statistics
        3. Calculate question-level analytics
        4. Calculate overall average
        5. Return comprehensive analytics
        """

        # Validate survey exists
        survey = self.survey_repo.get_by_id(survey_id)
        if not survey:
            return None

        # Get completion statistics
        completion_stats = self.team_member_repo.get_completion_stats(survey_id)

        # Get question analytics
        question_analytics_data = self.response_repo.get_analytics_for_survey(survey_id)

        question_analytics = []
        for qa_data in question_analytics_data:
            question_analytic = QuestionAnalytics(
                questionId=qa_data["question_id"],
                questionText=qa_data["question_text"],
                averageScore=round(qa_data["average_score"], 2),
                responseCount=qa_data["response_count"]
            )
            question_analytics.append(question_analytic)

        # Calculate overall average
        overall_average = self.response_repo.get_overall_average_for_survey(survey_id)
        if overall_average is not None:
            overall_average = round(overall_average, 2)

        return SurveyAnalytics(
            surveyId=str(survey_id),
            totalMembers=completion_stats["total"],
            completedResponses=completion_stats["completed"],
            completionRate=round(completion_stats["completion_rate"], 2),
            questionAnalytics=question_analytics,
            overallAverage=overall_average
        )

    async def get_progress_summary(self, survey_id: UUID) -> Optional[ProgressSummary]:
        """Get just the progress summary for a survey"""

        survey = self.survey_repo.get_by_id(survey_id)
        if not survey:
            return None

        completion_stats = self.team_member_repo.get_completion_stats(survey_id)

        return ProgressSummary(
            completed=completion_stats["completed"],
            pending=completion_stats["pending"],
            completionRate=round(completion_stats["completion_rate"], 2)
        )

    async def calculate_manager_analytics(self, manager_id: str) -> dict:
        """Calculate analytics across all surveys for a manager"""

        surveys = self.survey_repo.get_by_manager_id(manager_id)

        total_surveys = len(surveys)
        total_team_members = 0
        total_completed_responses = 0

        survey_analytics = []
        for survey in surveys:
            stats = self.team_member_repo.get_completion_stats(survey.id)
            total_team_members += stats["total"]
            total_completed_responses += stats["completed"]

            survey_analytics.append({
                "surveyId": str(survey.id),
                "title": survey.title,
                "status": survey.status,
                "completionRate": stats["completion_rate"],
                "createdAt": survey.created_at
            })

        overall_completion_rate = (
            (total_completed_responses / total_team_members * 100)
            if total_team_members > 0 else 0
        )

        return {
            "managerId": manager_id,
            "totalSurveys": total_surveys,
            "totalTeamMembers": total_team_members,
            "totalCompletedResponses": total_completed_responses,
            "overallCompletionRate": round(overall_completion_rate, 2),
            "surveys": survey_analytics
        }
