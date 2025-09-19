# main.py - Entry point for the FastAPI application
# This file initializes the FastAPI app and includes the routes
from fastapi import FastAPI
from routes import data ,base

# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv('.env')



app = FastAPI()

app.include_router(base.router )
app.include_router(data.data_router)




# Running instructions:
# To run the application with auto-reload during development:



# """"

#  uvicorn main:app --reload --host 127.0.0.1 --port 8000&'


# """""





# Access URLs:
# Swagger documentation: http://127.0.0.1:8000/docs
# Root endpoint: http://127.0.0.1:8000

# Network configuration options:
# To make the app accessible from other devices on the network:
# uvicorn main:app --host 0.0.0.0

# To change the default port (8000):
# uvicorn main:app --port 9000

