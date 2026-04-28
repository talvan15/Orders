import datetime
import uuid

from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)

    class Config:
        from_attributes = True

class Product(ProductBase):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Monitor UltraWide",
                    "price": 1800.50,
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat()
                }
            ]
        }
    }

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

    class Config:
        from_attributes = True