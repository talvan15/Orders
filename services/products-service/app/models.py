import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime

import uuid

class product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"