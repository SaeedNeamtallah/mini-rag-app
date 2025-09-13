# main.py - Entry point for the FastAPI application
# This file initializes the FastAPI app and includes the routes
from fastapi import FastAPI
from routes.base import router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

app = FastAPI()
# Include routers from other modules
app.include_router(router)



# Running instructions:
# To run the application with auto-reload during development:
# uvicorn main:app --reload

# Access URLs:
# Swagger documentation: http://127.0.0.1:8000/docs
# Root endpoint: http://127.0.0.1:8000

# Network configuration options:
# To make the app accessible from other devices on the network:
# uvicorn main:app --host 0.0.0.0

# To change the default port (8000):
# uvicorn main:app --port 9000

