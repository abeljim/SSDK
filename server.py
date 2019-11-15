import grpc
from concurrent import futures
import time

import ssdk_pb2
import ssdk_pb2_grpc

import ssdk

class CameraServicer(ssdk_pb2_grpc.CameraServicer):
    def TakePhoto(self, request, context):
        response = ssdk_pb2.Number()
        response.value = ssdk.take_photo(request.value)
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

ssdk_pb2_grpc.add_CameraServicer_to_server(
        CameraServicer(), server)

print("Starting server. Listening on port 50051.")
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop()
