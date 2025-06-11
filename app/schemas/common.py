from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None


class SuccessResponse(BaseModel, Generic[T]):
    """Success response format matching frontend expectations"""
    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = False
    error: str
    message: Optional[str] = None
