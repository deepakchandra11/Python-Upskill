import pytest
from httpx import AsyncClient
from app.models.user import UserRole


@pytest.mark.asyncio
async def test_register_doctor(client: AsyncClient):
    """Test doctor registration."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "doctor@test.com",
            "password": "password123",
            "role": "Doctor",
            "name": "Dr. Test"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "doctor@test.com"
    assert data["role"] == "Doctor"
    assert data["name"] == "Dr. Test"
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_patient(client: AsyncClient):
    """Test patient registration."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "patient@test.com",
            "password": "password123",
            "role": "Patient",
            "name": "Patient Test"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "patient@test.com"
    assert data["role"] == "Patient"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email."""
    await client.post(
        "/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "password123",
            "role": "Patient",
            "name": "Test User"
        }
    )
    
    response = await client.post(
        "/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "password123",
            "role": "Patient",
            "name": "Test User"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login."""
    # Register first
    await client.post(
        "/auth/register",
        json={
            "email": "login@test.com",
            "password": "password123",
            "role": "Patient",
            "name": "Login Test"
        }
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "login@test.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    # Register first
    await client.post(
        "/auth/register",
        json={
            "email": "valid@test.com",
            "password": "password123",
            "role": "Patient",
            "name": "Valid User"
        }
    )
    
    # Try login with wrong password
    response = await client.post(
        "/auth/login",
        json={
            "email": "valid@test.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    
    # Try login with non-existent email
    response = await client.post(
        "/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_forgot_password(client: AsyncClient):
    """Test forgot password endpoint."""
    # Register first
    await client.post(
        "/auth/register",
        json={
            "email": "forgot@test.com",
            "password": "password123",
            "role": "Patient",
            "name": "Forgot Test"
        }
    )
    
    # Request password reset
    response = await client.post(
        "/auth/forgot-password",
        json={
            "email": "forgot@test.com"
        }
    )
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Test with non-existent email (should still return success for security)
    response = await client.post(
        "/auth/forgot-password",
        json={
            "email": "nonexistent@test.com"
        }
    )
    assert response.status_code == 200

