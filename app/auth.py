# Lógica de autenticação

# 1. Hash e verificar com bcrypt

# 2. Geração de token JWT

# 3. Leitura e validação do token do cookie

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MINUTE = os.getenv("ACCES_TOKEN_EXPIRE_MINUTE")

# Configurar o algoritmo do hash = bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Funções de senha 

def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senah_hash: str):
    return pwd_context.verify(senha, senah_hash)

# Funções do tokem JWT

def criar_token(dados: dict):

    payload = dados.copy()

    #Define qaundo token expira
    expira = datetime.now(timezone.utc) + timedelta(minutes=int(ACCES_TOKEN_EXPIRE_MINUTE))
    payload.update({"exp": expira})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def decodificar_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


# função para usar nas rotas protegida
def get_usuario_logado(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    try:
        payload = decodificar_token(token)
        email: str = payload.get("sub")

        if not email:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido"
        )
        
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado"
        )
    
def get_usuario_opcional(request: Request):
    try:
        return get_usuario_logado(request)
    except HTTPException:
        return None