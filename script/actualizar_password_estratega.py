# Script para actualizar el password del estratega a un hash bcrypt válido

import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
proyecto_raiz = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_raiz))

import asyncio  # noqa: E402
from sqlmodel import select  # noqa: E402
from app.models.usuario import Usuario  # noqa: E402
from app.config import async_session_maker  # noqa: E402
from app.utils.auth import hashear_password  # noqa: E402


async def actualizar_password_estratega():
    """Actualiza el password del estratega a un hash bcrypt válido"""
    async with async_session_maker() as sesion:
        try:
            # Buscar el usuario estratega
            statement = select(Usuario).where(Usuario.identificacion == "1000000001")
            resultado = await sesion.execute(statement)
            usuario = resultado.scalar_one_or_none()

            if not usuario:
                print("❌ No se encontró el usuario estratega")
                return

            # Actualizar el password con un hash válido
            print("🔐 Hasheando password...")
            nuevo_password_hash = hashear_password("estratega2024")
            usuario.password = nuevo_password_hash

            # Guardar cambios
            sesion.add(usuario)
            await sesion.commit()
            await sesion.refresh(usuario)

            print("✅ Password actualizado correctamente")
            print(f"   Usuario: {usuario.nombres} {usuario.apellidos}")
            print(f"   Identificación: {usuario.identificacion}")
            print(f"   Password: estratega2024 (ahora hasheado con bcrypt)")

        except Exception as error:
            await sesion.rollback()
            print(f"❌ Error: {error}")
            import traceback

            traceback.print_exc()
            raise


if __name__ == "__main__":
    asyncio.run(actualizar_password_estratega())
