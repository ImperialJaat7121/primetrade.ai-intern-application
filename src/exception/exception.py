import sys
from src.logging import logger

from src import logging
class AppException(Exception):
    def __init__(self, error_message, error_detail: sys):
        self.message = error_message
        _, _, exc_tb = error_detail.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in script: {self.filename} at line number: {self.lineno} with error message: {self.message}"
    