from fastapi import APIRouter, HTTPException, Query
from ..database import db  # 초기화된 db 객체 가져오기
from ..models.video import Video
from bson import ObjectId  # MongoDB ObjectID 타입을 처리하기 위해 사용
from typing import List

router = APIRouter()

@router.get("/videos/", response_model=List[Video])
async def get_videos(
    youtuber: str = Query(..., description="유튜버 이름"),
    opening: str = Query(..., description="오프닝 이름"),
):
    """
    유튜버와 오프닝 이름으로 영상을 검색합니다.
    """
    # MongoDB에서 검색
    videos = list(
        db.videos.find(
            {"youtuber": youtuber, "opening": {"$regex": opening, "$options": "i"}}
        )
    )

    # 검색 결과가 없을 때 예외 처리
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found matching the criteria")

    # ObjectId는 JSON 직렬화가 안 되므로 문자열로 변환
    for video in videos:
        video["_id"] = str(video["_id"])

    return videos

@router.post("/videos/")
async def create_video(video: Video):
    db["videos"].insert_one(video.model_dump())
    return {"message": "Video added successfully"}

@router.delete("/videos/{video_id}")
async def delete_video(video_id: str):
    # ObjectId로 변환 가능한지 확인
    if not ObjectId.is_valid(video_id):
        raise HTTPException(status_code=400, detail="Invalid video ID format")

    # MongoDB에서 해당 ID의 비디오 삭제
    result = db["videos"].delete_one({"_id": ObjectId(video_id)})

    # 결과 확인
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Video not found")

    return {"message": "Video deleted successfully"}
