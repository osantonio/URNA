# ./app/routes/__init__.py

"""
Registro de rutas de la aplicación
"""

from .index import router as index_router
from .auth import router as auth_router
from .votantes import router as votantes_router
from .documentacion import router as documentacion_router

__all__ = ["index_router", "auth_router", "votantes_router", "documentacion_router"]
