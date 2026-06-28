# FILE: backend/app/api/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user # <-- NOVA LINHA: Importa get_current_user
from app.core.config import settings
from app.core.security import authenticate_user, create_access_token, get_password_hash
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioInDB, Token

auth_router = APIRouter()

@auth_router.post("/register", response_model=UsuarioInDB, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado."
        )
    hashed_password = get_password_hash(user_in.senha)
    db_user = Usuario(nome=user_in.nome, email=user_in.email, senha_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@auth_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=UsuarioInDB)
def read_users_me(current_user: Usuario = Depends(get_current_user)):
    return current_user