#!/usr/bin/env python3
"""
Script para corregir todos los mocks de work orders
"""

import os
import re


def fix_all_mocks():
    """Corregir todos los mocks de work orders"""

    # Archivos de test a corregir
    test_files = [
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
            # Cambiar mock_api_client.post.return_value = por AsyncMock
            (
                r"mock_api_client\.post\.return_value = sample_work_order_minimal",
                "from unittest.mock import AsyncMock\n        mock_api_client.post = AsyncMock(return_value=sample_work_order_minimal)",
            ),
            (
                r"mock_api_client\.post\.return_value = sample_work_order_response",
                "from unittest.mock import AsyncMock\n        mock_api_client.post = AsyncMock(return_value=sample_work_order_response)",
            ),
            # Cambiar mock_api_client.post.return_value = por AsyncMock para otros casos
            (
                r"mock_api_client\.post\.return_value = ",
                "from unittest.mock import AsyncMock\n        mock_api_client.post = AsyncMock(return_value=",
            ),
        ]

        # Aplicar correcciones
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # Escribir archivo corregido
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Corregido: {file_path}")


if __name__ == "__main__":
    print("Corrigiendo todos los mocks...")
    fix_all_mocks()
    print("Todos los mocks corregidos!")
