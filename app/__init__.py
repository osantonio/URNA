# ./app/__init__.py

"""
Aplicación principal de URNA
Configuración de FastAPI con lifespan, templates Jinja2 y archivos estáticos
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
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

# Agregar middleware de contexto de usuario
# IMPORTANTE: Los middlewares se ejecutan en orden INVERSO al que se agregan
# Por lo tanto, agregamos primero UsuarioContextMiddleware y luego SessionMiddleware
# para que SessionMiddleware se ejecute ANTES y configure request.session
from app.middleware import UsuarioContextMiddleware  # noqa: E402

app.add_middleware(UsuarioContextMiddleware)

# Configurar SessionMiddleware para autenticación
# Este se ejecutará PRIMERO (antes que UsuarioContextMiddleware)
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está configurada en las variables de entorno")

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="urna_session",
    max_age=86400,  # 24 horas en segundos
    same_site="lax",
    https_only=False,  # Cambiar a True en producción con HTTPS
)

# Configurar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Configurar templates Jinja2 con context processor personalizado
# IMPORTANTE: Debe estar ANTES de importar las rutas
class CustomJinja2Templates(Jinja2Templates):
    """
    Extensión de Jinja2Templates que automáticamente inyecta
    el usuario desde request.state en cada respuesta de template
    """

    def TemplateResponse(self, *args, **kwargs):
        """
        Sobrescribe TemplateResponse para inyectar automáticamente
        el usuario en el contexto.
        Soporta ambas firmas:
        1. (request, name, context) - Estándar Starlette
        2. (name, context) - Conveniencia (requiere request en context)
        """
        # Detectar argumentos
        if len(args) > 0 and isinstance(args[0], str):
            # Firma: (name, context)
            name = args[0]
            context = args[1] if len(args) > 1 else kwargs.get("context", {})
            request = context.get("request")
            if not request:
                # Intentar recuperar request de kwargs si existe (raro pero posible)
                request = kwargs.get("request")
                if not request:
                    raise ValueError(
                        "Request es requerido en el contexto para CustomJinja2Templates"
                    )
        else:
            # Firma: (request, name, context)
            request = args[0]
            name = args[1]
            context = args[2] if len(args) > 2 else kwargs.get("context", {})

        if context is None:
            context = {}

        # Asegurar que request esté en el contexto (para url_for, etc)
        if "request" not in context:
            context["request"] = request

        # Inyectar usuario desde request.state si existe
        if request and not context.get("usuario"):
            context["usuario"] = getattr(request.state, "usuario", None)

        # Llamar al padre con la firma correcta (request, name, context)
        return super().TemplateResponse(request, name, context, **kwargs)


templates = CustomJinja2Templates(directory="app/templates")

# Exportar para uso en rutas
__all__ = ["app", "templates"]

# Registrar rutas (DESPUÉS de definir templates)
from app.routes import index_router, auth_router, votantes_router, documentacion_router  # noqa: E402

app.include_router(index_router)
app.include_router(auth_router)
app.include_router(votantes_router)
app.include_router(documentacion_router)
