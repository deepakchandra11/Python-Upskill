from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, String
from sqlalchemy.orm import Session, DeclarativeBase, sessionmaker, Mapped, mapped_column
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from typing import Optional


app = FastAPI()

class Base(DeclarativeBase):
    pass

#------------------------------------------------------------

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))

#------------------------------------------------------------

# DATABASE_URL = "mysql+pymysql://root:igdefault@localhost:3306/fastapi_db"
DATABASE_URL = 'sqlite:///./user.db'

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create tables
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#------------------------------------------------------------

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    message: str

    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

#------------------------------------------------------------

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, request.email, request.password)
    return {"email": user.email, "message": "User registered successfully"}

@app.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, request.email, request.password)
    return {"access_token": token, "token_type": "bearer"}

#------------------------------------------------------------

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(plain_password, hashed_password):
        return pwd_cxt.verify(plain_password,hashed_password)

#------------------------------------------------------------

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception


#------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(data, credentials_exception)


#------------------------------------------------------------

def register_user(db: Session, email: str, password: str):
    if get_user_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = User(
        email=email,
        password=Hash.bcrypt(password)
    )
    return create_user(user, db)

def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not Hash.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_access_token(data={"sub": user.email})


#------------------------------------------------------------

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(user: User, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


#------------------------------------------------------------
"""           requirements.txt
    fastapi
    fastapi[standard]
    python-multipart
    pymysql
    cryptography
    python-jose[cryptography]
    passlib[bcrypt]
    python-dotenv
    sqlalchemy
"""
