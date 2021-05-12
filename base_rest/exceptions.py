"""
author: Sanidhya Mangal
github:sanidhyamangal
"""
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class BaseValidationError(APIException):
    """Custom Validation for bool status."""
    def __init__(self, detail=None, status_code=None):
        """"Default."""
        if status_code:
            self.status_code = status_code
        else:
            self.status_code = HTTP_400_BAD_REQUEST
        if detail:
            self.detail = {'status': False, 'message': detail, 'data': {}}
