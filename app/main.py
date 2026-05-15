# Ponte de entrada do meu sistema
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controllers import auth_controller

app = FastAPI(title="Sistema de Ponto de venda")

#Configurar a pasta para servir os arquivo estáticos (CSS, JS e IMG)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#Configurar o jinja2 para rederizar os HTML
templates = Jinja2Templates(directory="app/templates")

#Inclui os routers dos controladores
app.include_router(auth_controller.router)