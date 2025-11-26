# ./app/routes/index.py

"""
Rutas principales de la aplicación (index y salud)
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app import templates as jinja_templates
from app.utils.auth import requerir_autenticacion
from app.models import Usuario

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def raiz(request: Request):
    """Página de inicio de URNA"""
    return jinja_templates.TemplateResponse("index.html", {"request": request})


@router.get("/salud")
async def verificar_salud():
    """Endpoint para verificar el estado de la API (JSON)"""
    return {
        "estado": "saludable",
        "base_datos": "PostgreSQL con SSL requerido",
        "orm": "SQLModel",
        "templates": "Jinja2 + Tailwind CSS",
    }


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request, usuario: Usuario = Depends(requerir_autenticacion)
):
    """
    Dashboard del usuario autenticado
    Requiere autenticación - redirige a login si no está autenticado
    """
    return jinja_templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
        },
    )
