# ./main.py

"""
Punto de entrada principal de la aplicación URNA
"""

from app import app  # noqa: F401

# Este archivo solo importa la app configurada en app/__init__.py
# Para ejecutar: uvicorn main:app --reload
