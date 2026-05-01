from concurrent import futures
import grpc
import datetime

from generated import product_pb2, product_pb2_grpc

from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


class ProductService(product_pb2_grpc.ProductServiceServicer):

    def CreateProduct(self, request, context):
        db = SessionLocal()

        try:
            product_data = schemas.ProductBase(name=request.name, price=request.price)
            product = crud.create_product(db, product=product_data)

            return product_pb2.ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                created_at=product.created_at.isoformat(),
                updated_at=product.updated_at.isoformat()
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.ProductResponse()

        finally:
            db.close()

    def GetProductById(self, request, context):
        db = SessionLocal()

        try:
            product = crud.get_product(db, request.id)

            if not product:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Product not found")
                return product_pb2.ProductResponse()

            return product_pb2.ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                created_at=product.created_at.isoformat(),
                updated_at=product.updated_at.isoformat()
            )

        finally:
            db.close()

    def ListProducts(self, request, context):
        db = SessionLocal()

        try:
            products = crud.get_products(db)

            return product_pb2.ListProductsResponse(
                products=[
                    product_pb2.ProductResponse(
                        id=p.id,
                        name=p.name,
                        price=p.price,
                        created_at=p.created_at.isoformat(),
                        updated_at=p.updated_at.isoformat()
                    )
                    for p in products
                ]
            )

        finally:
            db.close()

    def UpdateProduct(self, request, context):
        db = SessionLocal()

        try:
            # Create ProductUpdate schema with only set values
            update_data = {}
            if request.name:
                update_data['name'] = request.name
            if request.price > 0:
                update_data['price'] = request.price
            
            product_update = schemas.ProductUpdate(**update_data)
            
            product = crud.update_product(
                db,
                product_id=request.id,
                product_update=product_update
            )

            if not product:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Product not found")
                return product_pb2.ProductResponse()

            return product_pb2.ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                created_at=product.created_at.isoformat(),
                updated_at=product.updated_at.isoformat()
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.ProductResponse()

        finally:
            db.close()

    def DeleteProduct(self, request, context):
        db = SessionLocal()

        try:
            success = crud.delete_product(db, request.id)

            if not success:
                return product_pb2.DeleteProductResponse(
                    success=False,
                    message="Product not found"
                )

            return product_pb2.DeleteProductResponse(
                success=True,
                message="Product deleted successfully"
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.DeleteProductResponse(success=False, message=str(e))

        finally:
            db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    product_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductService(),
        server
    )

    server.add_insecure_port("[::]:50052")
    server.start()

    print("Products Service gRPC rodando na porta 50052")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()