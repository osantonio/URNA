# ./script/crear_estratega.py

"""
Script para crear un usuario Estratega en URNA
El Estratega es el nivel máximo de poder en la jerarquía (Nivel 5)
"""

import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
# IMPORTANTE: Esto debe estar ANTES de importar app
proyecto_raiz = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_raiz))

import asyncio  # noqa: E402
from app.models.usuario import Usuario, RolUsuario, TipoSexo  # noqa: E402
from app.config import async_session_maker  # noqa: E402
from app.utils.auth import hashear_password  # noqa: E402


async def crear_estratega():
    """
    Crea un usuario con rol de Estratega en la base de datos

    El Estratega es el nivel más alto de la jerarquía electoral:
    - Nivel 5 - MÁXIMO poder
    - No reporta a nadie (asignado_a = None)
    - Tiene acceso completo al sistema
    """

    # Datos del Estratega
    estratega_data = {
        "identificacion": "1000000001",
        "nombres": "Roberto Carlos",
        "apellidos": "Mendoza Vargas",
        "telefono": "3001000001",
        "edad": 55,
        "sexo": TipoSexo.MASCULINO,
        "correoelectronico": "roberto.mendoza@urna.com",
        "barrio_vereda": "El Poblado",
        "lugar_votacion": "Universidad Central",
        "mesa_votacion": "1",
        "rol": RolUsuario.ESTRATEGA,
        "asignado_a": None,  # El Estratega no reporta a nadie
        "password": hashear_password("estratega2024"),  # Password hasheado con bcrypt
        "calidad_score": 100,  # Máximo score
    }

    # Crear instancia del usuario
    estratega = Usuario(**estratega_data)

    # Guardar en base de datos
    async with async_session_maker() as sesion:
        try:
            # Verificar si ya existe
            from sqlmodel import select

            statement = select(Usuario).where(
                Usuario.identificacion == estratega.identificacion
            )
            resultado = await sesion.execute(statement)
            usuario_existente = resultado.scalar_one_or_none()

            if usuario_existente:
                print(
                    f"⚠️  El Estratega con identificación {estratega.identificacion} ya existe"
                )
                print(
                    f"   Nombre: {usuario_existente.nombres} {usuario_existente.apellidos}"
                )
                return usuario_existente

            # Agregar y confirmar
            sesion.add(estratega)
            await sesion.commit()
            await sesion.refresh(estratega)

            print("✅ Estratega creado exitosamente:")
            print(f"   Identificación: {estratega.identificacion}")
            print(f"   Nombre: {estratega.nombres} {estratega.apellidos}")
            print(f"   Rol: {estratega.rol.value} (Nivel 5 - MÁXIMO PODER)")
            print(f"   Calidad Score: {estratega.calidad_score}/100")
            print(f"   Email: {estratega.correoelectronico}")

            return estratega

        except Exception as error:
            await sesion.rollback()
            print(f"❌ Error al crear Estratega: {error}")
            raise


async def main():
    """Función principal para ejecutar el script"""
    print("=" * 60)
    print("CREACIÓN DE USUARIO ESTRATEGA - URNA")
    print("=" * 60)
    print()

    await crear_estratega()

    print()
    print("=" * 60)
    print("Proceso completado")
    print("=" * 60)


if __name__ == "__main__":
    # Ejecutar el script
    asyncio.run(main())
