from dotenv import load_dotenv
from fastapi import FastAPI
from app.lib.controllers.chat_controller import router
from app.lib.database.mongo_db_connection import lifespan
from app.lib.errors.middleware import ErrorHandlingMiddleware

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    app.add_middleware(ErrorHandlingMiddleware)
    return app

app = create_app()