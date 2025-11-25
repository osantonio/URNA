# Dockerfile multi-etapa para aplicación URNA con FastAPI

# Etapa 1: Builder - Instalación de dependencias
FROM python:3.11-slim as builder

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes de Python
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Etapa 2: Runtime - Imagen final optimizada
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar solo las dependencias de runtime necesarias
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias de Python desde la etapa builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Crear usuario no-root para ejecutar la aplicación
RUN useradd -m -u 1000 urna_user && \
    chown -R urna_user:urna_user /app

# Copiar código de la aplicación
COPY --chown=urna_user:urna_user . .

# Cambiar a usuario no-root
USER urna_user

# Exponer puerto de la aplicación
EXPOSE 8000

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/salud')" || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
