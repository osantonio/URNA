# URNA - API con FastAPI

Proyecto de API REST construido con FastAPI, SQLModel y PostgreSQL.

## 📋 Requisitos

### Opción 1: Desarrollo Local
- Python 3.10 o superior
- PostgreSQL 12 o superior
- Visual Studio Build Tools (para Windows, necesario para asyncpg)

### Opción 2: Docker (Recomendado)
- Docker 20.10 o superior
- Docker Compose 2.0 o superior

## � Inicio Rápido con Docker (Recomendado)

La forma más rápida de ejecutar el proyecto es usando Docker:

```bash
# 1. Clonar el repositorio
cd d:\CODE\CODE\URNA

# 2. Construir y ejecutar los contenedores
docker-compose up --build
```

La aplicación estará disponible en:
- **Aplicación:** http://localhost:8000
- **Documentación (Swagger):** http://localhost:8000/docs
- **Documentación (ReDoc):** http://localhost:8000/redoc

### Comandos Útiles de Docker

```bash
# Ejecutar en segundo plano (detached mode)
docker-compose up -d

# Ver logs de la aplicación
docker-compose logs -f web

# Detener los contenedores
docker-compose down

# Reconstruir las imágenes
docker-compose build --no-cache

# Acceder al shell del contenedor web
docker-compose exec web bash
```

### Configuración de Docker

El archivo `docker-compose.yml` configura un servicio:

1. **web**: Aplicación FastAPI
   - Puerto: 8000
   - Hot-reload habilitado para desarrollo
   - Se conecta a tu base de datos PostgreSQL 17 en Neon

> [!IMPORTANT]
> Asegúrate de configurar tu `DATABASE_URL` en el archivo `.env` con las credenciales de tu base de datos Neon PostgreSQL 17.

## �🚀 Instalación (Desarrollo Local sin Docker)

### 1. Clonar el repositorio o crear el proyecto

```bash
cd d:\CODE\CODE\URNA
```

### 2. Crear y activar entorno virtual

El entorno virtual ya está creado en `.venv`. Para activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

Las dependencias principales ya están instaladas:
- ✅ FastAPI 0.121.3
- ✅ Uvicorn 0.38.0
- ✅ SQLModel 0.0.27
- ✅ python-dotenv 1.2.1
- ✅ Pydantic 2.12.4

#### Instalar asyncpg (opcional, requiere herramientas de compilación)

Para usar PostgreSQL con asyncpg, necesitas instalar Visual Studio Build Tools:

1. Descargar [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Instalar "Desktop development with C++"
3. Luego ejecutar:

```powershell
pip install asyncpg
```

**Alternativa:** Si no puedes instalar asyncpg, puedes usar `psycopg2-binary`:

```powershell
pip install psycopg2-binary
```

Y cambiar la URL de conexión en `.env`:
```
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/urna
```

### 4. Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo con tus credenciales:

```powershell
Copy-Item .env.example .env
```

Editar `.env` con tus datos de PostgreSQL:
```
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/urna
APP_NAME=URNA
DEBUG=True
```

## 🏃 Ejecutar la aplicación

```powershell
uvicorn main:app --reload
```

La API estará disponible en:
- **Aplicación:** http://localhost:8000
- **Documentación interactiva (Swagger):** http://localhost:8000/docs
- **Documentación alternativa (ReDoc):** http://localhost:8000/redoc

## 📁 Estructura del proyecto

```
URNA/
├── .venv/                  # Entorno virtual
├── app/                    # Aplicación principal
│   ├── __init__.py         # Configuración de FastAPI
│   ├── config/             # Configuración
│   │   ├── __init__.py
│   │   └── db.py           # Configuración de base de datos
│   ├── models/             # Modelos de SQLModel
│   │   ├── __init__.py
│   │   └── usuario.py      # Modelo de Usuario
│   ├── routes/             # Rutas de la API
│   │   ├── __init__.py
│   │   ├── index.py        # Rutas principales
│   │   └── auth.py         # Rutas de autenticación
│   └── schemas/            # Esquemas Pydantic
│       ├── __init__.py
│       └── auth.py         # Esquemas de autenticación
├── script/                 # Scripts de utilidad
│   └── ejemplo_usuario.py  # Ejemplos de creación de usuarios
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (no incluir en git)
└── README.md               # Este archivo
```

### Convenciones del Proyecto

- **Primera línea:** Todos los archivos `.py` incluyen su ruta relativa como comentario
  ```python
  # ./app/models/usuario.py
  ```

## 🔧 Uso

### Endpoints disponibles

- `GET /` - Endpoint raíz con información de la API
- `GET /salud` - Verificar estado de la API
- `POST /auth/login` - Autenticación de usuarios
- `GET /auth/verificar` - Verificar sesión (pendiente JWT)

### Crear tablas en la base de datos

Descomentar la línea en `app/__init__.py`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Iniciando aplicación URNA...")
    await crear_tablas()  # ← Descomentar esta línea
    print("✅ Aplicación iniciada correctamente")
```

## 📦 Dependencias instaladas

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| fastapi | 0.121.3 | Framework web moderno y rápido |
| uvicorn | 0.38.0 | Servidor ASGI |
| sqlmodel | 0.0.27 | ORM basado en SQLAlchemy y Pydantic |
| python-dotenv | 1.2.1 | Gestión de variables de entorno |
| pydantic | 2.12.4 | Validación de datos |
| pydantic-settings | 2.12.0 | Configuración con Pydantic |

## ⚠️ Notas importantes

1. **asyncpg en Windows:** Requiere Visual Studio Build Tools para compilarse. Si tienes problemas, usa `psycopg2-binary` como alternativa.

2. **Seguridad:** El archivo `.env` contiene información sensible y NO debe incluirse en el control de versiones.

3. **CORS:** La configuración actual permite todas las origenes (`allow_origins=["*"]`). En producción, especifica los dominios permitidos.

## 🛠️ Desarrollo

Para agregar nuevos modelos:

1. Crear el modelo en `models.py` heredando de `SQLModel`
2. Importar el modelo en `main.py`
3. Reiniciar la aplicación para que se creen las tablas

## 📝 Licencia

Este proyecto es de código abierto.
