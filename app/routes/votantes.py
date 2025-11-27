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
    request: Request, sesion: AsyncSession = Depends(obtener_sesion)):
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

    messages = request.session.pop("flash_messages", [])

    return jinja_templates.TemplateResponse(
        "votantes/listar.html",
        {
            "request": request,
            "votantes": votantes,
            "total": len(votantes),
            "messages": messages,
            "q": q,
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

    if telefono and (not telefono.isdigit() or len(telefono) != 10 or not telefono.startswith("3")):
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
