#!/usr/bin/env python3
"""
Script simple para verificar credenciales de TrackHS
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def check_credentials():
    """Verifica las credenciales configuradas"""
    print("VERIFICACION DE CREDENCIALES TRACKHS")
    print("=" * 40)

    # Verificar variables de entorno
    print("\nVariables de entorno:")
    api_url = os.getenv("TRACKHS_API_URL")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    print(f"TRACKHS_API_URL: {api_url}")
    print(f"TRACKHS_USERNAME: {username}")
    print(f"TRACKHS_PASSWORD: {'*' * len(password) if password else 'No configurada'}")

    # Verificar si las credenciales están configuradas
    if not username or not password:
        print("\nERROR: Credenciales no configuradas")
        print("Configura TRACKHS_USERNAME y TRACKHS_PASSWORD")
        return False

    # Analizar formato de credenciales
    print("\nAnalisis de credenciales:")

    # Verificar si parecen estar encriptadas
    username_is_hex = len(username) == 32 and all(
        c in "0123456789ABCDEF" for c in username.upper()
    )
    password_is_hex = len(password) == 32 and all(
        c in "0123456789ABCDEF" for c in password.upper()
    )

    print(f"Username parece encriptado (hex): {username_is_hex}")
    print(f"Password parece encriptado (hex): {password_is_hex}")

    if username_is_hex or password_is_hex:
        print("\nADVERTENCIA: Las credenciales parecen estar encriptadas")
        print("La API de TrackHS espera credenciales en texto plano")
        print("Necesitas configurar las credenciales reales")

    # Intentar crear configuración
    try:
        print("\nCreando configuracion...")
        from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig

        config = TrackHSConfig.from_env()
        print("Configuracion creada exitosamente")

        # Crear autenticación
        print("\nCreando autenticacion...")
        from trackhs_mcp.infrastructure.utils.auth import TrackHSAuth

        auth = TrackHSAuth(config)
        print("Autenticacion creada exitosamente")

        # Mostrar header de autorización (sin revelar credenciales)
        auth_header = auth.get_auth_header()
        print(f"\nHeader de Autorizacion generado:")
        print(f"{auth_header[:20]}...")

        return True

    except Exception as e:
        print(f"\nERROR al crear configuracion: {e}")
        return False


if __name__ == "__main__":
    print("Iniciando verificacion de credenciales...")

    if check_credentials():
        print("\nEXITO: Credenciales configuradas correctamente")
    else:
        print("\nERROR: Credenciales no configuradas o invalidas")
        print("\nSoluciones recomendadas:")
        print("1. Verifica que las credenciales sean las reales de TrackHS")
        print("2. Asegurate de que las credenciales esten en texto plano")
        print("3. Verifica que la URL de la API sea correcta")
        print(
            "4. Contacta al administrador de TrackHS si las credenciales son correctas"
        )
