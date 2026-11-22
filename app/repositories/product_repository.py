from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base_repository import BaseRepository

class ProductRepository(BaseRepository[Product]):
    """
    Репозиторий для сущности Product (ООО «Микс»).
    Реализует CRUD и специализированные бизнес-запросы для складского учета свежей продукции.
    """
    def __init__(self, session: Session):
        super().__init__(session, Product)

    def get_by_category(self, category: str) -> List[Product]:
        """Получение всех активных товаров конкретной категории (Овощи, Фрукты, Зелень)."""
        stmt = select(Product).where(Product.category == category, Product.is_active == True)
        return list(self.session.scalars(stmt).all())

    def get_low_stock(self) -> List[Product]:
        """
        Бизнес-логика склада Fresh Food:
        Возвращает товары, у которых текущий остаток ниже или равен неснижаемому минимуму (требуется закупка).
        """
        stmt = select(Product).where(
            Product.stock_quantity <= Product.min_stock_level,
            Product.is_active == True
        )
        return list(self.session.scalars(stmt).all())

    def update_stock(self, product_id: int, quantity_delta: float) -> Optional[Product]:
        """
        Изменение остатка на складе (положительное число — приход, отрицательное — списание/продажа).
        """
        product = self.get_by_id(product_id)
        if not product:
            return None
        product.stock_quantity += quantity_delta
        if product.stock_quantity < 0:
            product.stock_quantity = 0.0
        self.session.commit()
        self.session.refresh(product)
        return product

    def search_by_name(self, query: str) -> List[Product]:
        """Поиск товара по подстроке наименования."""
        stmt = select(Product).where(Product.name.ilike(f"%{query}%"))
        return list(self.session.scalars(stmt).all())
