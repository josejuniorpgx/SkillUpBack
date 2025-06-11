from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="AI-driven leadership feedback survey tool backend",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Leadership Feedback Survey API",
        "version": "0.1.0",
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# TODO: Add Routes
# from app.api.v1.api import api_router
# app.include_router(api_router, prefix=settings.API_V1_STR)
