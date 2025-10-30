"""
DEPRECADO: Este archivo está deprecado. Use src/__main__.py como entry point único.

Este archivo existe solo para compatibilidad con tests existentes.
Importa desde el módulo compartido _server.py.
"""

# Importar desde módulo compartido para compatibilidad
from _server import TrackHSServer

# Re-exportar para compatibilidad
__all__ = ["TrackHSServer"]
