from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(product: schemas.ProductBase, db: Session = Depends(get_db)):
    """
    Cria um novo produto.
    """
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=list[schemas.Product])
def read_products_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista de produtos.
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product_endpoint(product_id: str, db: Session = Depends(get_db)):
    """
    Retorna um produto específico pelo ID.
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product

@router.patch("/{product_id}", response_model=schemas.Product)
def update_product_endpoint(product_id: str, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um produto existente.
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return crud.update_product(db=db, product_id=product_id, product_update=product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id: str, db: Session = Depends(get_db)):
    """
    Deleta um produto pelo ID.
    """
    success = crud.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return