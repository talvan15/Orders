from sqlalchemy.orm import Session
from . import models


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session):
    return db.query(models.Order).all()


def create_order(db: Session, client_id: int, product_id: str, quantity: int):
    db_order = models.Order(
        client_id=client_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order