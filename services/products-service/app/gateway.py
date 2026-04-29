from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import grpc

from generated import product_pb2
from generated import product_pb2_grpc

app = FastAPI(title="Products Gateway")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


channel = grpc.insecure_channel("127.0.0.1:50052")
stub = product_pb2_grpc.ProductServiceStub(channel)



class ProductCreate(BaseModel):
    name: str
    price: float


class ProductUpdate(BaseModel):
    name: str
    price: float



@app.get("/products/")
def list_products():
    try:
        response = stub.ListProducts(product_pb2.Empty())

        return [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            }
            for p in response.products
        ]

    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())


@app.get("/products/{product_id}/")
def get_product(product_id: str):
    try:
        response = stub.GetProductById(
            product_pb2.GetProductByIdRequest(id=product_id)
        )

        return {
            "id": response.id,
            "name": response.name,
            "price": response.price,
            "created_at": response.created_at,
            "updated_at": response.updated_at,
        }

    except grpc.RpcError:
        raise HTTPException(status_code=404, detail="Produto não encontrado")



@app.post("/products/")
def create_product(product: ProductCreate):
    try:
        response = stub.CreateProduct(
            product_pb2.CreateProductRequest(
                name=product.name,
                price=product.price
            )
        )

        return {
            "id": response.id,
            "name": response.name,
            "price": response.price,
            "created_at": response.created_at,
            "updated_at": response.updated_at,
        }

    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())



@app.put("/products/{product_id}/")
def update_product(product_id: str, product: ProductUpdate):
    try:
        response = stub.UpdateProduct(
            product_pb2.UpdateProductRequest(
                id=product_id,
                name=product.name,
                price=product.price
            )
        )

        return {
            "id": response.id,
            "name": response.name,
            "price": response.price,
            "created_at": response.created_at,
            "updated_at": response.updated_at,
        }

    except grpc.RpcError:
        raise HTTPException(status_code=404, detail="Produto não encontrado")



@app.delete("/products/{product_id}/")
def delete_product(product_id: str):
    try:
        response = stub.DeleteProduct(
            product_pb2.DeleteProductRequest(id=product_id)
        )

        return {
            "success": response.success,
            "message": response.message
        }

    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())
