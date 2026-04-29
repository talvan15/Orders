from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import grpc
import requests

from . import order_pb2
from . import order_pb2_grpc

app = FastAPI(title="Orders Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

channel = grpc.insecure_channel("localhost:50052")
stub = order_pb2_grpc.OrderServiceStub(channel)

CLIENTS_URL = "http://127.0.0.1:8000"
PRODUCTS_URL = "http://127.0.0.1:8000/api/v1"


@app.get("/orders/")
def fetch_orders():
    response = stub.ListOrders(order_pb2.Empty())

    orders = []

    for order in response.orders:
        client_name = ""
        product_name = ""

        try:
            client_response = requests.get(
                f"{CLIENTS_URL}/clients/{order.client_id}"
            )

            if client_response.status_code == 200:
                client_name = client_response.json()["name"]

        except:
            client_name = "Cliente não encontrado"

        try:
            product_response = requests.get(
                f"{PRODUCTS_URL}/products/{order.product_id}/"
            )

            if product_response.status_code == 200:
                product_name = product_response.json()["name"]

        except:
            product_name = "Produto não encontrado"

        orders.append({
            "id": order.id,
            "client_id": order.client_id,
            "client_name": client_name,
            "product_id": order.product_id,
            "product_name": product_name,
            "quantity": order.quantity
        })

    return orders


@app.get("/orders/{id}/")
def fetch_order(id: int):
    response = stub.GetOrder(order_pb2.OrderId(id=id))

    client_name = ""
    product_name = ""

    try:
        client_response = requests.get(
            f"{CLIENTS_URL}/clients/{response.client_id}"
        )

        if client_response.status_code == 200:
            client_name = client_response.json()["name"]

    except:
        client_name = "Cliente não encontrado"

    try:
        product_response = requests.get(
            f"{PRODUCTS_URL}/products/{response.product_id}/"
        )

        if product_response.status_code == 200:
            product_name = product_response.json()["name"]

    except:
        product_name = "Produto não encontrado"

    return {
        "id": response.id,
        "client_id": response.client_id,
        "client_name": client_name,
        "product_id": response.product_id,
        "product_name": product_name,
        "quantity": response.quantity
    }


@app.post("/orders/")
def create_order(data: dict):
    response = stub.CreateOrder(
        order_pb2.OrderRequest(
            client_id=int(data["client_id"]),
            product_id=data["product_id"],
            quantity=int(data["quantity"])
        )
    )

    return {
        "id": response.id,
        "client_id": response.client_id,
        "product_id": response.product_id,
        "quantity": response.quantity
    }