from fastapi import FastAPI
from routers import video

app = FastAPI()

# 라우터 등록
app.include_router(video.router)