#!/usr/bin/env python3
"""
Script final para corregir TODOS los tests según la documentación de la API
"""

import os
import re


def fix_all_tests_final():
    """Corrige TODOS los tests según la documentación de la API"""
    print("Corrigiendo TODOS los tests según la documentación de la API...")

    # Archivo 1: tests/unit/use_cases/test_search_units_use_case.py
    fix_unit_tests_final()

    # Archivo 2: tests/e2e/test_search_units_e2e.py
    fix_e2e_tests_final()

    # Archivo 3: tests/integration/test_search_units.py
    fix_integration_tests_final()

    print("\nCorrecciones finales completadas!")


def fix_unit_tests_final():
    """Corrige los tests unitarios de forma definitiva"""
    file_path = "tests/unit/use_cases/test_search_units_use_case.py"
    print(f"Corrigiendo {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Patrones finales para tests unitarios
    patterns = [
        # Test básico - incluir parámetros por defecto
        (
            r"params=\{'page': 0, 'size': 25\}",
            r'params={"page": 0, "size": 25, "sortColumn": "name", "sortDirection": "asc"}',
        ),
        # Test con filtros - incluir parámetros por defecto
        (
            r"params=\{'page': 0, 'size': 10, 'nodeId': 1, 'bedrooms': 2, 'bathrooms': 2, 'petsFriendly': 1, 'isActive': 1\}",
            r'params={"page": 0, "size": 10, "sortColumn": "name", "sortDirection": "asc", "nodeId": 1, "bedrooms": 2, "bathrooms": 2, "petsFriendly": 1, "isActive": 1}',
        ),
        # Test con filtros de fecha - incluir parámetros por defecto
        (
            r"params=\{'page': 1, 'size': 10, 'arrival': '2024-01-01', 'departure': '2024-01-07', 'contentUpdatedSince': '2024-01-01T00:00:00Z'\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "arrival": "2024-01-01", "departure": "2024-01-07", "contentUpdatedSince": "2024-01-01T00:00:00Z"}',
        ),
        # Test con múltiples IDs - incluir parámetros por defecto
        (
            r"params=\{'page': 1, 'size': 10, 'nodeId': \[1, 2, 3\], 'amenityId': \[4, 5, 6\], 'unitTypeId': 7\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "nodeId": [1, 2, 3], "amenityId": [4, 5, 6], "unitTypeId": 7}',
        ),
    ]

    # Aplicar correcciones
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Escribir archivo corregido
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK {file_path} corregido")


def fix_e2e_tests_final():
    """Corrige los tests E2E de forma definitiva"""
    file_path = "tests/e2e/test_search_units_e2e.py"
    print(f"Corrigiendo {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Patrones finales para tests E2E
    patterns = [
        # Test de ordenamiento - incluir parámetros por defecto
        (
            r"params=\{'sortColumn': 'name', 'sortDirection': 'desc', 'size': 25\}",
            r'params={"page": 0, "size": 25, "sortColumn": "name", "sortDirection": "desc"}',
        ),
        # Test de texto - incluir parámetros por defecto
        (
            r"params=\{'search': 'luxury villa ocean view'\}",
            r'params={"page": 0, "size": 25, "sortColumn": "name", "sortDirection": "asc", "search": "luxury villa ocean view"}',
        ),
        # Test de filtros de habitaciones - incluir parámetros por defecto
        (
            r"params=\{'bedrooms': 3, 'minBathrooms': 2, 'maxBathrooms': 3\}",
            r'params={"page": 0, "size": 25, "sortColumn": "name", "sortDirection": "asc", "bedrooms": 3, "minBathrooms": 2, "maxBathrooms": 3}',
        ),
        # Test de filtros de estado - incluir parámetros por defecto
        (
            r"params=\{'isActive': 1, 'isBookable': 1, 'unitStatus': 'clean'\}",
            r'params={"page": 0, "size": 25, "sortColumn": "name", "sortDirection": "asc", "isActive": 1, "isBookable": 1, "unitStatus": "clean"}',
        ),
        # Test de filtros booleanos - incluir parámetros por defecto
        (
            r"params=\{'petsFriendly': 1, 'eventsAllowed': 0, 'smokingAllowed': 0, 'childrenAllowed': 1, 'isAccessible': 1\}",
            r'params={"page": 0, "size": 25, "sortColumn": "name", "sortDirection": "asc", "petsFriendly": 1, "eventsAllowed": 0, "smokingAllowed": 0, "childrenAllowed": 1, "isAccessible": 1}',
        ),
    ]

    # Aplicar correcciones
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Escribir archivo corregido
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK {file_path} corregido")


def fix_integration_tests_final():
    """Corrige los tests de integración de forma definitiva"""
    file_path = "tests/integration/test_search_units.py"
    print(f"Corrigiendo {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Patrones finales para tests de integración
    patterns = [
        # Test de filtros booleanos - incluir parámetros por defecto
        (
            r"params=\{'petsFriendly': 1, 'eventsAllowed': 0, 'smokingAllowed': 0, 'childrenAllowed': 1, 'isAccessible': 1, 'isBookable': 1, 'isActive': 1, 'computed': 1, 'inherited': 0, 'limited': 0, 'includeDescriptions': 1\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "petsFriendly": 1, "eventsAllowed": 0, "smokingAllowed": 0, "childrenAllowed": 1, "isAccessible": 1, "isBookable": 1, "isActive": 1, "computed": 1, "inherited": 0, "limited": 0, "includeDescriptions": 1}',
        ),
        # Test de filtros de fecha - incluir parámetros por defecto
        (
            r"params=\{'arrival': '2024-01-01', 'departure': '2024-01-07', 'contentUpdatedSince': '2024-01-01T00:00:00Z', 'updatedSince': '2024-01-01'\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "arrival": "2024-01-01", "departure": "2024-01-07", "contentUpdatedSince": "2024-01-01T00:00:00Z", "updatedSince": "2024-01-01"}',
        ),
        # Test de filtros de habitaciones - incluir parámetros por defecto
        (
            r"params=\{'bedrooms': 2, 'minBedrooms': 1, 'maxBedrooms': 3, 'bathrooms': 2, 'minBathrooms': 1, 'maxBathrooms': 3\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "bedrooms": 2, "minBedrooms": 1, "maxBedrooms": 3, "bathrooms": 2, "minBathrooms": 1, "maxBathrooms": 3}',
        ),
        # Test de filtros de búsqueda - incluir parámetros por defecto
        (
            r"params=\{'search': 'luxury villa', 'term': 'ocean view', 'unitCode': 'V001', 'shortName': 'VIL'\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "search": "luxury villa", "term": "ocean view", "unitCode": "V001", "shortName": "VIL"}',
        ),
        # Test de filtros de ID - incluir parámetros por defecto
        (
            r"params=\{'nodeId': \[1, 2, 3\], 'amenityId': 4, 'unitTypeId': \[5, 6\], 'id': \[7, 8, 9\], 'calendarId': 10, 'roleId': 11\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "nodeId": [1, 2, 3], "amenityId": 4, "unitTypeId": [5, 6], "id": [7, 8, 9], "calendarId": 10, "roleId": 11}',
        ),
        # Test de filtros de estado - incluir parámetros por defecto
        (
            r"params=\{'isActive': 1, 'isBookable': 1, 'unitStatus': 'clean'\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "asc", "isActive": 1, "isBookable": 1, "unitStatus": "clean"}',
        ),
        # Test de ordenamiento - incluir parámetros por defecto
        (
            r"params=\{'sortColumn': 'name', 'sortDirection': 'desc'\}",
            r'params={"page": 1, "size": 10, "sortColumn": "name", "sortDirection": "desc"}',
        ),
    ]

    # Aplicar correcciones
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Escribir archivo corregido
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK {file_path} corregido")


if __name__ == "__main__":
    fix_all_tests_final()
