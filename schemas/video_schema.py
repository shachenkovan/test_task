from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from db.models.video_model import VideoStatus


class VideoSchema(BaseModel):
    video_path: str = Field(description='Путь к видео')
    start_time: datetime = Field(description='Время начала видео')
    duration: int = Field(gt=0, description='Длительность видео в секундах')
    camera_number: int = Field(gt=0, description='Номер камеры')
    location: str = Field(description='Местоположение камеры')
    status: Optional[VideoStatus | None] = Field(default='new', description='Статус видео')


