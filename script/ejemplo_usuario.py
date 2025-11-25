# ./script/ejemplo_usuario.py

"""
Script de ejemplo para crear usuarios en URNA
Este archivo muestra ejemplos de cómo crear instancias del modelo Usuario
"""

from app.models.usuario import Usuario, RolUsuario, TipoSexo

# Ejemplo 1: Usuario votante básico
ejemplo_votante = {
    "identificacion": "1234567890",
    "nombres": "Juan Carlos",
    "apellidos": "Pérez González",
    "telefono": "3001234567",
    "edad": 35,
    "sexo": TipoSexo.MASCULINO,
    "correoelectronico": "juan.perez@ejemplo.com",
    "barrio_vereda": "Centro",
    "lugar_votacion": "Escuela Central",
    "mesa_votacion": "15",
    "rol": RolUsuario.VOTANTE,
    "asignado_a": None,
    "password": "$2b$12$...",  # Hash de ejemplo - usar bcrypt en producción
    "calidad_score": 75,
}

# Ejemplo 2: Líder con equipo asignado
ejemplo_lider = {
    "identificacion": "9876543210",
    "nombres": "María Fernanda",
    "apellidos": "Rodríguez López",
    "telefono": "3109876543",
    "edad": 42,
    "sexo": TipoSexo.FEMENINO,
    "correoelectronico": "maria.rodriguez@ejemplo.com",
    "barrio_vereda": "San Antonio",
    "lugar_votacion": "Colegio Municipal",
    "mesa_votacion": "23",
    "rol": RolUsuario.LIDER,
    "asignado_a": None,  # Reporta directamente a coordinador
    "password": "$2b$12$...",
    "calidad_score": 90,
}

# Ejemplo 3: Coordinador de campaña
ejemplo_coordinador = {
    "identificacion": "5555555555",
    "nombres": "Carlos Alberto",
    "apellidos": "Gómez Martínez",
    "telefono": "3205555555",
    "edad": 50,
    "sexo": TipoSexo.MASCULINO,
    "correoelectronico": "carlos.gomez@ejemplo.com",
    "rol": RolUsuario.COORDINADOR,
    "asignado_a": None,  # Reporta al Estratega
    "password": "$2b$12$...",
    "calidad_score": 95,
}

# Ejemplo 4: Activista nuevo
ejemplo_activista = {
    "identificacion": "1111111111",
    "nombres": "Ana María",
    "apellidos": "Torres Sánchez",
    "telefono": "3151111111",
    "edad": 28,
    "sexo": TipoSexo.FEMENINO,
    "rol": RolUsuario.ACTIVISTA,
    "asignado_a": "9876543210",  # Asignado a María (líder)
    "password": "$2b$12$...",
    "calidad_score": 60,
}


def crear_usuario_ejemplo(datos: dict) -> Usuario:
    """
    Función helper para crear un usuario desde un diccionario

    Args:
        datos: Diccionario con los datos del usuario

    Returns:
        Instancia de Usuario
    """
    return Usuario(**datos)


if __name__ == "__main__":
    # Crear instancias de ejemplo
    votante = crear_usuario_ejemplo(ejemplo_votante)
    lider = crear_usuario_ejemplo(ejemplo_lider)
    coordinador = crear_usuario_ejemplo(ejemplo_coordinador)
    activista = crear_usuario_ejemplo(ejemplo_activista)

    print("✅ Ejemplos de usuarios creados:")
    print(f"  - {votante.nombres} {votante.apellidos} ({votante.rol.value})")
    print(f"  - {lider.nombres} {lider.apellidos} ({lider.rol.value})")
    print(
        f"  - {coordinador.nombres} {coordinador.apellidos} ({coordinador.rol.value})"
    )
    print(f"  - {activista.nombres} {activista.apellidos} ({activista.rol.value})")
