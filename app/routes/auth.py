# ./app/routes/auth.py

"""
Rutas de autenticación (login)
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.config import obtener_sesion
from app.models import Usuario
from app import templates as jinja_templates
from app.utils.auth import (
    verificar_password,
    guardar_usuario_en_sesion,
    limpiar_sesion,
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.get("/login", response_class=HTMLResponse)
async def mostrar_login(request: Request):
    """Muestra el formulario de login"""
    return jinja_templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def procesar_login(
    request: Request,
    identificacion: str = Form(...),
    password: str = Form(...),
    sesion: AsyncSession = Depends(obtener_sesion),
):
    """
    Procesa el formulario de login
    Verifica credenciales y guarda usuario en sesión
    """

    # Buscar usuario por identificación
    statement = select(Usuario).where(Usuario.identificacion == identificacion)
    resultado = await sesion.execute(statement)
    usuario = resultado.scalar_one_or_none()

    # Validar credenciales
    if not usuario or not verificar_password(password, usuario.password):
        return jinja_templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "Identificación o contraseña incorrecta",
            },
        )

    # Login exitoso - guardar usuario en sesión
    guardar_usuario_en_sesion(request, usuario)

    # Redirigir a dashboard
    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    """
    Cierra la sesión del usuario
    """
    limpiar_sesion(request)
    return RedirectResponse(url="/", status_code=303)
