import bcrypt
import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from pydantic import BaseModel

from database import MongoClient, Users
from settings import settings


router = APIRouter()


manager = LoginManager(settings.SECRET_KEY, token_url='/user/login')


async def get_current_user(request: Request):
    token_type = request.headers.get('token_type')
    authorization = request.headers.get('Authorization')
    _, token = authorization.split()
    if token_type == "Google":
        profile_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"},
        )
        if profile_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired Google access token")
        user_info = profile_response.json()
        user = await MongoClient.get_client().chat.users.find_one({"email": user_info['email']})
        user = jsonable_encoder(user, exclude={"_id"})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials or user not found")
        return user
    elif token_type == "Standard":
        user = await manager(request)
        user = jsonable_encoder(user, exclude={"_id"})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials or user not found")
        return user
    else:
        raise HTTPException(status_code=400, detail="Unsupported token type")


class RegisterBody(BaseModel):
    name: str
    email: str
    password: str


def hash_password(plain_password: str) -> str:
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@manager.user_loader()
async def load_user(email: str):
    user = await MongoClient.get_client().chat.users.find_one({"email": email})
    return user


@router.post("/user/register")
async def register(body: RegisterBody):
    # 이메일 중복 검사
    existing_user = await MongoClient.get_client().chat.users.find_one({"email": body.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The email address is already in use"
        )

    hashed_password = hash_password(body.password)
    user = Users(name=body.name, email=body.email, hashed_password=hashed_password, threads=[])
    await MongoClient.get_client().chat.users.insert_one(jsonable_encoder(user))
    return {"message": "User registered successfully"}


@router.post('/user/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await MongoClient.get_client().chat.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    access_token = manager.create_access_token(data=dict(sub=form_data.username))
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/user/protected')
async def protected_route(user=Depends(get_current_user)):
    return user
