from dotenv import load_dotenv
from fastapi import FastAPI
from app.lib.controllers.chat_controller import router
from app.lib.controllers.chat_controller import lifespan

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app

app = create_app()