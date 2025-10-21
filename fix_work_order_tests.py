#!/usr/bin/env python3
"""
Script para corregir tests de work orders para usar AsyncMock
"""

import os
import re


def fix_work_order_tests():
    """Corregir tests de work orders para usar AsyncMock"""

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
            # Cambiar Mock por AsyncMock para métodos post
            (r"mock_api_client\.post = Mock\(", "mock_api_client.post = AsyncMock("),
            # Cambiar Mock por AsyncMock para métodos get
            (r"mock_api_client\.get = Mock\(", "mock_api_client.get = AsyncMock("),
            # Agregar import AsyncMock
            (
                r"from unittest.mock import Mock",
                "from unittest.mock import Mock, AsyncMock",
            ),
            # Corregir llamadas duplicadas await
            (r"await await ", "await "),
        ]

        # Aplicar correcciones
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # Escribir archivo corregido
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Corregido: {file_path}")


if __name__ == "__main__":
    print("Corrigiendo tests de work orders...")
    fix_work_order_tests()
    print("Tests de work orders corregidos!")
