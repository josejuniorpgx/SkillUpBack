import secrets
import string
from typing import Optional
from sqlalchemy.orm import Session
from app.models.team_member import TeamMember


def generate_unique_token(length: int = 32) -> str:
    """
    Generates a unique and secure token for survey links.

    Args:
        length: Token length (default 32 characters)

    Returns:
        Unique and secure string to use as token
    """
    # Use only letters and numbers to avoid URL problems
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_unique_survey_link(db: Session, max_attempts: int = 10) -> str:
    """
    Generates a unique link for a survey, verifying it doesn't exist in the DB.

    Args:
        db: Database session to verify uniqueness
        max_attempts: Maximum number of attempts to generate a unique token

    Returns:
        Unique token that doesn't exist in the database

    Raises:
        RuntimeError: If a unique token cannot be generated after max_attempts
    """
    for attempt in range(max_attempts):
        # Generate candidate token
        token = generate_unique_token()

        # Verify it doesn't exist in the database
        existing = db.query(TeamMember).filter(TeamMember.unique_link == token).first()

        if not existing:
            return token

    # If we get here, we couldn't generate a unique token
    raise RuntimeError(f"Could not generate a unique token after {max_attempts} attempts")


def create_survey_link_for_member(
        db: Session,
        name: str,
        email: str,
        survey_id: str,
        frontend_url: Optional[str] = None
) -> tuple[str, str]:
    """
    Creates a unique link for a team member and returns both the token and the complete link.

    Args:
        db: Database session
        name: Team member's name
        email: Team member's email
        survey_id: Survey ID
        frontend_url: Frontend base URL (optional)

    Returns:
        Tuple with (unique_token, complete_link)
    """
    # Generate unique token
    unique_token = generate_unique_survey_link(db)

    # Create complete link
    if frontend_url is None:
        from app.config import settings
        frontend_url = settings.FRONTEND_URL

    full_link = f"{frontend_url}/survey/{unique_token}"

    return unique_token, full_link


def validate_survey_token(db: Session, token: str) -> Optional[TeamMember]:
    """
    Validates a survey token and returns the associated TeamMember if it exists.

    Args:
        db: Database session
        token: Token to validate

    Returns:
        TeamMember if the token is valid, None if it doesn't exist
    """
    return db.query(TeamMember).filter(TeamMember.unique_link == token).first()


def is_survey_completed(db: Session, token: str) -> bool:
    """
    Verifies if a survey has been completed based on the token.

    Args:
        db: Database session
        token: Survey token

    Returns:
        True if the survey was completed, False if not
    """
    team_member = validate_survey_token(db, token)
    return team_member.has_completed if team_member else False