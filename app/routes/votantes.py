# ./app/routes/votantes.py

"""
Rutas para gestión de votantes
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.config import obtener_sesion
from app.models import Usuario
from app import templates as jinja_templates

router = APIRouter(prefix="/votantes", tags=["Votantes"])


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def listar_votantes(
    request: Request, sesion: AsyncSession = Depends(obtener_sesion)
):
    """
    Lista todos los votantes/usuarios del sistema
    """
    # Consultar todos los usuarios
    statement = select(Usuario).order_by(Usuario.fecha_registro.desc())
    resultado = await sesion.execute(statement)
    votantes = resultado.scalars().all()

    return jinja_templates.TemplateResponse(
        "votantes/listar.html",
        {"request": request, "votantes": votantes, "total": len(votantes)},
    )
