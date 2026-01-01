from fastapi import FastAPI
from app.routers import auth, doctors, appointments
from app.configs.database import engine, Base

app = FastAPI(
    title="Doctor Appointment API",
    description="A production-ready RESTful API for managing doctor appointments",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(appointments.router)

# Create tables
#Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Doctor Appointment API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "Service is up & running"}

