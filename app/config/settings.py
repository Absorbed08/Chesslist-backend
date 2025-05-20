from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str  # MongoDB 연결 URI
    debug: bool = False  # 디버그 모드
    admin_token: str

    class Config:
        env_file = ".env"  # 환경 변수 파일 위치

# 설정 인스턴스 생성
settings = Settings()