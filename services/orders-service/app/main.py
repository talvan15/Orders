from concurrent import futures
import grpc

from . import order_pb2
from . import order_pb2_grpc

from .database import engine, SessionLocal, Base
from .crud import create_order, get_order, get_orders

Base.metadata.create_all(bind=engine)


class OrderService(order_pb2_grpc.OrderServiceServicer):

    def CreateOrder(self, request, context):
        db = SessionLocal()

        order = create_order(
            db,
            request.client_id,
            request.product_id,
            request.quantity
        )

        return order_pb2.OrderResponse(
            id=order.id,
            client_id=order.client_id,
            product_id=order.product_id,
            quantity=order.quantity
        )

    def GetOrder(self, request, context):
        db = SessionLocal()

        order = get_order(db, request.id)

        return order_pb2.OrderResponse(
            id=order.id,
            client_id=order.client_id,
            product_id=order.product_id,
            quantity=order.quantity
        )

    def ListOrders(self, request, context):
        db = SessionLocal()

        orders = get_orders(db)

        return order_pb2.OrderList(
            orders=[
                order_pb2.OrderResponse(
                    id=o.id,
                    client_id=o.client_id,
                    product_id=o.product_id,
                    quantity=o.quantity
                )
                for o in orders
            ]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    order_pb2_grpc.add_OrderServiceServicer_to_server(
        OrderService(),
        server
    )

    server.add_insecure_port("[::]:50052")
    server.start()

    print("Orders Service gRPC rodando na porta 50052")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()