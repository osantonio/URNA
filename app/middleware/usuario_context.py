# ./app/middleware/usuario_context.py

"""
Middleware para inyectar el usuario autenticado en el contexto de todos los templates
"""

from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlmodel import select

from app.config import obtener_sesion
from app.models import Usuario


class UsuarioContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware que inyecta el usuario autenticado en request.state
    para que esté disponible en todos los templates Jinja2
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Procesa cada request para agregar el usuario al contexto

        Args:
            request: Request de FastAPI
            call_next: Siguiente middleware/handler

        Returns:
            Response procesada
        """
        # Inicializar usuario como None
        request.state.usuario = None

        # Intentar obtener usuario desde sesión
        usuario_id = request.session.get("usuario_id")

        if usuario_id:
            try:
                # Obtener sesión de base de datos
                async for sesion in obtener_sesion():
                    # Buscar usuario en base de datos
                    statement = select(Usuario).where(
                        Usuario.identificacion == usuario_id
                    )
                    resultado = await sesion.execute(statement)
                    usuario = resultado.scalar_one_or_none()

                    if usuario:
                        request.state.usuario = usuario

                    break  # Solo necesitamos una iteración
            except Exception:
                # Si hay algún error, simplemente dejamos usuario como None
                # Esto evita que errores de BD rompan toda la aplicación
                pass

        # Continuar con el siguiente middleware/handler
        response = await call_next(request)
        return response
