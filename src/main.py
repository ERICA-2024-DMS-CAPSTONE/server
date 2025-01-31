from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import cv2
import torch

# 모델 가져오기(수정 필요)
# from model import TmpModel

app = FastAPI()

# model = TmpModel()

# yolov5 사용
yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s')
yolo.to('cpu')

def detect_faces(frame):
    with torch.no_grad():
        results = yolo(frame)
    results = results.pandas().xyxy[0][['name','xmin','ymin','xmax','ymax']]
    # 사람만
    person_results = results[results['name'] == 'person']
    for num, i in enumerate(person_results.values):
                cv2.putText(frame, i[0], ((int(i[1]), int(i[2]))), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 255), 3)
                cv2.rectangle(frame, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)
    return frame

# 스트리밍 함수
def generate_frames():
    # 기본 카메라 사용
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = detect_faces(frame)
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