"""
Entry point para FastMCP Cloud
Ejecuta el servidor TrackHS MCP
"""

import os
import sys

# Agregar el directorio src al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import main

if __name__ == "__main__":
    main()
