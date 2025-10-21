#!/usr/bin/env python3
"""
Script para corregir tests de work orders para usar async/await
"""

import os
import re


def fix_work_order_tests():
    """Corregir tests de work orders para usar async/await"""

    # Archivos de test a corregir
    test_files = [
        "tests/unit/use_cases/test_create_work_order.py",
        "tests/unit/mcp/test_create_work_order_tool.py",
        "tests/e2e/test_create_work_order_e2e.py",
    ]

    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            continue

        print(f"Corrigiendo {file_path}...")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Patrones a corregir
        patterns = [
            # Métodos de test
            (r"def test_([^(]+)\(", r"async def test_\1("),
            # Llamadas a execute
            (r"result = use_case\.execute\(", r"result = await use_case.execute("),
            (r"use_case\.execute\(", r"await use_case.execute("),
            # Llamadas a create_maintenance_work_order
            (
                r"create_maintenance_work_order\(",
                r"await create_maintenance_work_order(",
            ),
        ]

        # Aplicar correcciones
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # Escribir archivo corregido
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Corregido: {file_path}")


def fix_search_units_tests():
    """Corregir tests de search_units para usar paginación 1-based"""

    test_files = [
        "tests/e2e/test_search_units_e2e.py",
        "tests/e2e/test_search_units_e2e_refactored.py",
    ]

    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            continue

        print(f"Corrigiendo {file_path}...")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Corregir expectativas de paginación de 0-based a 1-based
        patterns = [
            # Cambiar page=0 a page=1 en expectativas
            (r"'page': 0", "'page': 1"),
            (r'"page": 0', '"page": 1'),
            # Cambiar page=1 a page=2 cuando se espera página 2
            (r"'page': 1, 'size': 100", "'page': 2, 'size': 100"),
        ]

        # Aplicar correcciones
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # Escribir archivo corregido
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Corregido: {file_path}")


if __name__ == "__main__":
    print("Corrigiendo tests...")
    fix_work_order_tests()
    fix_search_units_tests()
    print("Todos los tests corregidos!")
