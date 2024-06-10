import requests
from fastapi import APIRouter
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

from database import MongoClient, Users
from service.fastapi_auth import hash_password
from settings import settings

router = APIRouter()
oauth = OAuth()


@router.get("/google/login")
async def google_login():
    url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?access_type=offline"
        "&prompt=consent"
        "&response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        "&scope=openid%20email%20profile"
    )

    return RedirectResponse(url)


@router.get("/callback")
async def callback(code: str):
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent",
        "grant_type": "authorization_code",
    }

    response = requests.post(settings.GOOGLE_TOKEN_ENDPOINT, data=token_data)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange authorization code for tokens",
        )

    token_response = response.json()
    access_token = token_response.get("access_token")
    refresh_token = token_response.get("refresh_token")
    profile_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_data = profile_response.json()
    user = await MongoClient.get_client().chat.users.find_one({"email": profile_data['email']})
    if not user:
        hashed_password = hash_password('google')
        user = Users(name=profile_data['name'], email=profile_data['email'], hashed_password=hashed_password,
                     threads=[])
        await MongoClient.get_client().chat.users.insert_one(jsonable_encoder(user))
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/google/userinfo")
async def userinfo(access_token: str):
    profile_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_data = profile_response.json()
    return profile_data
