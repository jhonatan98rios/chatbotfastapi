from fastapi import HTTPException

class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Invalid request parameters"):
        super().__init__(status_code=400, detail=detail)