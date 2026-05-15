# Rotas de autenticação vai ficar aqui 

from fastapi import APIRouter, Depends, Request, Response, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.usuarios import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

# APIRouter agrupa as rotas dentro desse módulo com o prefixo  /auth
router = APIRouter(prefix="/auth", tags=["Autenticação"])

templates = Jinja2Templates(directory="app/templates")



#Tela de cadastro
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/cadastro.html",
        {"request": request}
    )

#Tela de login
@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"request": request}
    )