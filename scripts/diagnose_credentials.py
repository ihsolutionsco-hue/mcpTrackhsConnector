#!/usr/bin/env python3
"""
Script de diagnóstico para verificar credenciales de TrackHS
"""

import os
import sys
from pathlib import Path

# Cargar variables de entorno desde .env
from dotenv import load_dotenv

load_dotenv()

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from server_logic import create_api_client
from utils.logger import get_logger


def main():
    """Función principal de diagnóstico"""
    logger = get_logger(__name__)

    print("DIAGNOSTICO DE CREDENCIALES TRACKHS")
    print("=" * 50)

    # Verificar variables de entorno
    print("\n1. VERIFICANDO VARIABLES DE ENTORNO:")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    api_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")

    print(f"   TRACKHS_USERNAME: {'SET' if username else 'NOT SET'}")
    print(f"   TRACKHS_PASSWORD: {'SET' if password else 'NOT SET'}")
    print(f"   TRACKHS_API_URL: {api_url}")

    if not username or not password:
        print("\nPROBLEMA IDENTIFICADO:")
        print("   Las credenciales de TrackHS no estan configuradas.")
        print("   Esto explica por que todos los endpoints retornan 0 resultados.")
        print("\nSOLUCION:")
        print("   1. Crear archivo .env en la raiz del proyecto")
        print("   2. Agregar las credenciales:")
        print("      TRACKHS_USERNAME=tu_usuario")
        print("      TRACKHS_PASSWORD=tu_contrasena")
        print("      TRACKHS_API_URL=https://ihmvacations.trackhs.com")
        return False

    # Intentar crear cliente API
    print("\n2. VERIFICANDO CONEXION A API:")
    try:
        api_client = create_api_client()
        if api_client:
            print("   Cliente API creado exitosamente")

            # Probar conexión básica
            print("\n3. PROBANDO CONEXION BASICA:")
            try:
                # Hacer una llamada simple para verificar autenticación
                result = api_client.get("api/pms/units", {"page": 1, "size": 1})
                print("   Conexion a API exitosa")
                print(
                    f"   Respuesta: {type(result)} con {len(result) if isinstance(result, dict) else 'N/A'} claves"
                )

                # Verificar si hay datos
                if isinstance(result, dict):
                    units = result.get("units", [])
                    if units:
                        print(f"   Se encontraron {len(units)} unidades")
                    else:
                        print(
                            "   No se encontraron unidades (puede ser normal si no hay datos)"
                        )
                        print("   Estructura de respuesta:")
                        for key, value in result.items():
                            print(f"      {key}: {type(value).__name__}")

            except Exception as api_error:
                print(f"   Error en llamada a API: {str(api_error)}")
                print(f"   Tipo de error: {type(api_error).__name__}")
                return False
        else:
            print("   No se pudo crear cliente API")
            return False

    except Exception as client_error:
        print(f"   Error creando cliente API: {str(client_error)}")
        print(f"   Tipo de error: {type(client_error).__name__}")
        return False

    print("\nDIAGNOSTICO COMPLETADO")
    print("   El sistema esta configurado correctamente.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
