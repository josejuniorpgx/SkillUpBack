"""
Main API router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import surveys, responses
api_router = APIRouter()

api_router.include_router(surveys.router, prefix="/surveys", tags=["surveys"])
api_router.include_router(responses.router, prefix="/survey", tags=["responses"])