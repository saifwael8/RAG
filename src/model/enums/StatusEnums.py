from enum import Enum

class StatusEnums(Enum):

    FILE_TYPE_NOT_SUPPORTED = "File type is not supported"
    FILE_SIZE_EXCEEDED_LIMIT = "File size exceeded limit"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_UPLOADING_FAILED = "File failed to be uploaded"
    FILE_VALIDATION_SUCCESS = "File is successfully validated"