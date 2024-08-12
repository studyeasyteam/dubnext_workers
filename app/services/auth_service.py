# api/services/auth_service.py
from fastapi import Depends, HTTPException
from keycloak import KeycloakOpenID, KeycloakGetError
import traceback
from app.config import Config
from keycloak import KeycloakAdmin
from app.utils.api_response import CustomErrorResponse
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/account/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        keycloak_openid = Auth.get_keycloak_openid()
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except KeycloakGetError as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


class Auth:
    KEYCLOAK_SERVER_URL = Config.KEYCLOAK_SERVER_URL
    KEYCLOAK_CLIENT_ID = Config.KEYCLOAK_CLIENT_ID
    KEYCLOAK_REALM_NAME = Config.KEYCLOAK_REALM_NAME
    KEYCLOAK_CLIENT_SECRET_KEY = Config.KEYCLOAK_CLIENT_SECRET_KEY

    @staticmethod
    def get_keycloak_openid():
        return KeycloakOpenID(server_url=Auth.KEYCLOAK_SERVER_URL,
                              client_id=Auth.KEYCLOAK_CLIENT_ID,
                              realm_name=Auth.KEYCLOAK_REALM_NAME,
                              client_secret_key=Auth.KEYCLOAK_CLIENT_SECRET_KEY,
                              verify=True)

    @staticmethod
    def login_user(data):
        try:
            # Keycloak Configuration
            keycloak_openid = Auth.get_keycloak_openid()
            token = keycloak_openid.token(data.get("username"), data.get("password"))
            roles = keycloak_openid.introspect(token['access_token'])['realm_access']['roles']
            if token:
                # Return the access token to the client
                return {
                    "status": "success",
                    "message": "Successfully logged in.",
                    "refresh_token": token['refresh_token'],
                    "access_token": token['access_token'],
                    "token_type": "bearer",
                    "user": data.get("username"),
                    "roles": roles

                }

            else:
                return (
                    CustomErrorResponse("Email or password does not match.", 401),
                    401,
                )

        except Exception as e:
            var = traceback.format_exc()
            print(f"Traceback login API: --> {var}")
            return (
                CustomErrorResponse(412, f"Unable to log in ! Please try again"),
                412,
            )

    @staticmethod
    def logout_user(request):
        keycloak_openid = Auth.get_keycloak_openid()
        if request.headers.get("refresh_token"):
            try:
                keycloak_openid.logout(request.headers.get("refresh_token"))
            except Exception as e:
                return {"status": "failed",
                        "message": "Invalid refresh token"}, 400

            return {"status": "success",
                    "message": "Logout successfully"}, 200
        else:
            return (
                CustomErrorResponse(412, f"Refresh token missing"),
                412,
            )

    @staticmethod
    def get_user_info(request):
        try:
            # Keycloak Configuration
            keycloak_openid = Auth.get_keycloak_openid()

            if request.headers.get("Authorization"):
                auth_token = request.headers.get("Authorization").split(" ")[1]
            else:
                auth_token = ""
            if auth_token:
                user = keycloak_openid.userinfo(auth_token)
                if user:
                    return keycloak_openid.userinfo(auth_token)
                else:
                    return False
            else:
                return False

        except Exception as e:
            print("Provide a valid auth token.", e)
            return False

    @staticmethod
    def register(firstname, lastname, username, password, email):
        try:
            keycloak_admin = KeycloakAdmin(server_url=Config.KEYCLOAK_SERVER_URL,
                                           username=Config.KEYCLOAK_MAKE_USER_USERNAME,
                                           password=Config.KEYCLOAK_MAKE_USER_PASSWORD,
                                           realm_name=Config.KEYCLOAK_REALM_NAME,
                                           verify=True)
            user_attributes = {
                "username": username,
                "email": email,
                "enabled": True,
                "emailVerified": True,
                "firstName": firstname,
                "lastName": lastname,
                "credentials": [{"type": "password", "value": password}]
            }
            user_id = keycloak_admin.create_user(user_attributes)
            return user_id
        except Exception as e:
            print("Provide a valid auth token.", e)
            return False
