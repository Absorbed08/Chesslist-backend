from pymongo import MongoClient
from .config.settings import settings

# MongoDB 클라이언트 초기화
client = MongoClient(settings.mongodb_uri)

# 사용할 데이터베이스 선택
db = client.chesslist
