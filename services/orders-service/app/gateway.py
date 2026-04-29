from fastapi import FastAPI
import grpc

from . import order_pb2
from . import order_pb2_grpc

app = FastAPI()

channel = grpc.insecure_channel("localhost:50052")
stub = order_pb2_grpc.OrderServiceStub(channel)


@app.get("/orders")
def list_orders():
    response = stub.ListOrders(order_pb2.Empty())

    return [
        {
            "id": o.id,
            "client_id": o.client_id,
            "product_id": o.product_id,
            "quantity": o.quantity
        }
        for o in response.orders
    ]


@app.post("/orders")
def create_order(data: dict):
    response = stub.CreateOrder(
        order_pb2.OrderRequest(
            client_id=data["client_id"],
            product_id=data["product_id"],
            quantity=data["quantity"]
        )
    )

    return {
        "id": response.id,
        "client_id": response.client_id,
        "product_id": response.product_id,
        "quantity": response.quantity
    }