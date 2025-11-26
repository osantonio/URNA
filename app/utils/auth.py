# ./app/utils/auth.py

"""
Utilidades de autenticación para gestión de sesiones y contraseñas
"""

from typing import Optional
from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from passlib.context import CryptContext

from app.config import obtener_sesion
from app.models import Usuario

# Configuración de bcrypt para hashing de contraseñas
contexto_password = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña
    """
    return contexto_password.hash(password)


def verificar_password(password: str, hash_password: str) -> bool:
    """
    Verifica una contraseña contra su hash

    Args:
        password: Contraseña en texto plano
        hash_password: Hash de la contraseña almacenada

    Returns:
        True si la contraseña coincide, False en caso contrario
    """
    return contexto_password.verify(password, hash_password)


def guardar_usuario_en_sesion(request: Request, usuario: Usuario) -> None:
    """
    Guarda los datos del usuario en la sesión

    Args:
        request: Request de FastAPI
        usuario: Usuario autenticado
    """
    request.session["usuario_id"] = usuario.identificacion
    request.session["usuario_rol"] = usuario.rol.value if usuario.rol else None
    request.session["usuario_nombre"] = usuario.nombre_completo


async def obtener_usuario_desde_sesion(
    request: Request, sesion: AsyncSession
) -> Optional[Usuario]:
    """
    Obtiene el usuario completo desde la sesión

    Args:
        request: Request de FastAPI
        sesion: Sesión de base de datos

    Returns:
        Usuario si está autenticado, None en caso contrario
    """
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return None

    # Obtener usuario completo desde base de datos
    statement = select(Usuario).where(Usuario.identificacion == usuario_id)
    resultado = await sesion.execute(statement)
    usuario = resultado.scalar_one_or_none()

    return usuario


def limpiar_sesion(request: Request) -> None:
    """
    Limpia completamente la sesión del usuario

    Args:
        request: Request de FastAPI
    """
    request.session.clear()


async def requerir_autenticacion(
    request: Request, sesion: AsyncSession = Depends(obtener_sesion)
) -> Usuario:
    """
    Dependencia de FastAPI para proteger rutas que requieren autenticación.
    Redirige a login si el usuario no está autenticado.

    Args:
        request: Request de FastAPI
        sesion: Sesión de base de datos

    Returns:
        Usuario autenticado

    Raises:
        HTTPException: Redirige a login si no está autenticado
    """
    usuario = await obtener_usuario_desde_sesion(request, sesion)

    if not usuario:
        # Redirigir a login si no está autenticado
        raise HTTPException(
            status_code=303,
            detail="No autenticado",
            headers={"Location": "/auth/login"},
        )

    return usuario
