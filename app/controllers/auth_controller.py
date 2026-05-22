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
            {"request": request, "erro": "E-mail já cadastrado."},
            status_code=400
        )
    # Criar o usuário - criar o objeto
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senah_hash=hash_senha(senha)  # Armazenar a senha de forma segura (hash)
    )

    # Salvar o usuário no banco de dados
    db.add(novo_usuario)
    db.commit()
    
    return RedirectResponse(url="/auth/login?cadastrado=ok", status_code=302)

# Fazer login
@router.post("/login")
def fazer_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    # 1. Buscar o usuário pelo email no db
    usuario = db.query(Usuario).filter_by(email=email).first()

    # 2. Verificar a senha com bcrypt
    senha_correta = (
        usuario is not None and verificar_senha(senha, usuario.senah_hash)
    )
    if not senha_correta:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"request": request, "erro": "E-mail ou senha incorretos."},
            status_code=400
        )
    # Verificar se o usuário está ativo
    if not usuario.ativo:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"request": request, "erro": "Usuário inativo. Entre em contato com o suporte."},
            status_code=400
        ),
 
    # 3. Gerar o token JWT
    # Dados do token (payload)
    token_data = {
        "sub": usuario.email,
        "nome": usuario.nome,
        "role": usuario.role,
        "id": usuario.id
    }
    token = criar_token(token_data)

    # 4. Salvar o token em um cookie e redirecionar para pagina home
    response = RedirectResponse(url="/", status_code=302)

    # Definir o cookie com o token JWT
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # O cookie não pode ser acessado via JavaScript
        max_age=3600,   # Expira em 1 hora
        samesite="lax"  # Proteção contra CSRF
    )

    return response

# Rota de sair
@router.get("/logout")
def sair(request: Request):
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response