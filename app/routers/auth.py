from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, ForgotPasswordRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user (Doctor or Patient)."""
    auth_service = AuthService(db)
    return await auth_service.register(user_data)


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login and receive JWT token."""
    auth_service = AuthService(db)
    return await auth_service.login(login_data)


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Mock forgot password flow."""
    auth_service = AuthService(db)
    return await auth_service.forgot_password(request.email)

