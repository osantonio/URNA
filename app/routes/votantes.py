# ./app/routes/votantes.py

"""
Rutas para gestión de votantes
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import sqlalchemy as sa

from app.config import obtener_sesion
from app.models import Usuario, RolUsuario, TipoSexo
from app import templates as jinja_templates
from app.utils.auth import requerir_autenticacion, hashear_password
import secrets

router = APIRouter(prefix="/votantes", tags=["Votantes"])


@router.get("/", response_class=HTMLResponse)
async def listar_votantes(
    request: Request, sesion: AsyncSession = Depends(obtener_sesion)
):
    """
    Lista todos los votantes/usuarios del sistema
    """
    q = request.query_params.get("q", "").strip()

    if q:
        pattern = f"%{q}%"
        statement = (
            select(Usuario)
            .where(
                sa.or_(
                    Usuario.nombres.ilike(pattern),
                    Usuario.apellidos.ilike(pattern),
                    Usuario.identificacion.like(pattern),
                    Usuario.telefono.like(pattern),
                )
            )
            .order_by(Usuario.fecha_registro.desc())
        )
    else:
        statement = select(Usuario).order_by(Usuario.fecha_registro.desc())
    resultado = await sesion.execute(statement)
    votantes = resultado.scalars().all()

    ids_referentes = list(
        {v.asignado_a for v in votantes if getattr(v, "asignado_a", None)}
    )
    referentes = {}
    if ids_referentes:
        ref_stmt = select(Usuario).where(Usuario.identificacion.in_(ids_referentes))
        ref_res = await sesion.execute(ref_stmt)
        ref_users = ref_res.scalars().all()
        referentes = {u.identificacion: u for u in ref_users}

    messages = request.session.pop("flash_messages", [])

    return jinja_templates.TemplateResponse(
        "votantes/listar.html",
        {
            "request": request,
            "votantes": votantes,
            "total": len(votantes),
            "messages": messages,
            "q": q,
            "referentes": referentes,
        },
    )


@router.get("/nuevo", response_class=HTMLResponse)
async def nuevo_votante_form(
    request: Request, usuario: Usuario = Depends(requerir_autenticacion)
):
    if usuario.rol not in [
        RolUsuario.LIDER,
        RolUsuario.JEFE_DE_ZONA,
        RolUsuario.COORDINADOR,
        RolUsuario.ESTRATEGA,
    ]:
        request.session.setdefault("flash_messages", []).append(
            "No autorizado para crear votantes"
        )
        return RedirectResponse(url="/votantes/", status_code=303)

    csrf_token = secrets.token_urlsafe(32)
    request.session["csrf_token"] = csrf_token

    return jinja_templates.TemplateResponse(
        "votantes/nuevo.html",
        {
            "request": request,
            "csrf_token": csrf_token,
            "sexo_opciones": [s.value for s in TipoSexo],
        },
    )


@router.post("/nuevo")
async def crear_nuevo_votante(
    request: Request,
    identificacion: str = Form(...),
    nombres: str = Form(...),
    apellidos: str = Form(...),
    telefono: str | None = Form(None),
    edad: int | None = Form(None),
    sexo: str | None = Form(None),
    correoelectronico: str | None = Form(None),
    barrio_vereda: str | None = Form(None),
    lugar_votacion: str | None = Form(None),
    mesa_votacion: str | None = Form(None),
    csrf_token: str = Form(...),
    sesion: AsyncSession = Depends(obtener_sesion),
    usuario: Usuario = Depends(requerir_autenticacion),
):
    if usuario.rol not in [
        RolUsuario.LIDER,
        RolUsuario.JEFE_DE_ZONA,
        RolUsuario.COORDINADOR,
        RolUsuario.ESTRATEGA,
    ]:
        request.session.setdefault("flash_messages", []).append(
            "No autorizado para crear votantes"
        )
        return RedirectResponse(url="/votantes/", status_code=303)

    expected_csrf = request.session.get("csrf_token")
    if not expected_csrf or csrf_token != expected_csrf:
        return jinja_templates.TemplateResponse(
            "votantes/nuevo.html",
            {
                "request": request,
                "error": "Solicitud inválida (CSRF)",
                "csrf_token": expected_csrf or "",
                "sexo_opciones": [s.value for s in TipoSexo],
            },
            status_code=400,
        )

    if not identificacion.isdigit() or not (6 <= len(identificacion) <= 10):
        return jinja_templates.TemplateResponse(
            "votantes/nuevo.html",
            {
                "request": request,
                "error": "La identificación debe tener 6-10 dígitos",
                "csrf_token": expected_csrf,
                "sexo_opciones": [s.value for s in TipoSexo],
            },
            status_code=400,
        )

    if telefono and (
        not telefono.isdigit() or len(telefono) != 10 or not telefono.startswith("3")
    ):
        return jinja_templates.TemplateResponse(
            "votantes/nuevo.html",
            {
                "request": request,
                "error": "Teléfono inválido",
                "csrf_token": expected_csrf,
                "sexo_opciones": [s.value for s in TipoSexo],
            },
            status_code=400,
        )

    if edad is not None and (edad < 18 or edad > 120):
        return jinja_templates.TemplateResponse(
            "votantes/nuevo.html",
            {
                "request": request,
                "error": "Edad fuera de rango",
                "csrf_token": expected_csrf,
                "sexo_opciones": [s.value for s in TipoSexo],
            },
            status_code=400,
        )

    statement = select(Usuario).where(Usuario.identificacion == identificacion)
    resultado = await sesion.execute(statement)
    existente = resultado.scalar_one_or_none()
    if existente:
        return jinja_templates.TemplateResponse(
            "votantes/nuevo.html",
            {
                "request": request,
                "error": "Ya existe un usuario con esa identificación",
                "csrf_token": expected_csrf,
                "sexo_opciones": [s.value for s in TipoSexo],
            },
            status_code=400,
        )

    random_password = secrets.token_urlsafe(12)
    password_hash = hashear_password(random_password)

    sexo_enum = None
    if sexo in [s.value for s in TipoSexo]:
        sexo_enum = TipoSexo(sexo)

    nuevo = Usuario(
        identificacion=identificacion,
        nombres=nombres,
        apellidos=apellidos,
        telefono=telefono,
        edad=edad,
        sexo=sexo_enum,
        correoelectronico=correoelectronico,
        barrio_vereda=barrio_vereda,
        lugar_votacion=lugar_votacion,
        mesa_votacion=mesa_votacion,
        rol=RolUsuario.VOTANTE,
        asignado_a=usuario.identificacion,
        password=password_hash,
    )

    try:
        sesion.add(nuevo)
        await sesion.commit()
        request.session.pop("csrf_token", None)
        request.session.setdefault("flash_messages", []).append(
            "Votante creado correctamente"
        )
        return RedirectResponse(url="/votantes/", status_code=303)
    except Exception:
        await sesion.rollback()
        return jinja_templates.TemplateResponse(
            "votantes/nuevo.html",
            {
                "request": request,
                "error": "No se pudo crear el votante",
                "csrf_token": expected_csrf,
                "sexo_opciones": [s.value for s in TipoSexo],
            },
            status_code=500,
        )


# ============================================================================
# FUNCIONES AUXILIARES PARA VISTA DE PERFIL
# ============================================================================


async def verificar_permiso_ver_perfil(
    sesion: AsyncSession, identificacion_perfil: str, identificacion_autenticado: str
) -> bool:
    """
    Verifica si el usuario autenticado puede ver el perfil solicitado.

    Reglas:
    1. Puede ver su propio perfil
    2. Puede ver perfiles de sus referidos descendentes (directos o indirectos)

    Args:
        sesion: Sesión de base de datos
        identificacion_perfil: ID del perfil que se quiere ver
        identificacion_autenticado: ID del usuario autenticado

    Returns:
        True si tiene permiso, False en caso contrario
    """
    # Caso 1: Ver su propio perfil
    if identificacion_perfil == identificacion_autenticado:
        return True

    # Caso 2: Verificar si el perfil es un referido descendente
    from sqlalchemy import text

    query = text("""
        WITH RECURSIVE red_descendente AS (
            SELECT identificacion, 1 as nivel
            FROM usuario
            WHERE asignado_a = :id_autenticado
            
            UNION ALL
            
            SELECT u.identificacion, r.nivel + 1
            FROM usuario u
            INNER JOIN red_descendente r ON u.asignado_a = r.identificacion
        )
        SELECT EXISTS(
            SELECT 1 FROM red_descendente 
            WHERE identificacion = :id_perfil
        ) as tiene_permiso
    """)

    resultado = await sesion.execute(
        query,
        {
            "id_autenticado": identificacion_autenticado,
            "id_perfil": identificacion_perfil,
        },
    )

    return resultado.scalar() or False


async def obtener_referidos_directos_agrupados(
    sesion: AsyncSession, identificacion: str
) -> dict:
    """
    Obtiene los referidos directos de un usuario agrupados por rol.

    Args:
        sesion: Sesión de base de datos
        identificacion: ID del usuario

    Returns:
        Diccionario con referidos agrupados por rol
    """
    from collections import defaultdict
    from sqlmodel import func

    # Consultar referidos directos
    statement = (
        select(Usuario)
        .where(Usuario.asignado_a == identificacion)
        .order_by(Usuario.rol, Usuario.fecha_registro.desc())
    )

    resultado = await sesion.execute(statement)
    referidos = resultado.scalars().all()

    # Agrupar por rol
    agrupados = defaultdict(list)
    for ref in referidos:
        agrupados[ref.rol.value].append(
            {
                "identificacion": ref.identificacion,
                "nombre_completo": ref.nombre_completo,
                "nombres": ref.nombres,
                "apellidos": ref.apellidos,
                "rol": ref.rol.value,
                "mesa_votacion": ref.mesa_votacion,
                "lugar_votacion": ref.lugar_votacion,
                "telefono": ref.telefono,
                "tiene_referidos": False,  # Se actualiza después
            }
        )

    # Verificar cuáles tienen referidos (para mostrar ícono de expandir)
    for rol_grupo in agrupados.values():
        for persona in rol_grupo:
            count_query = select(func.count(Usuario.identificacion)).where(
                Usuario.asignado_a == persona["identificacion"]
            )
            count_result = await sesion.execute(count_query)
            persona["tiene_referidos"] = count_result.scalar() > 0

    return dict(agrupados)


async def obtener_metricas_red_completa(
    sesion: AsyncSession, identificacion: str
) -> dict:
    """
    Calcula métricas de toda la red descendente usando CTE recursiva.

    Args:
        sesion: Sesión de base de datos
        identificacion: ID del usuario raíz

    Returns:
        Diccionario con métricas de la red completa
    """
    from sqlalchemy import text

    query = text("""
        WITH RECURSIVE red_completa AS (
            SELECT identificacion, rol, 1 as nivel
            FROM usuario
            WHERE asignado_a = :id_raiz
            
            UNION ALL
            
            SELECT u.identificacion, u.rol, r.nivel + 1
            FROM usuario u
            INNER JOIN red_completa r ON u.asignado_a = r.identificacion
        )
        SELECT 
            COUNT(*) as total,
            MAX(nivel) as niveles_profundidad,
            rol,
            COUNT(*) as cantidad
        FROM red_completa
        GROUP BY rol
    """)

    resultado = await sesion.execute(query, {"id_raiz": identificacion})
    filas = resultado.fetchall()

    if not filas:
        return {"total_red": 0, "niveles_profundidad": 0, "por_rol": {}}

    return {
        "total_red": sum(f.cantidad for f in filas),
        "niveles_profundidad": max((f.niveles_profundidad for f in filas), default=0),
        "por_rol": {f.rol: f.cantidad for f in filas},
    }


# ============================================================================
# RUTAS PARA VISTA DE PERFIL
# ============================================================================


@router.get("/{identificacion}", response_class=HTMLResponse)
async def ver_perfil_votante(
    identificacion: str,
    request: Request,
    sesion: AsyncSession = Depends(obtener_sesion),
    usuario_autenticado: Usuario = Depends(requerir_autenticacion),
):
    """
    Muestra el perfil detallado de un votante con árbol jerárquico de referidos.

    Control de acceso:
    - El usuario puede ver su propio perfil
    - El usuario puede ver perfiles de sus referidos descendentes
    """
    # Verificar permiso
    tiene_permiso = await verificar_permiso_ver_perfil(
        sesion, identificacion, usuario_autenticado.identificacion
    )

    if not tiene_permiso:
        request.session.setdefault("flash_messages", []).append(
            "No tienes permiso para ver este perfil"
        )
        return RedirectResponse(url="/votantes/", status_code=303)

    # Obtener usuario
    usuario = await sesion.get(Usuario, identificacion)
    if not usuario:
        request.session.setdefault("flash_messages", []).append("Usuario no encontrado")
        return RedirectResponse(url="/votantes/", status_code=303)

    # Obtener referidos directos agrupados por rol
    referidos_agrupados = await obtener_referidos_directos_agrupados(
        sesion, identificacion
    )

    # Obtener métricas de red completa
    metricas = await obtener_metricas_red_completa(sesion, identificacion)

    # Obtener referente (si tiene)
    referente = None
    if usuario.asignado_a:
        referente = await sesion.get(Usuario, usuario.asignado_a)

    return jinja_templates.TemplateResponse(
        "votantes/ver.html",
        {
            "request": request,
            "usuario": usuario,
            "referidos_agrupados": referidos_agrupados,
            "metricas": metricas,
            "referente": referente,
        },
    )


@router.get("/{identificacion}/referidos")
async def obtener_referidos_api(
    identificacion: str,
    sesion: AsyncSession = Depends(obtener_sesion),
    usuario_autenticado: Usuario = Depends(requerir_autenticacion),
):
    """
    API JSON para obtener referidos directos de un usuario.
    Usado para carga dinámica al expandir nodos en el árbol.

    Returns:
        JSON con referidos agrupados por rol
    """
    # Verificar permiso
    tiene_permiso = await verificar_permiso_ver_perfil(
        sesion, identificacion, usuario_autenticado.identificacion
    )

    if not tiene_permiso:
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="No autorizado")

    # Obtener usuario
    usuario = await sesion.get(Usuario, identificacion)
    if not usuario:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener referidos agrupados
    referidos_por_rol = await obtener_referidos_directos_agrupados(
        sesion, identificacion
    )

    # Obtener métricas
    metricas = await obtener_metricas_red_completa(sesion, identificacion)

    return {
        "identificacion": identificacion,
        "nombre_completo": usuario.nombre_completo,
        "referidos_por_rol": referidos_por_rol,
        "total_referidos_directos": sum(
            len(personas) for personas in referidos_por_rol.values()
        ),
        "total_red_completa": metricas["total_red"],
    }
