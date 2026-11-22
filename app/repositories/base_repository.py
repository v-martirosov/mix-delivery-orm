from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")

class IRepository(Generic[T], ABC):
    """
    Интерфейс базового репозитория (Repository Pattern).
    Соблюдает SOLID:
    - SRP: только операции доступа к персистентным данным.
    - OCP: открыт для расширения специфичными методами.
    - ISP: чистый интерфейс работы с сущностью.
    - DIP: бизнес-логика зависит от интерфейса репозитория, а не от конкретной БД.
    """

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass


class BaseRepository(IRepository[T]):
    """
    Универсальная реализация репозитория с базовыми CRUD-операциями в SQLAlchemy 2.0.
    """
    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class

    def get_by_id(self, item_id: int) -> Optional[T]:
        return self.session.get(self.model_class, item_id)

    def get_all(self) -> List[T]:
        stmt = select(self.model_class)
        return list(self.session.scalars(stmt).all())

    def add(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, item_id: int) -> bool:
        entity = self.get_by_id(item_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False
