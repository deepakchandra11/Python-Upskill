# Doctor Appointment API

A production-ready RESTful API for managing doctor appointments with full authentication and role-based access control (RBAC).

## 🛠 Tech Stack

- **Language**: Python 3.12+
- **Web Framework**: FastAPI
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy (Async)
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Pytest

## 📋 Features

### Authentication & Authorization
- User registration (Doctor / Patient)
- Login with JWT token generation
- Forgot password (mock flow)
- Secure JWT-based authentication for all business APIs
- Role-based access control (RBAC)

### Doctor Operations
- Set availability time slots
- View upcoming appointments

### Patient Operations
- List all doctors
- View doctor availability
- Book appointments (with double-booking prevention)
- Cancel own appointments

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd service
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and update the `SECRET_KEY` with a secure random string:
   ```env
   DATABASE_URL=mysql+aiomysql://app_user:app_password@localhost:3306/doctor_appointment
   SECRET_KEY=your-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. **Start MySQL database using Docker Compose**:
   ```bash
   docker-compose up -d
   ```
   
   This will start a MySQL 8.0 container on port 3306.

4. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**:
   - API Base URL: `http://localhost:8000`
   - Interactive API Documentation: `http://localhost:8000/docs`
   - Alternative API Documentation: `http://localhost:8000/redoc`

## 🧪 Running Tests

Run the test suite using pytest:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/test_auth.py
```

## 📚 API Endpoints

### Authentication

#### `POST /auth/register`
Register a new user (Doctor or Patient).

**Request Body:**
```json
{
  "email": "doctor@example.com",
  "password": "securepassword",
  "role": "Doctor",
  "name": "Dr. John Doe"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "doctor@example.com",
  "role": "Doctor",
  "name": "Dr. John Doe"
}
```

#### `POST /auth/login`
Login and receive JWT token.

**Request Body:**
```json
{
  "email": "doctor@example.com",
  "password": "securepassword"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### `POST /auth/forgot-password`
Mock forgot password flow.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`
```json
{
  "message": "If the email exists, a password reset link has been sent"
}
```

### Doctors (Patient Access)

#### `GET /doctors`
List all doctors. **Requires: Patient authentication**

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "doctor@example.com",
    "role": "Doctor",
    "name": "Dr. John Doe"
  }
]
```

#### `GET /doctors/{doctor_id}/availability`
Get availability for a specific doctor. **Requires: Patient authentication**

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "doctor_id": 1,
    "start_time": "2024-01-15T09:00:00",
    "end_time": "2024-01-15T17:00:00"
  }
]
```

### Doctors (Doctor Access)

#### `POST /doctors/availability`
Set availability time slots. **Requires: Doctor authentication**

**Request Body:**
```json
{
  "start_time": "2024-01-15T09:00:00",
  "end_time": "2024-01-15T17:00:00"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "doctor_id": 1,
  "start_time": "2024-01-15T09:00:00",
  "end_time": "2024-01-15T17:00:00"
}
```

#### `GET /doctors/appointments/upcoming`
Get upcoming appointments. **Requires: Doctor authentication**

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "doctor_id": 1,
    "patient_id": 2,
    "appointment_time": "2024-01-15T10:00:00",
    "status": "scheduled"
  }
]
```

### Appointments (Patient Access)

#### `POST /appointments`
Book an appointment. **Requires: Patient authentication**

**Request Body:**
```json
{
  "doctor_id": 1,
  "appointment_time": "2024-01-15T10:00:00"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "doctor_id": 1,
  "patient_id": 2,
  "appointment_time": "2024-01-15T10:00:00",
  "status": "scheduled"
}
```

#### `POST /appointments/{appointment_id}/cancel`
Cancel an appointment. **Requires: Patient authentication**

**Response:** `200 OK`
```json
{
  "id": 1,
  "doctor_id": 1,
  "patient_id": 2,
  "appointment_time": "2024-01-15T10:00:00",
  "status": "cancelled"
}
```

## 🔐 Authentication Flow and RBAC Design

### Authentication Flow

