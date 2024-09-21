from dotenv import load_dotenv
from fastapi import FastAPI
from app.lib.controllers.chat_controller import router

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

app = create_app()