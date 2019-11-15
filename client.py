import grpc
import calculator_pb2
import calculator_pb2_grpc

channel = grpc.insecure_channel('127.0.1.1:50051')

stub = calculator_pb2_grpc.CalculatorStub(channel)

number = calculator_pb2.Number(value=16)

response = stub.SquareRoot(number)
print(response.value)
