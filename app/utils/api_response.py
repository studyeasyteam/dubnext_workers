from typing import Dict

from app.utils.constants import APIResponses


def success_response(msg: str, code: int = 200) -> (Dict[str, str], int):
    return {
        "status": APIResponses.SUCCESS.value,
        "message": msg,
    }, code


def fail_response(msg: str, code: int = 400) -> (Dict[str, str], int):
    return {
        "status": APIResponses.FAIL.value,
        "message": msg,
    }, code


def auth_error_response(code: int = 401) -> (Dict[str, str], int):
    return {
        "status": APIResponses.FAIL.value,
        "message": "User don't have access to the resource",
    }, code


class ErrorResponse:
    def __new__(cls, code, message, **kwargs):
        cls.code = code
        cls.message = message
        error_response = {"code": cls.code, "message": cls.message}
        error_response.update(kwargs)
        return error_response


class CustomErrorResponse(ErrorResponse):
    def __new__(cls, message, code, **kwargs):
        return {"error": super().__new__(cls, code, message, **kwargs)}
