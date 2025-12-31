from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, Token
from app.configs.security import verify_password, create_access_token
from datetime import timedelta


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, user_data: UserCreate) -> dict:
        """Register a new user."""
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user
        user = await self.user_repo.create(user_data)
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "name": user.name
        }

    async def login(self, login_data: UserLogin) -> Token:
        """Authenticate user and return JWT token."""
        user = await self.user_repo.get_by_email(login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value},
            expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    async def forgot_password(self, email: str) -> dict:
        """Mock forgot password flow."""
        user = await self.user_repo.get_by_email(email)
        if not user:
            # Don't reveal if email exists or not (security best practice)
            return {"message": "If the email exists, a password reset link has been sent"}

        # In a real application, you would send an email here
        # For this assignment, we just return a success message
        return {"message": "If the email exists, a password reset link has been sent"}

