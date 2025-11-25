# ./app/config/__init__.py

"""
Configuración de la aplicación
"""

from .db import motor_async, async_session_maker, crear_tablas, obtener_sesion

__all__ = ["motor_async", "async_session_maker", "crear_tablas", "obtener_sesion"]
