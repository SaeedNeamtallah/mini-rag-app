import string
from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import uuid, os, re, time
import random

import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile) -> bool:

        allowed_types = self.app_settings.FILE_ALLOWED_TYPES
        max_size = self.app_settings.FILE_MAX_SIZE * 1024 * 1024  # Convert MB to bytes

        if file.content_type not in allowed_types:
            return False ,ResponseSignal.FILE_TYPE_NOT_ALLOWED.value # value to get the string representation of the enum why? Because we want to return a user-friendly message.

        if file.size > max_size:
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True , ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value   






    # def generate_unique_filename(self, original_filename: str, project_id: str) -> str:
    #     project_path = ProjectController().get_project_path(project_id)
    #     cleaned_file_name = self.get_clean_file_name(original_filename)

    #     while True:
    #         random_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    #         new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_file_name}")

    #         if not os.path.exists(new_file_path):
    #             return new_file_path

    # def get_clean_file_name(self, orig_file_name: str) -> str:
    #     cleaned_file_name = re.sub(r"[^\w. ]", "", orig_file_name.strip())
    #     return cleaned_file_name.replace(" ", "_")


    # organic one


    def generate_unique_filename(self, original_filename: str, project_id: str) -> str:

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)
        cleaned_file_name = self.get_clean_file_name(original_filename)
        new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_file_name}")

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_file_name}")


        return new_file_path
    




    def get_clean_file_name(self, orig_file_name: str) -> str:
        # remove special characters except underscore, dot, and space
        cleaned_file_name = re.sub(r"[^\w. ]", "", orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name






    # async def upload_data(self, project_id: str, file: UploadFile):
    #     upload_dir = self.app_settings.upload_directory
    #     project_dir = os.path.join(upload_dir, project_id)

    #     if not os.path.exists(project_dir):
    #         os.makedirs(project_dir)

    #     file_location = os.path.join(project_dir, file.filename)

    #     with open(file_location, "wb") as buffer:
    #         buffer.write(await file.read())

    #     return {"info": f"file '{file.filename}' saved at '{file_location}'"}

