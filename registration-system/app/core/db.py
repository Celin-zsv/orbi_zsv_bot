from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.core.config import settings


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True)


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(engine)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
