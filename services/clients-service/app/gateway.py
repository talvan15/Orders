from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import SessionLocal, engine
from app import crud, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clients Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClientCreate(BaseModel):
    name: str
    email: str


@app.get("/clients")
def list_clients():
    db = SessionLocal()

    try:
        clients = crud.get_clients(db)

        return [
            {
                "id": client.id,
                "name": client.name,
                "email": client.email,
            }
            for client in clients
        ]

    finally:
        db.close()


@app.get("/clients/{client_id}")
def get_client(client_id: int):
    db = SessionLocal()

    try:
        client = crud.get_client(db, client_id)

        if not client:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )

        return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
        }

    finally:
        db.close()


@app.post("/clients")
def create_client(client: ClientCreate):
    db = SessionLocal()

    try:
        db_client = crud.create_client(
            db,
            name=client.name,
            email=client.email
        )

        return {
            "id": db_client.id,
            "name": db_client.name,
            "email": db_client.email,
        }

    finally:
        db.close()


@app.put("/clients/{client_id}")
def update_client(client_id: int, client: ClientCreate):
    db = SessionLocal()

    try:
        updated_client = crud.update_client(
            db,
            client_id=client_id,
            name=client.name,
            email=client.email
        )

        if not updated_client:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )

        return {
            "id": updated_client.id,
            "name": updated_client.name,
            "email": updated_client.email,
        }

    finally:
        db.close()


@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    db = SessionLocal()

    try:
        deleted = crud.delete_client(db, client_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )

        return {
            "message": "Cliente excluído com sucesso"
        }

    finally:
        db.close()