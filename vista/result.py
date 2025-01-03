from fastapi import APIRouter, Depends
from openai import OpenAI

from database import MongoClient
from settings import settings
from service.fastapi_auth import get_current_user

router = APIRouter()
client = OpenAI(api_key=settings.OPEN_API_KEY)


@router.get('/chat-list')
async def chat_list(user=Depends(get_current_user)):
    threads = user['threads']
    return threads


# TODO user file name 불러오는 logic
@router.get('/user_file')
async def user_file(thread_id: str, user=Depends(get_current_user)):
    file_name = next((thread['file_name'] for thread in user['threads'] if thread['thread_id'] == thread_id), None)
    return file_name


@router.get('/file-store')
async def file_store(thread_id: str):
    thread_messages = client.beta.threads.messages.list(thread_id)
    file_ids = []
    for message in thread_messages.data:
        if message.role == 'user':
            break
        for content in message.content:
            if content.type == 'image_file':
                file_ids.append(content.image_file.file_id)
                if content.image_file.file_id:
                    image_file = client.files.with_raw_response.retrieve_content(content.image_file.file_id)
                    with open(f"static/images/{content.image_file.file_id}.png", "wb") as f:
                        f.write(image_file.content)

    return file_ids


@router.get('/db-store')
async def db_store(thread_id: str, user=Depends(get_current_user)):
    thread_messages = client.beta.threads.messages.list(thread_id)
    messages = []

    # JSON 데이터 파싱
    for message in thread_messages.data:
        new_message = {
            "role": message.role,
            "text": None,
            "file_id": [],
        }

        for user_file_object in message.attachments:
            new_message['file_id'].append(user_file_object.file_id)

        # output
        for content in message.content:
            if content.type == 'image_file':
                new_message['file_id'].append(content.image_file.file_id)
            elif content.type == 'text':
                new_message['text'] = content.text.value

        messages.append(new_message)

    # MongoDB에 새로운 thread 추가
    result = await MongoClient.get_client().chat.users.update_one(
        {"email": user['email'], "threads.thread_id": thread_id},
        {"$set": {"threads.$.messages": messages}}
    )

    if result.modified_count > 0 or result.matched_count > 0:
        return messages
    else:
        return f"Failed to add message to thread {thread_id} for user {user['email']}."
