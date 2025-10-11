#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración en producción
"""

import os
import sys
from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Cargar variables de entorno
load_dotenv()

from trackhs_mcp.config import TrackHSConfig


def diagnose_production_config():
    """Diagnosticar la configuración de producción"""
    print("DIAGNOSTICO: Configuracion de Produccion")
    print("=" * 60)
    
    # Verificar variables de entorno
    print("\nVariables de Entorno:")
    print("-" * 30)
    
    env_vars = [
        "TRACKHS_API_URL",
        "TRACKHS_USERNAME", 
        "TRACKHS_PASSWORD",
        "TRACKHS_TIMEOUT"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "PASSWORD" in var:
                print(f"{var}: {'*' * len(value)} (configurada)")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: NO CONFIGURADA")
    
    # Crear configuración
    print(f"\nConfiguracion Creada:")
    print("-" * 30)
    
    try:
        config = TrackHSConfig.from_env()
        print(f"Base URL: {config.base_url}")
        print(f"Username: {config.username}")
        print(f"Password: {config.password[:10]}...")
        print(f"Timeout: {config.timeout}")
        
        # Validar URL
        if config.validate_url():
            print("URL validada: CORRECTA")
        else:
            print("URL validada: INCORRECTA")
            print(f"URL esperada debe contener: ihmvacations.trackhs.com")
            print(f"URL actual: {config.base_url}")
        
        # Verificar credenciales por defecto
        if config.username == "your_username_here":
            print("\nPROBLEMA DETECTADO:")
            print("- Usando credenciales de ejemplo")
            print("- Necesitas configurar TRACKHS_USERNAME en variables de entorno")
        
        if config.password == "your_password_here":
            print("\nPROBLEMA DETECTADO:")
            print("- Usando credenciales de ejemplo")
            print("- Necesitas configurar TRACKHS_PASSWORD en variables de entorno")
            
        # Verificar si está usando credenciales hardcodeadas
        if config.username == "aba99777416466b6bdc1a25223192ccb":
            print("\nINFORMACION:")
            print("- Usando credenciales hardcodeadas")
            print("- Estas credenciales pueden estar expiradas")
            print("- Considera usar variables de entorno para mayor seguridad")
            
    except Exception as e:
        print(f"Error creando configuracion: {e}")


def check_environment():
    """Verificar el entorno de ejecución"""
    print(f"\nEntorno de Ejecucion:")
    print("-" * 30)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'No especificado')}")
    print(f"Production: {os.getenv('PRODUCTION', 'No especificado')}")
    
    # Verificar si hay archivo .env
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"Archivo .env: ENCONTRADO")
    else:
        print(f"Archivo .env: NO ENCONTRADO")
        print("Crear archivo .env con las variables necesarias")


def suggest_solutions():
    """Sugerir soluciones para los problemas detectados"""
    print(f"\nSoluciones Recomendadas:")
    print("-" * 30)
    
    print("1. Configurar variables de entorno en el servidor de producción:")
    print("   export TRACKHS_API_URL=https://ihmvacations.trackhs.com/api")
    print("   export TRACKHS_USERNAME=tu_usuario_real")
    print("   export TRACKHS_PASSWORD=tu_password_real")
    print("   export TRACKHS_TIMEOUT=30")
    
    print("\n2. Crear archivo .env en el servidor:")
    print("   TRACKHS_API_URL=https://ihmvacations.trackhs.com/api")
    print("   TRACKHS_USERNAME=tu_usuario_real")
    print("   TRACKHS_PASSWORD=tu_password_real")
    print("   TRACKHS_TIMEOUT=30")
    
    print("\n3. Verificar que las credenciales sean válidas:")
    print("   - Contactar al administrador de TrackHS")
    print("   - Verificar que la cuenta esté activa")
    print("   - Confirmar que tenga permisos de API")
    
    print("\n4. Verificar conectividad de red:")
    print("   - El servidor debe poder acceder a https://ihmvacations.trackhs.com")
    print("   - Verificar firewall y proxy")
    print("   - Probar conectividad desde el servidor")


if __name__ == "__main__":
    diagnose_production_config()
    check_environment()
    suggest_solutions()
