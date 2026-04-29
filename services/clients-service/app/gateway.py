from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import SessionLocal
from app import crud


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