"""
Script para probar el esquema de paginación de la API TrackHS.
Determina si la API usa paginación 0-based o 1-based.
"""

import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv("TRACKHS_API_URL", "https://api.trackhs.com")
username = os.getenv("TRACKHS_USERNAME")
password = os.getenv("TRACKHS_PASSWORD")

if not username or not password:
    print("❌ Credenciales no configuradas")
    sys.exit(1)

client = httpx.Client(auth=(username, password), timeout=30)

print("🔍 Probando paginación de la API TrackHS...")
print()

# Test 1: page=0
print("Test 1: page=0, size=2")
try:
    r1 = client.get(f"{api_url}/api/pms/units", params={"page": 0, "size": 2})
    print(f"  Status: {r1.status_code}")
    if r1.status_code == 200:
        data = r1.json()
        print(f'  Response page field: {data.get("page")}')
        print(f'  Total items: {data.get("total_items")}')
        units1 = data.get("_embedded", {}).get("units", [])
        print(f"  Units returned: {len(units1)}")
        if units1:
            unit_ids_0 = [u.get("id") for u in units1]
            print(f"  Unit IDs: {unit_ids_0}")
    else:
        print(f"  Error: {r1.text[:200]}")
except Exception as e:
    print(f"  Error: {e}")

print()

# Test 2: page=1
print("Test 2: page=1, size=2")
try:
    r2 = client.get(f"{api_url}/api/pms/units", params={"page": 1, "size": 2})
    print(f"  Status: {r2.status_code}")
    if r2.status_code == 200:
        data = r2.json()
        print(f'  Response page field: {data.get("page")}')
        print(f'  Total items: {data.get("total_items")}')
        units2 = data.get("_embedded", {}).get("units", [])
        print(f"  Units returned: {len(units2)}")
        if units2:
            unit_ids_1 = [u.get("id") for u in units2]
            print(f"  Unit IDs: {unit_ids_1}")
    else:
        print(f"  Error: {r2.text[:200]}")
except Exception as e:
    print(f"  Error: {e}")

print()

# Test 3: page=2 para confirmar
print("Test 3: page=2, size=2")
try:
    r3 = client.get(f"{api_url}/api/pms/units", params={"page": 2, "size": 2})
    print(f"  Status: {r3.status_code}")
    if r3.status_code == 200:
        data = r3.json()
        print(f'  Response page field: {data.get("page")}')
        units3 = data.get("_embedded", {}).get("units", [])
        print(f"  Units returned: {len(units3)}")
        if units3:
            unit_ids_2 = [u.get("id") for u in units3]
            print(f"  Unit IDs: {unit_ids_2}")
except Exception as e:
    print(f"  Error: {e}")

print()
print("=" * 60)
print("✅ CONCLUSIÓN:")
print("=" * 60)

# Análisis de resultados
if "r1" in locals() and r1.status_code == 200:
    if "r2" in locals() and r2.status_code == 200:
        print("✓ Ambos page=0 y page=1 funcionan")
        if "unit_ids_0" in locals() and "unit_ids_1" in locals():
            if unit_ids_0 != unit_ids_1:
                print("✓ Los IDs de unidades son diferentes entre page=0 y page=1")
                print("📊 RESULTADO: API usa paginación 0-BASED")
            else:
                print("✓ Los IDs son iguales, la API probablemente ignora page=0")
                print("📊 RESULTADO: API usa paginación 1-BASED")
    else:
        print("✗ page=1 falló pero page=0 funcionó")
        print("📊 RESULTADO: API usa paginación 0-BASED")
elif "r2" in locals() and r2.status_code == 200:
    print("✗ page=0 falló pero page=1 funcionó")
    print("📊 RESULTADO: API usa paginación 1-BASED")
else:
    print("❌ No se pudieron obtener resultados conclusivos")

client.close()
