#!/usr/bin/env python3
"""
Script para corregir los tests E2E e Integration que fallan
por no incluir los parámetros por defecto de la API.
"""

import os
import re


def fix_test_file(file_path):
    """Corrige un archivo de test para incluir parámetros por defecto"""
    print(f"Corrigiendo {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Patrones para corregir
    patterns = [
        # Patrón 1: params={"page": X, "size": Y}
        (
            r'params=\{"page": (\d+), "size": (\d+)\}',
            r'params={"page": \1, "size": \2, "sortColumn": "name", "sortDirection": "asc"}',
        ),
        # Patrón 2: params={"page": X, "size": Y, ...}
        (
            r'params=\{"page": (\d+), "size": (\d+),',
            r'params={"page": \1, "size": \2, "sortColumn": "name", "sortDirection": "asc",',
        ),
        # Patrón 3: params={'page': X, 'size': Y}
        (
            r"params=\{'page': (\d+), 'size': (\d+)\}",
            r'params={"page": \1, "size": \2, "sortColumn": "name", "sortDirection": "asc"}',
        ),
        # Patrón 4: params={'page': X, 'size': Y, ...}
        (
            r"params=\{'page': (\d+), 'size': (\d+),",
            r'params={"page": \1, "size": \2, "sortColumn": "name", "sortDirection": "asc",',
        ),
    ]

    # Aplicar correcciones
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Escribir archivo corregido
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK {file_path} corregido")


def main():
    """Funcion principal"""
    print("Corrigiendo tests para incluir parametros por defecto de la API...")

    # Archivos a corregir
    test_files = [
        "tests/e2e/test_search_units_e2e.py",
        "tests/integration/test_search_units.py",
        "tests/e2e/test_tools_integration.py",
    ]

    for file_path in test_files:
        if os.path.exists(file_path):
            fix_test_file(file_path)
        else:
            print(f"Archivo no encontrado: {file_path}")

    print("\nCorrecciones completadas!")
    print("Los tests ahora incluyen los parametros por defecto:")
    print("- sortColumn: 'name'")
    print("- sortDirection: 'asc'")


if __name__ == "__main__":
    main()
