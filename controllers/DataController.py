from .BaseContoller import BaseController
from fastapi import UploadFile
from models import ResponceSignal
from .ProjectController import ProjectController
import re
import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576
        
    def validate_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False, ResponceSignal.FILE_TYPE_NOT_SUPPORTED.value
                
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponceSignal.FILE_SIZE_EXEEDED.value

        return True, ResponceSignal.FILE_UPLOAD_SUCCESS.value
    
    def clean_file_name(self, original_file_name: str):
        cleaned_name = re.sub(r'[^\w.]', '', original_file_name)
        cleaned_name = cleaned_name.replace(' ', '_')
        return cleaned_name
    
    def generate_unique_filename(self, original_file_name: str, project_id: str):
        rand_file_name = self.generate_rand_str()
        project_path = ProjectController().get_project_path(project_id=project_id)
        
        cleaned_file_name = self.clean_file_name(
            original_file_name=original_file_name
            )
        
        new_file_path = os.path.join(
            project_path,
            rand_file_name + '_' + cleaned_file_name,
        )
        
        while os.path.exists(new_file_path):
            rand_file_name = self.generate_rand_str()
            new_file_path = os.path.join(
                project_path,
                rand_file_name + '_' + cleaned_file_name,
            )

        return new_file_path