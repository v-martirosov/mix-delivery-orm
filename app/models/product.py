from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Float, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Product(Base):
    """
    Модель товара плодоовощной базы ООО «Микс» (г. Владимир).
    Отражает номенклатуру свежих овощей, фруктов, зелени и ягод.
    """
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # Овощи, Фрукты, Зелень, Ягоды
    variety: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)     # Сорт (напр. 'Розовый Баку', 'Луховицкие')
    unit: Mapped[str] = mapped_column(String(20), default="кг")                   # кг, ящик, фасовка
    price: Mapped[float] = mapped_column(Float, nullable=False)                    # Розничная цена (руб.)
    wholesale_price: Mapped[float] = mapped_column(Float, nullable=False)          # Оптовая цена для B2B (руб.)
    stock_quantity: Mapped[float] = mapped_column(Float, default=0.0)             # Текущий остаток на складе
    min_stock_level: Mapped[float] = mapped_column(Float, default=10.0)           # Критический остаток для дозаказа
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Связь со строками заказов
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', category='{self.category}', price={self.price} руб., stock={self.stock_quantity} {self.unit})>"
