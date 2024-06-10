from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import database
import vista
import service


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:3000"
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(database.router)
app.include_router(service.fastapi_auth_router)
app.include_router(service.google_auth_router)
app.include_router(vista.run_router)
app.include_router(vista.chat_router)
app.include_router(vista.result_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
