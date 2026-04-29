from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Order(id={self.id}, client_id={self.client_id}, product_id={self.product_id})>"