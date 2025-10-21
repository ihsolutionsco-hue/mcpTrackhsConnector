#!/usr/bin/env python3
"""
Script para corregir tests E2E para usar await en tool_function
"""

import os
import re


def fix_e2e_tests():
    """Corregir tests E2E para usar await en tool_function"""

    # Archivos de test a corregir
    test_files = ["tests/e2e/test_create_work_order_e2e.py"]

    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            continue

        print(f"Corrigiendo {file_path}...")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Patrones a corregir
        patterns = [
            # Cambiar tool_function( por await tool_function(
            (r"result = tool_function\(", "result = await tool_function("),
            # Cambiar tool_function( por await tool_function( en otras líneas
            (r"tool_function\(", "await tool_function("),
        ]

        # Aplicar correcciones
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # Escribir archivo corregido
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Corregido: {file_path}")


if __name__ == "__main__":
    print("Corrigiendo tests E2E...")
    fix_e2e_tests()
    print("Tests E2E corregidos!")
