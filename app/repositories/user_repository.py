from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.configs.security import get_password_hash


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            role=user_data.role,
            name=user_data.name
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_doctors(self) -> list[User]:
        """Get all doctors."""
        from app.models.user import UserRole
        result = await self.db.execute(
            select(User).where(User.role == UserRole.DOCTOR)
        )
        return list(result.scalars().all())

