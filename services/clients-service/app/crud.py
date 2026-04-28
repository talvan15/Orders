from sqlalchemy.orm import Session

from . import models


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_clients(db: Session):
    return db.query(models.Client).all()


def create_client(db: Session, name: str, email: str):
    db_client = models.Client(
        name=name,
        email=email
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client


def update_client(db: Session, client_id: int, name: str, email: str):
    db_client = get_client(db, client_id)

    if not db_client:
        return None

    db_client.name = name
    db_client.email = email

    db.commit()
    db.refresh(db_client)

    return db_client


def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)

    if not db_client:
        return False

    db.delete(db_client)
    db.commit()

    return True