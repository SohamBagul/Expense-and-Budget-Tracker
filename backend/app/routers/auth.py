from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import RefreshTokenRequest, TokenResponse, UserCreate, UserLogin, UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    print("========== LOGIN HIT ==========")
    print("Credentials:", credentials)
    print("===============================")

    user = auth_service.authenticate_user(db, credentials)
    return auth_service.create_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(db, token_data.refresh_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    return {"message": "Successfully logged out. Please discard your tokens on the client."}

from app.models.user import User
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()