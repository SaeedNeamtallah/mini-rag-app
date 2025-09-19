from helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:
    def __init__(self):
        self.app_settings: Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(self.base_dir, 'assets/files')

        # os.makedirs(self.file_dir, exist_ok=True)

    def generate_random_string(self, length=12):

        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))