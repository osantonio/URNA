# ./app/schemas/auth.py

"""
Esquemas Pydantic para autenticación
"""

from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Esquema para solicitud de login"""

    identificacion: str = Field(
        ...,
        min_length=6,
        max_length=10,
        pattern=r"^[0-9]{6,10}$",
        description="Cédula de ciudadanía",
    )
    password: str = Field(..., min_length=4, description="Contraseña del usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "identificacion": "1234567890",
                "password": "mi_password_seguro",
            }
        }


class LoginResponse(BaseModel):
    """Esquema para respuesta de login exitoso"""

    mensaje: str
    usuario: dict
    token: Optional[str] = None  # Para implementación futura de JWT

    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Login exitoso",
                "usuario": {
                    "identificacion": "1234567890",
                    "nombres": "Juan Carlos",
                    "apellidos": "Pérez González",
                    "rol": "Votante",
                },
                "token": None,
            }
        }
