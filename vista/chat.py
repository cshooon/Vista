import os

from fastapi import APIRouter, Depends, Form, UploadFile, File
from openai import OpenAI
from database import MongoClient
from starlette.responses import JSONResponse, StreamingResponse

from settings import settings
from service.fastapi_auth import get_current_user
from vista.event_handler import generate_responses

router = APIRouter()
client = OpenAI(api_key=settings.OPEN_API_KEY)


@router.post('/create-chat')
async def create_chat(file: UploadFile = File(...), name: str = Form(...), user=Depends(get_current_user)):
    file_name = file.filename
    file_contents = await file.read()
    try:
        file_object = client.files.create(
            file=(file_name, file_contents),
            purpose="assistants",
        )

        # 파일 시스템에 파일 저장 (file_id를 파일명으로 사용)
        file_path = f"static/files/{file_object.id}.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_contents)

        thread = client.beta.threads.create(messages=[
            {"role": "user",
             "content": "visualize following csv file",
             "attachments": [{"file_id": file_object.id, "tools": [{"type": "code_interpreter"}]}]
             }
        ])
        await MongoClient.get_client().chat.users.update_one(
            {"email": user['email']},
            {"$push": {"threads": {"assistant_id": settings.ASSISTANT_ID, "file_name": [{file_object.id: file_name}],
                                   "thread_id": thread.id,
                                   "name": name,
                                   "messages": [{}]}}},
        )
        return {"thread_id": thread.id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post('/create-chat-example')
async def create_chat_example(csv_name: str = Form(...), user=Depends(get_current_user)):
    file_id = None
    if csv_name == 'shopping_trends.csv':
        file_id = 'file-9KpfhJkEcugGwbq6vGzSH4'
    elif csv_name == 'london_houses.csv':
        file_id = 'file-QXw27DZEUu1eTJ9LeJZkEz'
    elif csv_name == 'iris.csv':
        file_id = 'file-8SQdjo4u5oc8CuNWV3W1bc'
    thread = client.beta.threads.create(messages=[
        {"role": "user", "content": "give me visualization",
         "attachments": [{"file_id": file_id, "tools": [{"type": "code_interpreter"}]}]
         }])

    await MongoClient.get_client().chat.users.update_one(
        {"email": user['email']},
        {"$push": {"threads": {"assistant_id": settings.ASSISTANT_ID, "file_name": [{file_id: csv_name}],
                               "thread_id": thread.id, "name": csv_name,
                               "messages": [{}]
                               }
                   }},
    )

    return {"thread_id": thread.id}


@router.post('/continue-chat')
async def resume(file: UploadFile = None, thread_id: str = Form(...),
                 message: str = Form(...), user=Depends(get_current_user)):
    thread = None
    if file:
        file_name = file.filename
        file_contents = await file.read()
        file_object = client.files.create(
            file=(file_name, file_contents),
            purpose="assistants",
        )

        await MongoClient.get_client().chat.users.update_one(
            {"email": user['email'], "threads.thread_id": thread_id},
            {"$push": {"threads.$.file_name": {file_object.id: file_name}}}
        )

        thread = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
            attachments=[{"file_id": file_object.id, "tools": [{"type": "code_interpreter"}]}],
        )

    else:
        thread = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
            attachments=[],
        )
    if not thread:
        return JSONResponse(status_code=500, content={"message": "thread is None!"})

    generator = await generate_responses(
        client,
        settings.ASSISTANT_ID,
        thread_id,
    )
    return StreamingResponse(generator(), media_type="text/event-stream")


