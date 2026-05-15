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

#Rota para criar o usuário
@router.post("/cadastro")
def fzer_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    
    # Verificar se o email já está cadastrado
    usuario_existente = db.query(Usuario).filter_by(email=email).first()

    # mensagem de erro se o email estiver cadastrado
    if usuario_existente:
        return templates.TemplateResponse(
            request,
            "auth/cadastro.html",
            {"request": request, "erro": "E-mail já cadastrado."}
        )
    # Criar o usuário - criar o objeto
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=hash_senha(senha)  # Armazenar a senha de forma segura (hash)
    )

    # Salvar o usuário no banco de dados
    db.add(novo_usuario)
    db.commit()
    
    return RedirectResponse(url="/auth/login", status_code=302)