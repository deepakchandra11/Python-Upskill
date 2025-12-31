from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


# DATABASE_URL=mysql+aiomysql://root:igdefault@localhost:3306/doctor_appointment
DATABASE_URL='sqlite+aiosqlite:///./doctor_appointment.db'

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

