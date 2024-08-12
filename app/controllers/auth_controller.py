# import sys

# sys.path.append('../app')
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import DataError
from app.services.auth_service import Auth, get_current_user
from app.schemas.auth_schema import RegisterSchema
from app.utils.api_response import ErrorResponse

router = APIRouter()


@router.post("/account/register")
def register(registerSchema: RegisterSchema):
    try:
        user_id = Auth.register(registerSchema.firstname, registerSchema.lastname, registerSchema.username,
                                registerSchema.password, registerSchema.email)
        if user_id:
            return {
                'id': user_id,
                'email': registerSchema.email,
                'name': registerSchema.firstname + " " + registerSchema.lastname,
                'username': registerSchema.username
            }
        else:
            return ErrorResponse(412, f"Please check the input")
    except DataError as e:
        return ErrorResponse(412, f"Unexpected error: {e}")


@router.post("/account/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = Auth.login_user({"username": form_data.username, "password": form_data.password})
        if res:
            return res
        else:
            return ErrorResponse(412, "Please check the input")
    except DataError as e:
        return ErrorResponse(412, f"Unexpected error: {e}")

    #     return res2
    # except DataError as e:
    #     return ErrorResponse(412, f"Unexpected error: {e}")


@router.get("/account/me")
def me(current_user: dict = Depends(get_current_user)):
    res = {
        "user": {
            "id": current_user["sub"],
            "email": current_user["email"],
            "name": current_user["name"]
        }
    }
    return res
