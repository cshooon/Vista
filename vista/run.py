from fastapi import APIRouter
from openai import OpenAI

from .event_handler import generate_responses
from starlette.responses import StreamingResponse

from settings import settings

router = APIRouter()
client = OpenAI(api_key=settings.OPEN_API_KEY)


@router.get("/run")
async def test_gpt():
    empty_thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=empty_thread.id,
        role="user",
        content="hi!",
        attachments=[]
    )

    generator = await generate_responses(
        client,
        "asst_DLVaOcpVTqj7dCBsjyqzoloQ",
        empty_thread.id,
    )
    return StreamingResponse(generator(), media_type="text/event-stream")
