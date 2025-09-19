# This file defines the base API routes for the application using FastAPI.
from fastapi import FastAPI ,APIRouter,Depends
from helpers.config import get_settings,Settings
import os


# Create an API router with a prefix and tag for organization
router = APIRouter(
    prefix="/api/v1",
    tags=["api-v1"]
)

@router.get("/")
async def read_root(app_settings: Settings = Depends(get_settings)):
    """
    Root endpoint that returns the application name and version.
    Retrieves values from environment variables.
    """

    # app_settings = get_settings()

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {"app_name": app_name,
            "app_version": app_version}
