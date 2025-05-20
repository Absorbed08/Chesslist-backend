from pydantic import BaseModel

class Video(BaseModel):
    youtuber: str
    opening: str
    url: str
    thumbnail: str
    title: str
    date: str
