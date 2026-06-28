# FILE: backend/app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioInDB


# ---------------------------------------------------------------------------
# Utilitários de hashing de senha (bcrypt direto, sem passlib)
# ---------------------------------------------------------------------------

def _encode_password(password: str) -> bytes:
    """
    Converte a senha para bytes UTF-8 e trunca para 72 bytes,
    respeitando o limite interno do bcrypt.
    """
    return password.encode("utf-8")[:72]


def get_password_hash(password: str) -> str:
    """Gera o hash bcrypt de uma senha e retorna como string."""
    password_bytes = _encode_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash armazenado."""
    password_bytes = _encode_password(plain_password)
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Cria e retorna um token de acesso JWT assinado."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> str:
    """
    Decodifica o token JWT e retorna o subject (email/username).
    Lança HTTPException 401 se o token for inválido ou expirado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        subject: Optional[str] = payload.get("sub")
        if subject is None:
            raise credentials_exception
        return subject
    except JWTError:
        raise credentials_exception


# ---------------------------------------------------------------------------
# Autenticação de usuário
# ---------------------------------------------------------------------------

def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> Optional[UsuarioInDB]:
    """
    Busca o usuário pelo e-mail e verifica a senha.
    Retorna UsuarioInDB se as credenciais forem válidas, caso contrário None.
    """
    user: Optional[Usuario] = (
        db.query(Usuario).filter(Usuario.email == email).first()
    )
    if user is None:
        return None
    if not verify_password(password, user.senha_hash):
        return None
    return UsuarioInDB.model_validate(user)