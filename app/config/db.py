# ./app/config/db.py

"""
Configuración de la base de datos usando SQLModel y PostgreSQL
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URL de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://usuario:password@localhost:5432/urna"
)

# Crear motor asíncrono para PostgreSQL con SSL requerido
motor_async = create_async_engine(
    DATABASE_URL,
    #    echo=True if os.getenv("DEBUG", "False") == "True" else False,
    future=True,
    connect_args={
        "ssl": "require"  # Requerir SSL para conexión segura
    },
)

# Crear sesión asíncrona usando async_sessionmaker
async_session_maker = async_sessionmaker(
    motor_async, class_=AsyncSession, expire_on_commit=False
)


async def crear_tablas():
    """Crear todas las tablas en la base de datos"""
    async with motor_async.begin() as conexion:
        await conexion.run_sync(SQLModel.metadata.create_all)


async def obtener_sesion() -> AsyncGenerator[AsyncSession, None]:
    """
    Generador de sesiones de base de datos para usar con FastAPI Depends

    Uso:
        @app.get("/endpoint")
        async def mi_endpoint(sesion: AsyncSession = Depends(obtener_sesion)):
            # usar sesion aquí
    """
    async with async_session_maker() as sesion:
        yield sesion
