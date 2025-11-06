from src.helper.config import get_settings, Settings
import os

class BaseController():

    def __init__(self):
        self.app_settings = get_settings()
        self.parent_dir = os.path.dirname(__file__)
        self.parent_of_parent_dir = os.path.dirname(self.parent_dir)
        self.project_dir = os.path.join(
            self.parent_of_parent_dir,
            "assets/files"
        )