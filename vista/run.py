from fastapi import APIRouter
from openai import OpenAI
from .event_handler import generate_responses
from starlette.responses import StreamingResponse

from settings import settings

router = APIRouter()
client = OpenAI(api_key=settings.OPEN_API_KEY)


@router.get("/run")
async def test_gpt():
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "file_ids": ['file-RizaJySrKNS5vQCwrXTGqSM1'],
                "content": "It's csv file. give me visualizations"
            }
        ]
    )
    generator = await generate_responses(
        client,
        thread.id,

    )
    return StreamingResponse(generator(), media_type="text/event-stream")
