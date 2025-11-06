from .BaseController import BaseController
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()


    def get_project_dir_path(self, project_id: str):
        folder_path = os.path.join(
            self.project_dir,
            project_id
        ) 
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path
