# ./app/schemas/__init__.py

"""
Esquemas Pydantic para validación de datos
"""

from .auth import LoginRequest, LoginResponse

__all__ = ["LoginRequest", "LoginResponse"]
