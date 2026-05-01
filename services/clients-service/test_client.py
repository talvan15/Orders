import grpc
from generated import client_pb2, client_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = client_pb2_grpc.ClientServiceStub(channel)

# CREATE
response = stub.CreateClient(
    client_pb2.CreateClientRequest(
        name="Lucas Campelo",
        email="lucas@email.com"
    )
)

print("CREATE:", response)

# LIST
response = stub.ListClients(client_pb2.Empty())
print("LIST:", response)

# GET
response = stub.GetClientById(
    client_pb2.GetClientByIdRequest(id=1)
)
print("GET:", response)

# UPDATE
response = stub.UpdateClient(
    client_pb2.UpdateClientRequest(
        id=1,
        name="Lucas Atualizado",
        email="lucas@novo.com"
    )
)
print("UPDATE:", response)

# DELETE
response = stub.DeleteClient(
    client_pb2.DeleteClientRequest(id=1)
)
print("DELETE:", response)