import grpc
import ssdk_pb2
import ssdk_pb2_grpc
channel = grpc.insecure_channel('127.0.1.1:50051') 
stub = ssdk_pb2_grpc.CameraStub(channel)


number = ssdk_pb2.Number(value=2,name="temp")
response = stub.TakePhoto(number)
print(response.value) # not necesary but helpful for checking
