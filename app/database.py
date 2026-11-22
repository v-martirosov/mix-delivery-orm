from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Путь к локальной SQLite базе данных ООО «Микс»
DATABASE_URL = "sqlite:///mix_delivery.db"

# Создаем движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# Фабрика сессий (SessionLocal)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

def get_session() -> Session:
    """Возвращает новую сессию для работы с базой данных."""
    return SessionLocal()
