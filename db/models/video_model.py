import enum
from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base


class VideoStatus(str, enum.Enum):
    new = 'new'
    transcoded = 'transcoded'
    recognized = 'recognized'


class Videos(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    video_path: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    duration: Mapped[int] = mapped_column(Integer)
    camera_number: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String(255))
    status: Mapped[VideoStatus] = mapped_column(default='new')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)



