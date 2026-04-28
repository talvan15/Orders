from concurrent import futures
import grpc

from generated import client_pb2, client_pb2_grpc

from app import crud, models
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


class ClientService(client_pb2_grpc.ClientServiceServicer):

    def CreateClient(self, request, context):
        db = SessionLocal()

        try:
            client = crud.create_client(
                db,
                name=request.name,
                email=request.email
            )

            return client_pb2.ClientResponse(
                id=client.id,
                name=client.name,
                email=client.email
            )

        finally:
            db.close()

    def GetClientById(self, request, context):
        db = SessionLocal()

        try:
            client = crud.get_client(db, request.id)

            if not client:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Client not found")
                return client_pb2.ClientResponse()

            return client_pb2.ClientResponse(
                id=client.id,
                name=client.name,
                email=client.email
            )

        finally:
            db.close()

    def ListClients(self, request, context):
        db = SessionLocal()

        try:
            clients = crud.get_clients(db)

            return client_pb2.ListClientsResponse(
                clients=[
                    client_pb2.ClientResponse(
                        id=c.id,
                        name=c.name,
                        email=c.email
                    )
                    for c in clients
                ]
            )

        finally:
            db.close()

    def UpdateClient(self, request, context):
        db = SessionLocal()

        try:
            client = crud.update_client(
                db,
                client_id=request.id,
                name=request.name,
                email=request.email
            )

            if not client:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Client not found")
                return client_pb2.ClientResponse()

            return client_pb2.ClientResponse(
                id=client.id,
                name=client.name,
                email=client.email
            )

        finally:
            db.close()

    def DeleteClient(self, request, context):
        db = SessionLocal()

        try:
            success = crud.delete_client(db, request.id)

            if not success:
                return client_pb2.DeleteClientResponse(
                    success=False,
                    message="Client not found"
                )

            return client_pb2.DeleteClientResponse(
                success=True,
                message="Client deleted successfully"
            )

        finally:
            db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    client_pb2_grpc.add_ClientServiceServicer_to_server(
        ClientService(),
        server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("Clients Service gRPC rodando na porta 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()