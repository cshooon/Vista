import os

from fastapi import APIRouter, File, UploadFile, Depends, Form
from openai import OpenAI
from database import MongoClient
from starlette.responses import JSONResponse, StreamingResponse

from settings import settings
from service.fastapi_auth import get_current_user
from vista.event_handler import generate_responses

router = APIRouter()
client = OpenAI(api_key=settings.OPEN_API_KEY)


@router.post('/create')
async def create(file: UploadFile = File(...), name: str = Form(...), user=Depends(get_current_user)):
    file_name = file.filename
    file_contents = await file.read()
    try:
        file = client.files.create(
            file=file_contents,
            purpose="assistants",
        )

        # 파일 시스템에 파일 저장 (file_id를 파일명으로 사용)
        file_path = f"static/files/{file.id}.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_contents)

        thread_response = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "file_ids": [file.id],
                    "content": "Follow following messages."
                }
            ]
        )
        thread_info = thread_response.model_dump()
        thread_id = thread_info['id']

        await MongoClient.get_client().chat.users.update_one(
            {"email": user['email']},
            {"$push": {"threads": {"thread_id": thread_id, "name": name, "file_name": [{file.id: file_name}],
                                   "messages": [{}]}}},
        )

        return {'thread_id': thread_id}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post('/create_example')
async def create_example(file_name: str = Form(...), name: str = Form(...), user=Depends(get_current_user)):
    try:
        file_id = None
        if file_name == 'cars.csv':
            file_id = 'file-MBaj0cR57iInT6lHhv7S67hz'
        elif file_name == 'housing.csv':
            file_id = 'file-wqrqSzlMC8lsjjfdtQJ9nnsF'
        elif file_name == 'Iris.csv':
            file_id = 'file-bYtSYvkZGRF3anUrtkkbuSSL'

        thread_response = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "file_ids": [file_id],
                    "content": "Follow following messages."
                }
            ]
        )
        thread_info = thread_response.model_dump()
        thread_id = thread_info['id']

        await MongoClient.get_client().chat.users.update_one(
            {"email": user['email']},
            {"$push": {"threads": {"thread_id": thread_id, "name": name, "file_name": [{file_id: file_name}],
                                   "messages": [{}]}}},
        )

        return {'thread_id': thread_id}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post('/chat')
async def create_chat(file: UploadFile = None, thread_id: str = Form(...),
                      message: str = Form(...), user=Depends(get_current_user)):
    if file:
        file_name = file.filename
        file_contents = await file.read()
        try:
            file = client.files.create(
                file=file_contents,
                purpose="assistants",
            )
            await MongoClient.get_client().chat.users.update_one(
                {"email": user['email'], "threads.thread_id": thread_id},
                {"$push": {"threads.$.file_name": {file.id: file_name}}}
            )
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message,
                file_ids=[file.id]
            )
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})
    else:
        try:
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message,
            )
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})
    try:
        generator = await generate_responses(
            client,
            thread_id=thread_id,
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

    return StreamingResponse(generator(), media_type="text/event-stream")
