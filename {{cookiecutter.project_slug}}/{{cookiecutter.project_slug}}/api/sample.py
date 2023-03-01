from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims
from .app.auth import get_current_user

router = APIRouter(prefix="/user")


@router.get("/sample-restricted", dependencies=[Depends(get_current_user)])
def restricted():
    # ID Token is valid
    return "Hello"


@router.get("/sample-get-email")
def get_current_user_email(current_user: CognitoClaims = Depends(get_current_user)):
    # ID Token is valid, and getting user info
    return current_user.email
