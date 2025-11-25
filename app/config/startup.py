# ./app/config/startup.py

"""
Utilidades para el ciclo de vida de la aplicación
"""

import os
from app.config.db import crear_tablas


async def init_db_urna():
    """
    Inicializa la base de datos según el entorno

    - En desarrollo: Crea tablas automáticamente
    - En producción/staging: Solo muestra advertencia (usar migraciones)
    """
    entorno = os.getenv("ENVIRONMENT", "development")

    if entorno == "development":
        print("📋 Creando tablas (modo desarrollo)...")
        await crear_tablas()
    else:
        print(
            f"⚠️  Modo {entorno}: Tablas NO se crean automáticamente (usar migraciones)"
        )


def app_urna_abierta():
    """Muestra mensaje cuando URNA se abre (inicio de la aplicación)"""
    print("🚀 Iniciando aplicación URNA...")


def app_urna_cerrada():
    """Muestra mensaje cuando URNA se cierra (shutdown de la aplicación)"""
    print("👋 Cerrando aplicación URNA...")


def app_urna_iniciada():
    """Muestra mensaje cuando URNA está lista para recibir peticiones"""
    print("✅ Aplicación iniciada correctamente")
