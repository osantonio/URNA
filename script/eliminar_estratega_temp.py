# Script temporal para eliminar y recrear el usuario estratega con password hasheado

import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
proyecto_raiz = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_raiz))

import asyncio  # noqa: E402
from sqlmodel import select  # noqa: E402
from app.models.usuario import Usuario  # noqa: E402
from app.config import async_session_maker  # noqa: E402


async def eliminar_estratega():
    """Elimina el usuario estratega existente"""
    async with async_session_maker() as sesion:
        try:
            statement = select(Usuario).where(Usuario.identificacion == "1000000001")
            resultado = await sesion.execute(statement)
            usuario = resultado.scalar_one_or_none()

            if usuario:
                await sesion.delete(usuario)
                await sesion.commit()
                print("✅ Usuario estratega eliminado")
            else:
                print("⚠️  No se encontró el usuario estratega")

        except Exception as error:
            await sesion.rollback()
            print(f"❌ Error: {error}")
            raise


if __name__ == "__main__":
    asyncio.run(eliminar_estratega())
