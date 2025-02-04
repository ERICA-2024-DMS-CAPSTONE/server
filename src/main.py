import threading
import grpc
from fastapi import FastAPI
from protos import Service_pb2, Service_pb2_grpc
from concurrent import futures
from services.info_service import InfoService
from routers import video

app = FastAPI()

app.include_router(video.router)

# gRPC 서비스 핸들러
class InfoServiceHandler(Service_pb2_grpc.InfoServiceServicer):
    def __init__(self):
        self.service = InfoService()

    def FetchInfo(self, request, context):
        for info in self.service.fetch_info():
            yield info

    def UpdateInfo(self, request, context):
        self.service.update_info(request)
        return Service_pb2.Empty()

    def Offer(self, request, context):
        return self.service.offer(request)


def start_grpc_server():
    """gRPC 서버 실행"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_InfoServiceServicer_to_server(InfoServiceHandler(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC 서버 실행 중 (포트 50051)")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    # gRPC 서버를 백그라운드 스레드로 실행
    grpc_thread = threading.Thread(target=start_grpc_server, daemon=True)
    grpc_thread.start()

    # FastAPI 서버 실행
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
