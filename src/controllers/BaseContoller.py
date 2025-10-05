from helper.config import get_settings, Settings
import os
import random
import string

class BaseController:
    # Constructor to initialize settings
    
    def __init__(self):
        self.app_settings: Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(
            self.base_dir,
            'assets/files'
        )
        
    def generate_rand_str(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
