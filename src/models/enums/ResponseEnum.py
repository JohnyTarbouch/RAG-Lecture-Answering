from enum import Enum

class ResponceSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = 'File type not supported. Please choose txt or pdf'
    FILE_SIZE_EXEEDED = 'Upload file size exceeds 10 MB'
    FILE_UPLOAD_SUCCESS = 'File successfully uploaded'
    FILE_UPLOAD_FAILED = 'File upload failed'
    FILE_PROCESSING_FAILED = 'File processing failed'