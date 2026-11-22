from datetime import datetime
from typing import List
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Courier(Base):
    """
    Модель водителя-экспедитора доставки ООО «Микс».
    """
    __tablename__ = "couriers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    vehicle: Mapped[str] = mapped_column(String(80), default="ГАЗель Next (Изотермический)")
    delivery_zone: Mapped[str] = mapped_column(String(60), default="г. Владимир")
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Связь с заказами
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="courier")

    def __repr__(self) -> str:
        return f"<Courier(id={self.id}, name='{self.full_name}', vehicle='{self.vehicle}', zone='{self.delivery_zone}')>"
