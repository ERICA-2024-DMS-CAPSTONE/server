import cv2
import torch
import time
from collections import deque
# from models.drowsiness_model import DrowsinessModel

# YOLO 모델 로드
yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s').to('cpu')

# 졸음 감지 모델
# model = DrowsinessModel()

input_frames = deque(maxlen=3)
drowsy_start_time = None
driver_state = 'normal'

# def update_state(frame):
#     global input_frames, drowsy_start_time, driver_state
     
#     input_frames.append(frame)

#     if len(input_frames) == 3:
#         state = model(input_frames)

#         if state == 'drowsy':
#             if drowsy_start_time is None:
#                 drowsy_start_time = time.time()
#                 elapsed_time = time.time() - drowsy_start_time

#                 if elapsed_time < 2:
#                     driver_state = 'normal'
#                 elif 2 <= elapsed_time < 4:
#                     driver_state = 'dangerous'
#                 else:
#                     driver_state = 'very dangerous'

#         else:
#             drowsy_start_time = None
#             driver_state = 'normal'

#     return driver_state

def detect_faces(frame):
    with torch.no_grad():
        results = yolo(frame)
    results = results.pandas().xyxy[0][['name','xmin','ymin','xmax','ymax']]
    person_results = results[results['name'] == 'person']
    for _, i in person_results.iterrows():
        cv2.putText(frame, i['name'], (int(i['xmin']), int(i['ymin'])), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        cv2.rectangle(frame, (int(i['xmin']), int(i['ymin'])), (int(i['xmax']), int(i['ymax'])), (0, 0, 255), 3)
    return frame
