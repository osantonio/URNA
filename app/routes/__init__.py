# ./app/routes/__init__.py

"""
Registro de rutas de la aplicación
"""

from .index import router as index_router
from .auth import router as auth_router

__all__ = ["index_router", "auth_router"]
