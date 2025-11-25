# ./app/__init__.py

"""
Aplicación principal de URNA
Configuración de FastAPI con lifespan, templates Jinja2 y archivos estáticos
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from app.config.startup import (
    init_db_urna,
    app_urna_abierta,
    app_urna_cerrada,
    app_urna_iniciada,
)

# Cargar variables de entorno
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación
    Reemplaza los eventos deprecados startup y shutdown
    """
    # Startup
    app_urna_abierta()
    await init_db_urna()
    app_urna_iniciada()
    yield
    # Shutdown
    app_urna_cerrada()


# Crear instancia de FastAPI con lifespan
app = FastAPI(
    title=os.getenv("APP_NAME", "URNA"),
    description="Aplicación web construida con FastAPI, SQLModel, PostgreSQL y Tailwind CSS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configurar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates Jinja2
# IMPORTANTE: Debe estar ANTES de importar las rutas
templates = Jinja2Templates(directory="app/templates")

# Exportar para uso en rutas
__all__ = ["app", "templates"]

# Registrar rutas (DESPUÉS de definir templates)
from app.routes import index_router, auth_router  # noqa: E402

app.include_router(index_router)
app.include_router(auth_router)
