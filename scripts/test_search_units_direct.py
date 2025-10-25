#!/usr/bin/env python3
"""
Script directo para probar search_units con la API real de TrackHS
Usa las credenciales del archivo .env
"""

import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_BASE_URL = os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")


def test_api_connection():
    """Probar conexión básica con la API"""
    print("🔌 Probando conexión con TrackHS API...")
    print(f"   Base URL: {API_BASE_URL}")
    print(f"   Username: {'✅ Configurado' if API_USERNAME else '❌ No configurado'}")
    print(f"   Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas en .env")
        return False

    return True


def search_units_direct(page=1, size=10, **filters):
    """Búsqueda directa de unidades usando httpx"""
    print(f"\n🔍 Buscando unidades (página {page}, tamaño {size})")
    if filters:
        print(f"   Filtros: {filters}")

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=30.0) as client:
            params = {"page": page, "size": size}
            params.update(filters)

            response = client.get(f"{API_BASE_URL}/pms/units", params=params)
            response.raise_for_status()

            data = response.json()
            print(f"✅ Respuesta exitosa: {response.status_code}")
            return data

    except httpx.HTTPStatusError as e:
        print(f"❌ Error HTTP {e.response.status_code}: {e.response.text}")
        return None
    except httpx.RequestError as e:
        print(f"❌ Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None


def test_basic_search():
    """Prueba básica de búsqueda"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 1: Búsqueda básica")
    print("=" * 60)

    result = search_units_direct()
    if result:
        print(f"📊 Total de unidades: {result.get('total_items', 0)}")
        print(f"📄 Página {result.get('page', 0)} de {result.get('page_count', 0)}")

        if result.get("_embedded", {}).get("units"):
            units = result["_embedded"]["units"]
            print(f"🏠 Mostrando {len(units)} unidades:")

            for i, unit in enumerate(units[:3], 1):  # Mostrar primeras 3
                print(f"   {i}. {unit.get('name', 'Sin nombre')}")
                print(f"      📍 {unit.get('address', 'Sin dirección')}")
                print(
                    f"      🛏️  {unit.get('bedrooms', 0)} dormitorios, {unit.get('bathrooms', 0)} baños"
                )
                print(
                    f"      💰 Activa: {unit.get('is_active', False)}, Disponible: {unit.get('is_bookable', False)}"
                )
                if unit.get("amenities"):
                    amenities = unit["amenities"][:3]  # Primeras 3 amenidades
                    print(f"      🏊 Amenidades: {', '.join(amenities)}")
                print()


def test_filtered_search():
    """Prueba de búsqueda con filtros"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 2: Búsqueda con filtros")
    print("=" * 60)

    # Buscar unidades de 2 dormitorios, 1 baño
    result = search_units_direct(bedrooms=2, bathrooms=1, is_active=1, is_bookable=1)
    if result:
        print(f"🏠 Unidades de 2 dormitorios, 1 baño: {result.get('total_items', 0)}")

        if result.get("_embedded", {}).get("units"):
            units = result["_embedded"]["units"]
            for unit in units:
                print(
                    f"   • {unit.get('name', 'Sin nombre')} - {unit.get('address', 'Sin dirección')}"
                )


def test_search_by_text():
    """Prueba de búsqueda por texto"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 3: Búsqueda por texto")
    print("=" * 60)

    # Buscar por texto (puedes cambiar el término de búsqueda)
    search_terms = ["beach", "pool", "penthouse", "villa"]

    for term in search_terms:
        result = search_units_direct(search=term, is_active=1, is_bookable=1)
        if result:
            count = result.get("total_items", 0)
            print(f"🔍 '{term}': {count} unidades encontradas")

            if count > 0 and result.get("_embedded", {}).get("units"):
                unit = result["_embedded"]["units"][0]
                print(f"   Ejemplo: {unit.get('name', 'Sin nombre')}")


def test_pagination():
    """Prueba de paginación"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 4: Paginación")
    print("=" * 60)

    # Primera página
    result1 = search_units_direct(page=1, size=5)
    if result1:
        total_items = result1.get("total_items", 0)
        page_count = result1.get("page_count", 0)
        print(f"📄 Página 1: {total_items} unidades totales, {page_count} páginas")

        if page_count > 1:
            # Segunda página
            result2 = search_units_direct(page=2, size=5)
            if result2:
                print(
                    f"📄 Página 2: {len(result2.get('_embedded', {}).get('units', []))} unidades"
                )


def test_inventory_analysis():
    """Análisis del inventario"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 5: Análisis de inventario")
    print("=" * 60)

    # Obtener todas las unidades (paginación)
    all_units = []
    page = 1
    max_pages = 3  # Limitar para no sobrecargar

    while page <= max_pages:
        result = search_units_direct(page=page, size=25)
        if not result:
            break

        units = result.get("_embedded", {}).get("units", [])
        if not units:
            break

        all_units.extend(units)

        if page >= result.get("page_count", 1):
            break

        page += 1

    if all_units:
        print(f"📊 Inventario analizado: {len(all_units)} unidades")

        # Análisis por dormitorios
        bedroom_dist = {}
        for unit in all_units:
            bedrooms = unit.get("bedrooms", 0)
            bedroom_dist[bedrooms] = bedroom_dist.get(bedrooms, 0) + 1

        print("📊 Distribución por dormitorios:")
        for bedrooms, count in sorted(bedroom_dist.items()):
            print(f"   {bedrooms} dormitorios: {count} unidades")

        # Análisis por estado
        active_count = sum(1 for unit in all_units if unit.get("is_active", False))
        bookable_count = sum(1 for unit in all_units if unit.get("is_bookable", False))

        print(f"📊 Estado de unidades:")
        print(f"   Activas: {active_count}")
        print(f"   Disponibles: {bookable_count}")


def test_error_handling():
    """Prueba de manejo de errores"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 6: Manejo de errores")
    print("=" * 60)

    # Test con parámetros inválidos
    print("🔍 Probando con página inválida (debería fallar)...")
    result = search_units_direct(page=0)  # Inválido
    if result is None:
        print("✅ Error manejado correctamente")

    # Test con parámetros válidos
    print("🔍 Probando con parámetros válidos...")
    result = search_units_direct(page=1, size=5)
    if result:
        print("✅ Sistema funciona correctamente después del error")


def main():
    """Función principal"""
    print("🚀 Prueba directa de search_units con TrackHS API")
    print("=" * 60)

    # Verificar conexión
    if not test_api_connection():
        return 1

    try:
        # Ejecutar pruebas
        test_basic_search()
        test_filtered_search()
        test_search_by_text()
        test_pagination()
        test_inventory_analysis()
        test_error_handling()

        print("\n" + "=" * 60)
        print("✅ Todas las pruebas completadas")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error ejecutando pruebas: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
