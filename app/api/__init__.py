"""
API package
"""


# FILE: app/main.py (UPDATE)
"""
FastAPI application main file - UPDATE to include API routes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.v1.api import api_router

settings = get_settings()

app = FastAPI(
    title="Leadership Feedback Survey API",
    description="AI-driven leadership feedback survey tool backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Leadership Feedback Survey API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
