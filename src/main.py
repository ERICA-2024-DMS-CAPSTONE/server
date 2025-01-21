from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import cv2

# 모델 가져오기(수정 필요)
# from model import TmpModel

app = FastAPI()

# model = TmpModel()

# 스트리밍 함수
def generate_frames():
    # 기본 카메라 사용
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        # 프레임을 JPEG로 인코딩
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        # HTTP 응답 형식으로 프레임 반환
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )
    cap.release()

@app.get("/video")
async def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )