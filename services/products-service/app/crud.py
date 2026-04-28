import datetime
import uuid

from sqlalchemy.orm import Session

from . import models, schemas

def get_product(db: Session, product_id: str):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductBase):
    db_product = models.Product(
        id=str(uuid.uuid4()),
        name=product.name,
        price=product.price,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: str, product_update: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_product, key, value)

        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: str):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False