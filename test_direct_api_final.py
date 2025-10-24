#!/usr/bin/env python3
"""
Script de prueba directo con la API usando las credenciales del .env
"""

import asyncio
import json
import httpx
import base64
import os
from datetime import datetime

# Cargar credenciales del archivo .env
def load_env_credentials():
    """Cargar credenciales del archivo .env"""
    credentials = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    credentials[key] = value
    except FileNotFoundError:
        print("⚠️ Archivo .env no encontrado")
    
    return credentials

# Cargar credenciales
env_vars = load_env_credentials()
username = env_vars.get('TRACKHS_USERNAME', 'demo_user')
password = env_vars.get('TRACKHS_PASSWORD', 'demo_password')
base_url = env_vars.get('TRACKHS_API_URL', 'https://ihmvacations.trackhs.com/api')

print(f"🔐 Usando credenciales: {username}")
print(f"🌐 Base URL: {base_url}")

# Crear headers con autenticación básica
auth_string = f"{username}:{password}"
auth_bytes = auth_string.encode('ascii')
auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {auth_b64}"
}

# Payload de prueba SIN el campo status (según la documentación)
TEST_PAYLOAD = {
    "dateReceived": "2025-01-24",
    "priority": 5,
    "summary": "Test work order - Aire acondicionado no funciona",
    "estimatedCost": 150.0,
    "estimatedTime": 120
}

async def test_api_direct():
    """Probar la API directamente"""
    print("🧪 PROBANDO API DIRECTAMENTE")
    print("=" * 50)
    
    endpoint = f"{base_url}/pms/maintenance/work-orders"
    print(f"📡 URL: {endpoint}")
    print(f"📦 Payload: {json.dumps(TEST_PAYLOAD, indent=2)}")
    print()
    
    async with httpx.AsyncClient() as client:
        try:
            print("🚀 Enviando petición POST...")
            response = await client.post(
                endpoint,
                json=TEST_PAYLOAD,
                headers=HEADERS,
                timeout=30.0
            )
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Headers: {dict(response.headers)}")
            print()
            
            if response.is_success:
                print("✅ ÉXITO - Work Order creado")
                result = response.json()
                print(f"📄 Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print("❌ ERROR - Falló la creación")
                print(f"📄 Response Body: {response.text}")
                
                # Intentar parsear como JSON para ver detalles
                try:
                    error_json = response.json()
                    print(f"📄 Error JSON: {json.dumps(error_json, indent=2)}")
                    
                    # Mostrar mensajes de validación si existen
                    if 'validation_messages' in error_json:
                        print(f"🔍 Validation Messages: {error_json['validation_messages']}")
                    if 'detail' in error_json:
                        print(f"🔍 Detail: {error_json['detail']}")
                        
                except Exception as e:
                    print(f"⚠️ No se pudo parsear como JSON: {e}")
                    
                return False
                    
        except httpx.RequestError as e:
            print(f"🌐 Error de red: {e}")
            return False
        except Exception as e:
            print(f"💥 Error inesperado: {e}")
            return False

async def test_with_status_field():
    """Probar con el campo status incluido"""
    print("\n" + "=" * 50)
    print("🔄 PROBANDO CON CAMPO STATUS")
    print("=" * 50)
    
    # Payload CON el campo status
    payload_with_status = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "status": "open",
        "summary": "Test work order with status",
        "estimatedCost": 100.0,
        "estimatedTime": 60
    }
    
    endpoint = f"{base_url}/pms/maintenance/work-orders"
    print(f"📡 URL: {endpoint}")
    print(f"📦 Payload: {json.dumps(payload_with_status, indent=2)}")
    print()
    
    async with httpx.AsyncClient() as client:
        try:
            print("🚀 Enviando petición POST con status...")
            response = await client.post(
                endpoint,
                json=payload_with_status,
                headers=HEADERS,
                timeout=30.0
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.is_success:
                print("✅ ÉXITO - Work Order creado con status")
                result = response.json()
                print(f"📄 Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print("❌ ERROR - Falló la creación con status")
                print(f"📄 Response: {response.text}")
                return False
                    
        except Exception as e:
            print(f"💥 Error: {e}")
            return False

async def test_minimal_payload():
    """Probar con payload mínimo"""
    print("\n" + "=" * 50)
    print("🔄 PROBANDO PAYLOAD MÍNIMO")
    print("=" * 50)
    
    # Payload mínimo con solo campos requeridos
    minimal_payload = {
        "dateReceived": "2025-01-24",
        "priority": 5,
        "summary": "Minimal test work order",
        "estimatedCost": 50.0,
        "estimatedTime": 30
    }
    
    endpoint = f"{base_url}/pms/maintenance/work-orders"
    print(f"📡 URL: {endpoint}")
    print(f"📦 Payload: {json.dumps(minimal_payload, indent=2)}")
    print()
    
    async with httpx.AsyncClient() as client:
        try:
            print("🚀 Enviando petición POST mínima...")
            response = await client.post(
                endpoint,
                json=minimal_payload,
                headers=HEADERS,
                timeout=30.0
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.is_success:
                print("✅ ÉXITO - Work Order creado con payload mínimo")
                result = response.json()
                print(f"📄 Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print("❌ ERROR - Falló la creación con payload mínimo")
                print(f"📄 Response: {response.text}")
                return False
                    
        except Exception as e:
            print(f"💥 Error: {e}")
            return False

if __name__ == "__main__":
    print("🔧 TRACKHS API - DIRECT TEST WITH .ENV CREDENTIALS")
    print("=" * 70)
    
    # Ejecutar pruebas
    success1 = asyncio.run(test_api_direct())
    
    if not success1:
        success2 = asyncio.run(test_with_status_field())
        
        if not success2:
            success3 = asyncio.run(test_minimal_payload())
            
            if not success3:
                print("\n❌ Todas las pruebas fallaron")
                print("🔍 Posibles causas:")
                print("  1. Credenciales incorrectas en .env")
                print("  2. Permisos insuficientes")
                print("  3. API no disponible")
                print("  4. Formato de datos incorrecto")
    
    print("\n" + "=" * 70)
    print("🏁 PRUEBAS COMPLETADAS")
