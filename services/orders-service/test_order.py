import grpc
from app import order_pb2, order_pb2_grpc

channel = grpc.insecure_channel("localhost:50052")
stub = order_pb2_grpc.OrderServiceStub(channel)

response = stub.ListOrders(order_pb2.Empty())

print(response)