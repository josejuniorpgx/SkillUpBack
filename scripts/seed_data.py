"""
Script to insert initial data into the database.
It runs after creating migrations to insert the 3 predefined questions.
"""

import asyncio
from sqlalchemy.orm import Session
from app.database.connection import engine
from app.database.session import SessionLocal
from app.models.question import SurveyQuestion


def seed_questions(db: Session):
    """
    Insert the 3 predefined questions into the database.
    """
    print("🌱 Starting seed of predefined questions...")

    # Check if questions already exist
    existing_questions = db.query(SurveyQuestion).count()

    if existing_questions > 0:
        print(f"✅ {existing_questions} questions already exist in the database. Skipping seed.")
        return

    # Get predefined questions from the model
    default_questions = SurveyQuestion.get_default_questions()

    # Create the questions
    for question_data in default_questions:
        question = SurveyQuestion(**question_data)
        db.add(question)

    # Save to database
    db.commit()

    print(f"✅ {len(default_questions)} predefined questions were inserted:")

    # Show inserted questions
    for i, question_data in enumerate(default_questions, 1):
        print(f"   {i}. {question_data['question_text']}")

    print("🎉 Seed completed successfully!")


def main():
    """
    Main function to execute the seed.
    """
    print("🚀 Starting database seed process...")

    # Create database session
    db = SessionLocal()

    try:
        # Execute questions seed
        seed_questions(db)

    except Exception as e:
        print(f"❌ Error during seed: {e}")
        db.rollback()
        raise

    finally:
        db.close()
        print("🔒 Database session closed.")


if __name__ == "__main__":
    main()