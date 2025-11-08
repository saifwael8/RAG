from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from src.model import StatusEnums
import re
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_file(self, file: UploadFile):
        to_MB = 1024*1024
        if file.content_type not in self.app_settings.SUPPORTED_FILE_TYPES:
            return False, StatusEnums.FILE_TYPE_NOT_SUPPORTED
        
        if file.size > self.app_settings.MAX_FILE_SIZE*to_MB:
            return False, StatusEnums.FILE_SIZE_EXCEEDED_LIMIT
        
        return True, StatusEnums.FILE_VALIDATION_SUCCESS

    def clean_filename(self, orig_filename: str):
        cleaned_filename = cleaned_filename.replace(" ", "_")
        cleaned_filename = re.sub(r'[^\w.]', '', orig_filename.strip()) #deletes characters other than letters, numbers, underscore and .
        return cleaned_filename

    def generate_unique_filename_and_return_path(self, file: UploadFile, project_id: str):
        project_path = ProjectController().get_project_dir_path(project_id=project_id)

        cleaned_filename = self.clean_filename(orig_filename=file.filename)

        new_filename = BaseController().generate_random_string() + "_" + cleaned_filename

        new_file_path = os.path.join(
            project_path,
            new_filename
        )

        while os.path.exists(new_file_path):
            new_filename = BaseController().generate_random_string() + "_" + cleaned_filename

            new_file_path = os.path.join(
                project_path,
                new_filename
            )

        return new_file_path


    