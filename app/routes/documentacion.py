from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import os

from app import templates as jinja_templates
from app.utils import requerir_autenticacion

router = APIRouter(prefix="/documentacion", tags=["Documentación"])


def _maybe_auth():
    env = os.getenv("ENVIRONMENT", "development").lower()
    return env != "development"


@router.get("/", response_class=HTMLResponse)
async def doc_index(request: Request):
    if _maybe_auth():
        try:
            await requerir_autenticacion(request)  # type: ignore[arg-type]
        except Exception:
            return RedirectResponse(url="/auth/login", status_code=303)
    return jinja_templates.TemplateResponse(
        "documentacion/index.html",
        {"request": request},
    )


@router.get("/busqueda", response_class=HTMLResponse)
async def doc_busqueda(request: Request):
    if _maybe_auth():
        try:
            await requerir_autenticacion(request)  # type: ignore[arg-type]
        except Exception:
            return RedirectResponse(url="/auth/login", status_code=303)
    return jinja_templates.TemplateResponse(
        "documentacion/busqueda.html",
        {"request": request},
    )


@router.get("/modelo-datos", response_class=HTMLResponse)
async def doc_modelo_datos(request: Request):
    if _maybe_auth():
        try:
            await requerir_autenticacion(request)  # type: ignore[arg-type]
        except Exception:
            return RedirectResponse(url="/auth/login", status_code=303)
    return jinja_templates.TemplateResponse(
        "documentacion/modelo_datos.html",
        {"request": request},
    )


@router.get("/base-datos", response_class=HTMLResponse)
async def doc_base_datos(request: Request):
    if _maybe_auth():
        try:
            await requerir_autenticacion(request)  # type: ignore[arg-type]
        except Exception:
            return RedirectResponse(url="/auth/login", status_code=303)
    return jinja_templates.TemplateResponse(
        "documentacion/base_datos.html",
        {"request": request},
    )


@router.get("/templates", response_class=HTMLResponse)
async def doc_templates(request: Request):
    if _maybe_auth():
        try:
            await requerir_autenticacion(request)  # type: ignore[arg-type]
        except Exception:
            return RedirectResponse(url="/auth/login", status_code=303)
    return jinja_templates.TemplateResponse(
        "documentacion/templates.html",
        {"request": request},
    )

