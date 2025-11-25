# ./app/routes/index.py

"""
Rutas principales de la aplicación (index y salud)
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app import templates as jinja_templates

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
async def dashboard(request: Request):
    """
    Dashboard del usuario

    TODO: Implementar verificación de sesión
    TODO: Obtener datos del usuario desde la sesión/cookie

    Por ahora, esta es una ruta temporal que muestra datos de ejemplo.
    En producción, debe verificar que el usuario esté autenticado.
    """
    # TODO: Obtener usuario real desde sesión
    # Por ahora, datos de ejemplo para demostración
    usuario_ejemplo = {
        "identificacion": "1000000001",
        "nombre": "Roberto Carlos Mendoza Vargas",
        "nombres": "Roberto Carlos",
        "apellidos": "Mendoza Vargas",
        "rol": "Estratega",
        "calidad_score": 100,
        "telefono": "3001000001",
        "correoelectronico": "roberto.mendoza@urna.com",
        "barrio_vereda": "El Poblado",
        "lugar_votacion": "Universidad Central",
    }

    return jinja_templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario_ejemplo,
        },
    )
