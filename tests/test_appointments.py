import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from app.models.user import UserRole


@pytest.fixture
async def doctor_token(client: AsyncClient) -> str:
    """Create a doctor and return auth token."""
    # Register doctor
    await client.post(
        "/auth/register",
        json={
            "email": "doctor@test.com",
            "password": "password123",
            "role": "Doctor",
            "name": "Dr. Test"
        }
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "doctor@test.com",
            "password": "password123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
async def patient_token(client: AsyncClient) -> str:
    """Create a patient and return auth token."""
    # Register patient
    await client.post(
        "/auth/register",
        json={
            "email": "patient@test.com",
            "password": "password123",
            "role": "Patient",
            "name": "Patient Test"
        }
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "patient@test.com",
            "password": "password123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
async def doctor_id_and_token(client: AsyncClient) -> tuple[int, str]:
    """Create a doctor and return doctor ID and token."""
    # Register doctor
    response = await client.post(
        "/auth/register",
        json={
            "email": "doctor2@test.com",
            "password": "password123",
            "role": "Doctor",
            "name": "Dr. Test 2"
        }
    )
    doctor_id = response.json()["id"]
    
    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "doctor2@test.com",
            "password": "password123"
        }
    )
    token = response.json()["access_token"]
    return doctor_id, token


@pytest.mark.asyncio
async def test_list_doctors(client: AsyncClient, patient_token: str):
    """Test listing all doctors."""
    # Create a doctor first
    await client.post(
        "/auth/register",
        json={
            "email": "doctor_list@test.com",
            "password": "password123",
            "role": "Doctor",
            "name": "Dr. List"
        }
    )
    
    # List doctors
    response = await client.get(
        "/doctors",
        headers={"Authorization": f"Bearer {patient_token}"}
    )
    assert response.status_code == 200
    doctors = response.json()
    assert isinstance(doctors, list)
    assert len(doctors) > 0
    assert any(d["email"] == "doctor_list@test.com" for d in doctors)


@pytest.mark.asyncio
async def test_list_doctors_unauthorized(client: AsyncClient):
    """Test listing doctors without authentication."""
    response = await client.get("/doctors")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_set_availability(client: AsyncClient, doctor_token: str):
    """Test setting doctor availability."""
    start_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
    end_time = (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat()
    
    response = await client.post(
        "/doctors/availability",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "start_time": start_time,
            "end_time": end_time
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "doctor_id" in data


@pytest.mark.asyncio
async def test_set_availability_invalid_time(client: AsyncClient, doctor_token: str):
    """Test setting availability with invalid time range."""
    start_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
    end_time = (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat()
    
    # End time before start time
    response = await client.post(
        "/doctors/availability",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "start_time": end_time,
            "end_time": start_time
        }
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_doctor_availability(
    client: AsyncClient,
    patient_token: str,
    doctor_id_and_token: tuple[int, str]
):
    """Test getting doctor availability."""
    doctor_id, doctor_token = doctor_id_and_token
    
    # Set availability first
    start_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
    end_time = (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat()
    
    await client.post(
        "/doctors/availability",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "start_time": start_time,
            "end_time": end_time
        }
    )
    
    # Get availability
    response = await client.get(
        f"/doctors/{doctor_id}/availability",
        headers={"Authorization": f"Bearer {patient_token}"}
    )
    assert response.status_code == 200
    availabilities = response.json()
    assert isinstance(availabilities, list)
    assert len(availabilities) > 0


@pytest.mark.asyncio
async def test_book_appointment(
    client: AsyncClient,
    patient_token: str,
    doctor_id_and_token: tuple[int, str]
):
    """Test booking an appointment."""
    doctor_id, doctor_token = doctor_id_and_token
    
    # Set availability first
    appointment_time = datetime.utcnow() + timedelta(days=1, hours=1)
    start_time = (appointment_time - timedelta(hours=1)).isoformat()
    end_time = (appointment_time + timedelta(hours=1)).isoformat()
    
    await client.post(
        "/doctors/availability",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "start_time": start_time,
            "end_time": end_time
        }
    )
    
    # Book appointment
    response = await client.post(
        "/appointments",
        headers={"Authorization": f"Bearer {patient_token}"},
        json={
            "doctor_id": doctor_id,
            "appointment_time": appointment_time.isoformat()
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["doctor_id"] == doctor_id
    assert data["status"] == "scheduled"


@pytest.mark.asyncio
async def test_book_appointment_double_booking(
    client: AsyncClient,
    patient_token: str,
    doctor_id_and_token: tuple[int, str]
):
    """Test preventing double-booking."""
    doctor_id, doctor_token = doctor_id_and_token
    
    # Set availability
    appointment_time = datetime.utcnow() + timedelta(days=1, hours=1)
    start_time = (appointment_time - timedelta(hours=1)).isoformat()
    end_time = (appointment_time + timedelta(hours=1)).isoformat()
    
    await client.post(
        "/doctors/availability",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "start_time": start_time,
            "end_time": end_time
        }
    )
    
    # Book first appointment
    await client.post(
        "/appointments",
        headers={"Authorization": f"Bearer {patient_token}"},
        json={
            "doctor_id": doctor_id,
            "appointment_time": appointment_time.isoformat()
        }
    )
    
    # Try to book second appointment at same time (should fail)
    response = await client.post(
        "/appointments",
        headers={"Authorization": f"Bearer {patient_token}"},
        json={
            "doctor_id": doctor_id,
            "appointment_time": appointment_time.isoformat()
        }
    )
    assert response.status_code == 409
    assert "already booked" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_book_appointment_no_availability(
    client: AsyncClient,
    patient_token: str,
    doctor_id_and_token: tuple[int, str]
):
    """Test booking appointment when doctor has no availability."""
    doctor_id, _ = doctor_id_and_token
    
    appointment_time = datetime.utcnow() + timedelta(days=1, hours=1)
    
    # Try to book without setting availability
    response = await client.post(
        "/appointments",
        headers={"Authorization": f"Bearer {patient_token}"},
        json={
            "doctor_id": doctor_id,
            "appointment_time": appointment_time.isoformat()
        }
    )
    assert response.status_code == 400
    assert "not available" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_cancel_appointment(
    client: AsyncClient,
    patient_token: str,
    doctor_id_and_token: tuple[int, str]
):
    """Test cancelling an appointment."""
    doctor_id, doctor_token = doctor_id_and_token
    
    # Set availability
    appointment_time = datetime.utcnow() + timedelta(days=1, hours=1)
    start_time = (appointment_time - timedelta(hours=1)).isoformat()
    end_time = (appointment_time + timedelta(hours=1)).isoformat()
    
    await client.post(
        "/doctors/availability",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "start_time": start_time,
            "end_time": end_time
        }
    )
    
    # Book appointment
    response = await client.post(
        "/appointments",
        headers={"Authorization": f"Bearer {patient_token}"},
        json={
            "doctor_id": doctor_id,
            "appointment_time": appointment_time.isoformat()
        }
    )
    appointment_id = response.json()["id"]
    
    # Cancel appointment
    response = await client.post(
        f"/appointments/{appointment_id}/cancel",
        headers={"Authorization": f"Bearer {patient_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_get_upcoming_appointments(client: AsyncClient, doctor_token: str):
    """Test getting upcoming appointments for a doctor."""
    response = await client.get(
        "/doctors/appointments/upcoming",
        headers={"Authorization": f"Bearer {doctor_token}"}
    )
    assert response.status_code == 200
    appointments = response.json()
    assert isinstance(appointments, list)

