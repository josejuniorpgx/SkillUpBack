import os
import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))
from app.database.connection import engine, Base
from app.models import *  # Import all Models
from scripts.seed_data import seed_questions
from app.database.session import SessionLocal


def create_database():
    """
    Creates and initializes the database tables using SQLAlchemy metadata.

    This function is responsible for creating all database tables defined in
    the SQLAlchemy model metadata associated with the Base object. After
    successfully creating the tables, it outputs the list of created tables
    to the console for verification.

    :raises RuntimeError: If the database engine fails to bind metadata or
        table creation encounters errors.

    :return: None
    """
    print("🏗️ Creating Databases...")
    # Create All tables in the database
    Base.metadata.create_all(bind=engine)
    # Show created tables
    table_names = Base.metadata.tables.keys()
    print(f"Tables Created: {', '.join(table_names)}")


def init_database():
    """
    Initializes the database by creating necessary tables and executing seed data.
    This process includes creating database schemas and populating the database
    with initial data. The function ensures that the database is ready for use
    after initialization.

    :raises Exception: Raised if there is an issue with seeding or interacting
        with the database.

    :return: None
    """
    print("🚀 Initializing Database...")

    # 1. Create database tables
    create_database()

    # 2. Execute seed
    db = SessionLocal()
    try:
        seed_questions(db)
    finally:
        db.close()

    print("Database Initialized Correctly!")


def reset_database():
    """
    Resets the database by dropping all tables and reinitializing it.

    This function provides a prompt to confirm the user's action before proceeding
    to delete all the database tables. It is intended for scenarios where the
    database needs to be completely reset.

    :raises SystemExit: Raised when the operation is canceled by the user.
    """
    print("⚠️  WARNING: This will delete all the database!")
    response = input("Are you sure to continue? (y/N): ")

    if response.lower() != 'y':
        print("❌ Operation Cancelled.")
        return

    print("🗑️  Deleting all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables eliminated!")
    # Re-initialize the database    init_database()


def main():
    """
    Main function responsible for handling database-related operations based on
    the command-line arguments provided. This script allows for database
    initialization, resetting, and seeding. If no command is specified, it
    defaults to initializing the database.

    Commands:
      - "init": Initializes the database.
      - "reset": Resets the database.
      - "seed": Executes the database seeding process.

    The function interacts with the database through helper methods such as
    `reset_database`, `init_database`, and `seed_questions`. When seeding, it
    establishes and closes a database session.

    :raises SystemExit: If an unrecognized command is provided, an error
        message is displayed, and the script exits after showing valid commands.
    """
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "reset":
            reset_database()
        elif command == "init":
            init_database()
        elif command == "seed":
            db = SessionLocal()
            try:
                seed_questions(db)
            finally:
                db.close()
        else:
            print("❌ Unrecognized command.")
            print("Available commands:")
            print("  python scripts/init_db.py init   - Initialize database")
            print("  python scripts/init_db.py reset  - Reset database")
            print("  python scripts/init_db.py seed   - Only execute seed")
    else:
        # Default, initialize
        init_database()


if __name__ == "__main__":
    main()