1. **Registration**: Users register with email, password, role (Doctor/Patient), and name. Passwords are hashed using bcrypt before storage.

2. **Login**: Users authenticate with email and password. Upon successful authentication, a JWT token is generated containing:
   - User ID (`sub`)
   - Email
   - Role

3. **Token Usage**: All protected endpoints require the JWT token in the Authorization header:
   ```
   Authorization: Bearer <token>
   ```

4. **Token Validation**: Each request validates the JWT token:
   - Verifies token signature
   - Checks token expiration
   - Retrieves user from database
   - Attaches user to request context

### Role-Based Access Control (RBAC)

The system implements RBAC with two roles:

1. **Doctor Role**:
   - Can set their availability
   - Can view their upcoming appointments
   - Cannot book appointments
   - Cannot view other doctors' appointments

2. **Patient Role**:
   - Can list all doctors
   - Can view doctor availability
   - Can book appointments
   - Can cancel their own appointments
   - Cannot set availability
   - Cannot view other patients' appointments

### Security Features

- **Password Hashing**: Passwords are hashed using bcrypt with automatic salt generation
- **JWT Tokens**: Secure token-based authentication with configurable expiration
- **Input Validation**: All requests are validated using Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Double-Booking Prevention**: Business logic prevents overlapping appointments
- **Authorization Checks**: Role-based access control enforced at the endpoint level

## 🏗 Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
app/
├── api/              # API routes and endpoints
├── core/             # Core configuration (database, security, config)
├── models/           # SQLAlchemy database models
├── repositories/     # Data access layer
├── schemas/          # Pydantic request/response schemas
└── services/         # Business logic layer
```

### Design Patterns

- **Repository Pattern**: Abstracts database operations
- **Service Pattern**: Encapsulates business logic
- **Dependency Injection**: FastAPI's dependency system for clean code organization

## 📝 Example Usage

### 1. Register a Doctor
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@example.com",
    "password": "password123",
    "role": "Doctor",
    "name": "Dr. Smith"
  }'
```

### 2. Login as Doctor
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@example.com",
    "password": "password123"
  }'
```

### 3. Set Availability (as Doctor)
```bash
curl -X POST "http://localhost:8000/doctors/availability" \
  -H "Authorization: Bearer <doctor_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "start_time": "2024-01-15T09:00:00",
    "end_time": "2024-01-15T17:00:00"
  }'
```

### 4. Register a Patient
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "password123",
    "role": "Patient",
    "name": "John Patient"
  }'
```

### 5. List Doctors (as Patient)
```bash
curl -X GET "http://localhost:8000/doctors" \
  -H "Authorization: Bearer <patient_token>"
```

### 6. Book Appointment (as Patient)
```bash
curl -X POST "http://localhost:8000/appointments" \
  -H "Authorization: Bearer <patient_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": 1,
    "appointment_time": "2024-01-15T10:00:00"
  }'
```

## 🧪 Testing

The test suite includes comprehensive unit tests covering:

- Authentication (registration, login, forgot password)
- Doctor operations (setting availability, viewing appointments)
- Patient operations (listing doctors, viewing availability, booking/cancelling appointments)
- Double-booking prevention
- Authorization and access control

Run tests:
```bash
pytest
```

## 🔧 Configuration

Configuration is managed through environment variables (`.env` file):

- `DATABASE_URL`: MySQL connection string
- `SECRET_KEY`: Secret key for JWT token signing (change in production!)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## 📦 Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `role`: Enum (Doctor/Patient)
- `name`: User's full name

### Availabilities Table
- `id`: Primary key
- `doctor_id`: Foreign key to users
- `start_time`: Availability start time
- `end_time`: Availability end time

### Appointments Table
- `id`: Primary key
- `doctor_id`: Foreign key to users
- `patient_id`: Foreign key to users
- `appointment_time`: Scheduled appointment time
- `status`: Enum (scheduled/cancelled/completed)

## 🚨 Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., double-booking)

## 📄 License

This project is part of a backend engineering assignment.

## 🤝 Contributing

This is an assignment project. For questions or issues, please refer to the assignment guidelines.

