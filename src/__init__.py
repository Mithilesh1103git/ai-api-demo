from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api_server import main_api_router
from dotenv import load_dotenv

load_dotenv(dotenv_path=r".env")

app = FastAPI()

origins = [
    "http://localhost:80",
    "http://127.0.0.1:80",
    "http://0.0.0.0:80",
    "http://my.dev.experiments:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_api_router)