from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Tenta processar a requisição
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:  # Captura HTTPException padrão do FastAPI
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        except Exception as exc:  # Captura todas as outras exceções não tratadas
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
