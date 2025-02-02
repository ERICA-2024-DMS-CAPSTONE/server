from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.video_service import generate_frames

router = APIRouter()

@router.get("/video")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
