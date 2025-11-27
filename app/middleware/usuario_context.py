# ./app/middleware/usuario_context.py

"""
Middleware para inyectar el usuario autenticado en el contexto de todos los templates
"""

from typing import Callable
import os
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
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
        request.state.usuario = None
        """
        idle_timeout se encarga de cerrar la sesion
        si el usuario no ha hecho nada, durante los
        segundos expresados en  idle_timeout.
        """
        idle_timeout = int(os.getenv("SESSION_IDLE_TIMEOUT_SECONDS", "2700"))
        path = request.url.path
        excluded = path.startswith("/static") or path.startswith("/auth/login")
        now = int(time.time())
        last = request.session.get("ultimo_uso")

        if last and now - last > idle_timeout:
            request.session.clear()
            if not excluded:
                return RedirectResponse(url="/auth/login", status_code=303)

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

        if usuario_id:
            request.session["ultimo_uso"] = now

        response = await call_next(request)
        return response
