from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from ..config.settings import settings
from ..routes import videos

ADMIN_TOKEN = settings.admin_token

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # 자동 생성 비활성화

app.include_router(videos.router)

# 인증 함수
def check_admin_token(request: Request):
    token = request.headers.get("X-Admin-Token")
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")

# OpenAPI 스키마 생성
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ChessList API",
        version="1.0.0",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema