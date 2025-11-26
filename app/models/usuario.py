# ./app/models/usuario.py

"""
Modelo de Usuario basado en modelo_base.sql
"""

from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from enum import Enum
import sqlalchemy as sa


class RolUsuario(str, Enum):
    """
    Jerarquía oficial de la campaña - el orden es sagrado
    Nivel 0 a 5 de menor a mayor poder
    """

    VOTANTE = "Votante"  # Nivel 0 - base de la pirámide
    ACTIVISTA = "Activista"  # Nivel 1 - el que jala gente en la calle
    LIDER = "Líder"  # Nivel 2 - jefe de su grupo/barrio
    JEFE_DE_ZONA = "Jefe de Zona"  # Nivel 3 - controla varios líderes
    COORDINADOR = "Coordinador"  # Nivel 4 - brazo derecho del candidato
    ESTRATEGA = "Estratega"  # Nivel 5 - MÁXIMO poder


class TipoSexo(str, Enum):
    """Sexo según normativa electoral colombiana"""

    MASCULINO = "Masculino"
    FEMENINO = "Femenino"
    OTRO = "Otro"


class Usuario(SQLModel, table=True):
    """
    Modelo principal de Usuario para URNA
    Cada fila es una persona en la pirámide electoral
    """

    # Identificación - PRIMARY KEY
    identificacion: str = Field(
        primary_key=True,
        max_length=10,
        regex=r"^[0-9]{6,10}$",
        description="Cédula de ciudadanía (6-10 dígitos)",
    )

    # Datos personales
    nombres: str = Field(description="Nombres completos")
    apellidos: str = Field(description="Apellidos completos")

    telefono: Optional[str] = Field(
        default=None,
        max_length=10,
        regex=r"^3[0-9]{9}$",
        description="Teléfono celular colombiano (10 dígitos, inicia con 3)",
    )

    edad: Optional[int] = Field(
        default=None, ge=18, le=120, description="Edad del usuario (18-120 años)"
    )

    sexo: Optional[TipoSexo] = Field(default=None, sa_column=Column(sa.Enum(TipoSexo)))

    correoelectronico: Optional[str] = Field(
        default=None, description="Correo electrónico"
    )

    # Datos electorales
    barrio_vereda: Optional[str] = Field(
        default=None, description="Barrio o vereda donde vive"
    )

    lugar_votacion: Optional[str] = Field(default=None, description="Lugar donde vota")

    mesa_votacion: Optional[str] = Field(
        default=None, description="Número de mesa de votación"
    )

    # Jerarquía y permisos
    rol: RolUsuario = Field(
        default=RolUsuario.VOTANTE,
        sa_column=Column(sa.Enum(RolUsuario)),
        description="Define poder, permisos y visibilidad",
    )

    # Árbol jerárquico - quién trajo o supervisa a este usuario
    asignado_a: Optional[str] = Field(
        default=None,
        foreign_key="usuario.identificacion",
        description="Identificación de quien reclutó/supervisa a este usuario",
    )

    # Autenticación
    password: str = Field(
        description="Contraseña hasheada (bcrypt/argon2) - NUNCA en texto plano"
    )

    # Métricas
    calidad_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Score de calidad del voto (0=dudoso, 100=voto seguro)",
    )

    # Auditoría
    fecha_registro: datetime = Field(
        default_factory=datetime.now,
        description="Fecha de registro del usuario",
    )

    fecha_actualizacion: datetime = Field(
        default_factory=datetime.now,
        description="Fecha de última actualización",
    )

    @property
    def nombre_completo(self) -> str:
        """
        Retorna el nombre completo del usuario (nombres + apellidos)
        """
        return f"{self.nombres} {self.apellidos}"
