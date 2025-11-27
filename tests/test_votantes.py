from fastapi.testclient import TestClient
import re

from app import app
from app.models.usuario import Usuario, RolUsuario
from app.config import obtener_sesion
from app.utils.auth import requerir_autenticacion


class FakeResult:
    def scalar_one_or_none(self):
        return None

    class _Scalars:
        def all(self):
            return []

    def scalars(self):
        return self._Scalars()


class FakeSession:
    async def execute(self, statement):
        return FakeResult()

    def add(self, obj):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass


async def fake_obtener_sesion():
    yield FakeSession()


def test_listar_incluye_boton_nuevo_votante():
    app.dependency_overrides[obtener_sesion] = fake_obtener_sesion
    client = TestClient(app)
    r = client.get("/votantes/")
    assert r.status_code == 200
    assert "/votantes/nuevo" in r.text


def test_busqueda_persistencia_valor_en_input():
    app.dependency_overrides[obtener_sesion] = fake_obtener_sesion
    client = TestClient(app)
    r = client.get("/votantes/?q=Juan")
    assert r.status_code == 200
    assert 'name="q"' in r.text
    assert 'value="Juan"' in r.text


def test_listar_incluye_parser_y_badges():
    app.dependency_overrides[obtener_sesion] = fake_obtener_sesion
    client = TestClient(app)
    r = client.get("/votantes/")
    assert r.status_code == 200
    assert 'id="filter-badges"' in r.text
    assert 'function parseFilters' in r.text


def test_nuevo_votante_redirige_si_no_autenticado():
    client = TestClient(app)
    r = client.get("/votantes/nuevo", allow_redirects=False)
    assert r.status_code == 303
    assert r.headers.get("location") == "/auth/login"


def test_formulario_nuevo_votante_muestra_csrf():
    app.dependency_overrides[obtener_sesion] = fake_obtener_sesion
    app.dependency_overrides[requerir_autenticacion] = lambda: Usuario(
        identificacion="9999999999",
        nombres="Admin",
        apellidos="Test",
        rol=RolUsuario.COORDINADOR,
        password="x",
    )
    client = TestClient(app)
    r = client.get("/votantes/nuevo")
    assert r.status_code == 200
    assert 'name="csrf_token"' in r.text


def test_crear_nuevo_votante_exitoso():
    app.dependency_overrides[obtener_sesion] = fake_obtener_sesion
    app.dependency_overrides[requerir_autenticacion] = lambda: Usuario(
        identificacion="9999999999",
        nombres="Admin",
        apellidos="Test",
        rol=RolUsuario.COORDINADOR,
        password="x",
    )
    client = TestClient(app)
    r = client.get("/votantes/nuevo")
    assert r.status_code == 200
    m = re.search(r'name="csrf_token" value="([^"]+)"', r.text)
    assert m
    token = m.group(1)
    data = {
        "identificacion": "1234567890",
        "nombres": "Juan",
        "apellidos": "Pérez",
        "csrf_token": token,
    }
    rp = client.post("/votantes/nuevo", data=data, allow_redirects=False)
    assert rp.status_code == 303
    assert rp.headers.get("location") == "/votantes/"
