from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from .config.settings import settings
from .routes import videos
from .utils.helpers import check_admin_token, custom_openapi

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # 자동 경로 비활성화

app.include_router(videos.router)

origins = [
    "https://chesslist-frontend.vercel.app",  # ✅ 네 프론트 주소를 정확히 넣기
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 모든 도메인 허용 (개발 중에만 사용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.debug:
    print("Debug mode is enabled")

@app.get("/")
async def root():
    return {"message": "Welcome to ChessList!"}

# Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(request: Request):
    check_admin_token(request)  # 인증 확인
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")

# OpenAPI JSON
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi_json(request: Request):
    check_admin_token(request)  # 인증 확인
    return custom_openapi()

# ReDoc
@app.get("/redoc", include_in_schema=False)
async def custom_redoc(request: Request):
    check_admin_token(request)  # 인증 확인
    return get_redoc_html(openapi_url="/openapi.json", title="Custom ReDoc UI")