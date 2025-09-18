# This file defines the base API routes for the application using FastAPI.
from fastapi import FastAPI ,APIRouter
import os


# Create an API router with a prefix and tag for organization
router = APIRouter(
    prefix="/api/v1",
    tags=["api-v1"]
)

@router.get("/")
async def read_root():
    """
    Root endpoint that returns the application name and version.
    Retrieves values from environment variables.
    """
    app_name = os.getenv("app_name")
    app_version = os.getenv("app_version")
    return {"app_name": app_name, "app_version": app_version}

