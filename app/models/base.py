import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.connection import Base


class BaseModel(Base):
    """
    BaseModel class serves as an abstract base model for other database models.

    This class defines common attributes and behaviors for all models inheriting from it.
    It provides universally needed fields like `id`, creation timestamp, and update
    timestamp. It is meant to be used as a base class for concrete models in an
    application using SQLAlchemy. The abstract nature of the class ensures it is not
    directly used for table creation.

    :ivar id: Unique identifier for the model instance, represented as a UUID.
    :ivar created_at: Timestamp tracking the creation time of the record.
    :ivar updated_at: Timestamp tracking the last update time of the record.
    """
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"