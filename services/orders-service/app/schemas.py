from pydantic import BaseModel, Field
from datetime import datetime


class OrderBase(BaseModel):
    client_id: int
    product_id: str
    quantity: int = Field(..., gt=0)


class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True