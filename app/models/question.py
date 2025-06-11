from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class SurveyQuestion(BaseModel):
    """
    Represents a survey question entity used to capture user responses in a survey.

    The class is designed to handle the storage and retrieval of individual survey
    questions along with their associated configurations such as a defined response
    scale and question order. It also manages relationships with responses for
    tracking answers provided by users.

    :ivar question_text: The text of the survey question that will be presented to
        the respondents.
    :type question_text: sqlalchemy.types.Text
    :ivar question_order: Numerical value indicating the order of the question in
        the survey.
    :type question_order: sqlalchemy.types.Integer
    :ivar scale_min: Lower bound of the response scale for the survey question.
    :type scale_min: sqlalchemy.types.Integer
    :ivar scale_max: Upper bound of the response scale for the survey question.
    :type scale_max: sqlalchemy.types.Integer
    :ivar scale_min_label: Label representing the meaning of the lowest value on
        the response scale.
    :type scale_min_label: sqlalchemy.types.String
    :ivar scale_max_label: Label representing the meaning of the highest value on
        the response scale.
    :type scale_max_label: sqlalchemy.types.String
    :ivar responses: Relationship to the Response model, representing the
        responses associated with this survey question.
    :type responses: sqlalchemy.orm.relationship
    """
    __tablename__ = "survey_questions"

    question_text = Column(Text, nullable=False)

    question_order = Column(Integer, nullable=False, index=True)

    scale_min = Column(Integer, default=1, nullable=False)
    scale_max = Column(Integer, default=5, nullable=False)
    scale_min_label = Column(String(50), default="Poor", nullable=False)
    scale_max_label = Column(String(50), default="Excellent", nullable=False)

    responses = relationship(
        "Response",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<SurveyQuestion(id={self.id}, order={self.question_order}, text='{self.question_text[:50]}...')>"

    @classmethod
    def get_default_questions(cls):
        """
        Provides default questions for evaluating managerial skills and leadership.

        This method returns a list of dictionaries, where each dictionary represents
        a survey question related to a manager's performance. Each question includes
        information such as question text, order, scale range, and labels.

        :return: List of dictionaries, each representing a survey question. Each
            dictionary contains the following keys:

            - ``question_text`` (str): Text of the question.
            - ``question_order`` (int): The order of the question in the survey.
            - ``scale_min`` (int): Minimum scale value for the response.
            - ``scale_max`` (int): Maximum scale value for the response.
            - ``scale_min_label`` (str): Label describing the minimum scale value.
            - ``scale_max_label`` (str): Label describing the maximum scale value.
        :rtype: list[dict[str, int | str]]
        """
        return [
            {
                "question_text": "How effectively does your manager communicate expectations?",
                "question_order": 1,
                "scale_min": 1,
                "scale_max": 5,
                "scale_min_label": "Poor",
                "scale_max_label": "Excellent"
            },
            {
                "question_text": "How well does your manager support your professional development?",
                "question_order": 2,
                "scale_min": 1,
                "scale_max": 5,
                "scale_min_label": "Poor",
                "scale_max_label": "Excellent"
            },
            {
                "question_text": "How would you rate your manager's overall leadership effectiveness?",
                "question_order": 3,
                "scale_min": 1,
                "scale_max": 5,
                "scale_min_label": "Poor",
                "scale_max_label": "Excellent"
            }
        ]