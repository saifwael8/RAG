from .BaseController import BaseController
from fastapi import UploadFile
from src.model import StatusEnums


class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_file(self, file: UploadFile):
        to_MB = 1024*1024
        if file.content_type not in self.app_settings.SUPPORTED_FILE_TYPES:
            return False, StatusEnums.FILE_TYPE_NOT_SUPPORTED
        
        if file.size > self.app_settings.MAX_FILE_SIZE*to_MB:
            return False, StatusEnums.FILE_SIZE_EXCEEDED_LIMIT
        
        return True, StatusEnums.FILE_UPLOADED_SUCCESSFULLY
