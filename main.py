from fastapi import FastAPI

from api import video_router

app = FastAPI(
    title='Тестовое задание',
    description='Сервис является простой оберткой над'
                ' БД PostgreSQL и предоставляет методы для добавления,'
                ' получения и обновления информации о видео.')

app.include_router(video_router, tags=['Видео'])


@app.get('/')
def root():
    return {'message': 'App is running.'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
