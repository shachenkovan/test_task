from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.db import get_db
from db.models.video_model import VideoStatus, Videos
from schemas.video_schema import VideoSchema

video_router = APIRouter(prefix='/videos')


@video_router.post('/add')
def post_videos(
        video_path: str,
        start_time: datetime,
        duration: int,
        camera_number: int,
        location: str,
        db: Session = Depends(get_db)
):
    try:
        video_data = VideoSchema(
            video_path=video_path,
            start_time=start_time,
            duration=duration,
            camera_number=camera_number,
            location=location
        )
        video = Videos(
            video_path=video_data.video_path,
            start_time=video_data.start_time,
            duration=video_data.duration,
            camera_number=video_data.camera_number,
            location=video_data.location
        )
        db.add(video)
        db.commit()
        db.refresh(video)
        return video
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при добавлении видео: {str(e)}"
        )


@video_router.get('/get')
def get_videos(
        status_filter: Optional[list[VideoStatus]] = Query(None),
        camera_number: Optional[list[int]] = Query(None),
        location: Optional[list[str]] = Query(None),
        start_time_from: Optional[datetime] = Query(None),
        start_time_to: Optional[datetime] = Query(None),
        db: Session = Depends(get_db)
):
    try:
        videos = db.query(Videos)

        filters = []
        if status_filter:
            filters.append(Videos.status.in_(status_filter))
        if camera_number:
            filters.append(Videos.camera_number.in_(camera_number))
        if location:
            filters.append(Videos.location.in_(location))
        if start_time_from:
            filters.append(Videos.start_time >= start_time_from)
        if start_time_to:
            filters.append(Videos.start_time <= start_time_to)

        if filters:
            videos = videos.filter(and_(*filters)).all()
        else:
            videos = videos.all()

        if not videos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Видео не найдено"
            )

        return videos
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении видео: {str(e)}"
        )


@video_router.get('/{video_id}')
def get_video_by_id(
        video_id: int,
        db: Session = Depends(get_db)
):
    try:
        video = db.query(Videos).filter(Videos.id == video_id).first()
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Видео не найдено"
            )
        return video
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении видео: {str(e)}"
        )


@video_router.patch('/{video_id}/status')
def patch_video_status(
        video_id: int,
        new_status: VideoStatus,
        db: Session = Depends(get_db)
):
    try:
        video = db.query(Videos).filter(Videos.id == video_id).first()
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Видео не найдено"
            )
        video.status = new_status
        db.commit()
        db.refresh(video)
        return video
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении статуса видео: {str(e)}"
        )
