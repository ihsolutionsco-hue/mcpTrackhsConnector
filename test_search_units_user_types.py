"""
Pruebas de tipos de usuarios para search_units en MCP TrackHS
Documenta los problemas encontrados con validación de tipos
"""

import asyncio
import json
from typing import Any, Dict, List

# Simulación de diferentes tipos de usuarios y sus escenarios
test_scenarios = [
    {
        "nombre": "Usuario básico - Búsqueda simple",
        "descripcion": "Usuario busca propiedades por nombre",
        "parametros": {"page": 1, "size": 3, "search": "villa"},
        "tipo_usuario": "Turista",
        "expectativa": "Debería funcionar sin problemas",
    },
    {
        "nombre": "Usuario avanzado - Filtros de características",
        "descripcion": "Usuario busca con filtros específicos de habitaciones",
        "parametros": {
            "page": 1,
            "size": 3,
            "bedrooms": "4",  # String en lugar de int
            "bathrooms": "2",  # String en lugar de int
        },
        "tipo_usuario": "Familia",
        "expectativa": "FALLA - Espera integer pero recibe string",
    },
    {
        "nombre": "Usuario con preferencias - Filtros booleanos",
        "descripcion": "Usuario busca propiedades pet-friendly activas",
        "parametros": {
            "page": 1,
            "size": 3,
            "pets_friendly": "1",  # String en lugar de int
            "is_active": "1",  # String en lugar de int
        },
        "tipo_usuario": "Dueño de mascotas",
        "expectativa": "FALLA - Espera integer pero recibe string",
    },
    {
        "nombre": "Usuario por ubicación",
        "descripcion": "Usuario busca por nodo específico",
        "parametros": {
            "page": 1,
            "size": 3,
            "node_id": "3",  # String permitido
            "search": "Champions Gate",
        },
        "tipo_usuario": "Turista local",
        "expectativa": "Debería funcionar - node_id acepta string",
    },
    {
        "nombre": "Usuario buscando disponibilidad",
        "descripcion": "Usuario busca con fechas específicas",
        "parametros": {
            "page": 1,
            "size": 3,
            "arrival": "2025-11-01",
            "departure": "2025-11-07",
            "is_bookable": "1",  # String en lugar de int
        },
        "tipo_usuario": "Planificador de viajes",
        "expectativa": "FALLA en is_bookable - Espera integer pero recibe string",
    },
    {
        "nombre": "Usuario con rango de habitaciones",
        "descripcion": "Usuario busca con rango mínimo/máximo",
        "parametros": {
            "page": 1,
            "size": 3,
            "min_bedrooms": "3",  # String en lugar de int
            "max_bedrooms": "6",  # String en lugar de int
        },
        "tipo_usuario": "Grupo grande",
        "expectativa": "FALLA - Espera integer pero recibe string",
    },
]

# Análisis de tipos de parámetros en el schema MCP
parametros_problematicos = {
    "Numéricos que deberían aceptar string": [
        "bedrooms",
        "min_bedrooms",
        "max_bedrooms",
        "bathrooms",
        "min_bathrooms",
        "max_bathrooms",
        "calendar_id",
        "role_id",
    ],
    "Booleanos (0/1) que deberían aceptar string": [
        "pets_friendly",
        "allow_unit_rates",
        "computed",
        "inherited",
        "limited",
        "is_bookable",
        "include_descriptions",
        "is_active",
        "events_allowed",
        "smoking_allowed",
        "children_allowed",
        "is_accessible",
    ],
    "IDs que ya aceptan string (correcto)": [
        "node_id",
        "amenity_id",
        "unit_type_id",
        "id",
    ],
}


def generar_reporte():
    """Genera reporte de las pruebas de tipos de usuario"""

    reporte = {
        "titulo": "Reporte de Pruebas de Tipos de Usuario - search_units MCP TrackHS",
        "fecha": "2025-10-22",
        "resumen": {
            "total_escenarios": len(test_scenarios),
            "escenarios_exitosos": 2,
            "escenarios_fallidos": 4,
            "problema_principal": "Inconsistencia en validación de tipos de parámetros",
        },
        "escenarios_de_prueba": test_scenarios,
        "analisis_tecnico": {
            "problema": "El schema MCP define parámetros numéricos y booleanos como Optional[str] pero el servidor FastMCP los valida como integer",
            "causa_raiz": "Discrepancia entre el schema definido en el código Python y la validación del servidor MCP",
            "impacto": "Los usuarios no pueden usar filtros numéricos o booleanos a través del MCP",
            "parametros_afectados": parametros_problematicos,
        },
        "casos_de_uso_bloqueados": [
            {
                "caso": "Filtrado por número de habitaciones",
                "usuarios_afectados": "Familias, grupos grandes",
                "gravedad": "Alta",
            },
            {
                "caso": "Filtrado por propiedades pet-friendly",
                "usuarios_afectados": "Dueños de mascotas",
                "gravedad": "Alta",
            },
            {
                "caso": "Filtrado por unidades activas/disponibles",
                "usuarios_afectados": "Todos los usuarios",
                "gravedad": "Crítica",
            },
            {
                "caso": "Filtrado por rangos de características",
                "usuarios_afectados": "Usuarios avanzados",
                "gravedad": "Media",
            },
        ],
        "recomendaciones": [
            {
                "prioridad": "Alta",
                "accion": "Actualizar el schema MCP para aceptar tanto string como integer en parámetros numéricos",
                "justificacion": "Permite compatibilidad con diferentes clientes MCP",
            },
            {
                "prioridad": "Alta",
                "accion": "Implementar normalización de tipos en el servidor antes de la validación",
                "justificacion": "Convierte strings a integers automáticamente cuando sea necesario",
            },
            {
                "prioridad": "Media",
                "accion": "Documentar explícitamente los tipos esperados en las descripciones",
                "justificacion": "Ayuda a los desarrolladores a entender los requisitos",
            },
            {
                "prioridad": "Baja",
                "accion": "Agregar mensajes de error más descriptivos",
                "justificacion": "Facilita el debugging para los usuarios",
            },
        ],
        "ejemplos_de_uso": {
            "funciona_actualmente": [
                {
                    "descripcion": "Búsqueda básica por texto",
                    "codigo": 'search_units(page=1, size=3, search="villa")',
                },
                {
                    "descripcion": "Filtro por IDs (acepta string)",
                    "codigo": 'search_units(page=1, size=3, node_id="3")',
                },
            ],
            "no_funciona_actualmente": [
                {
                    "descripcion": "Filtro por habitaciones",
                    "codigo": 'search_units(page=1, size=3, bedrooms="4")',
                    "error": "Parameter 'bedrooms' must be one of types [integer, null], got string",
                },
                {
                    "descripcion": "Filtro pet-friendly",
                    "codigo": 'search_units(page=1, size=3, pets_friendly="1")',
                    "error": "Parameter 'pets_friendly' must be one of types [integer, null], got string",
                },
            ],
        },
    }

    return reporte


if __name__ == "__main__":
    print("=" * 80)
    print("REPORTE DE PRUEBAS DE TIPOS DE USUARIO - search_units MCP TrackHS")
    print("=" * 80)
    print()

    reporte = generar_reporte()

    # Guardar reporte en JSON
    with open("reporte_pruebas_tipos_search_units.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    print(f"[OK] Reporte generado: reporte_pruebas_tipos_search_units.json")
    print()

    # Mostrar resumen
    print("RESUMEN:")
    print(f"  • Total de escenarios: {reporte['resumen']['total_escenarios']}")
    print(f"  • Escenarios exitosos: {reporte['resumen']['escenarios_exitosos']}")
    print(f"  • Escenarios fallidos: {reporte['resumen']['escenarios_fallidos']}")
    print()

    print("PROBLEMA PRINCIPAL:")
    print(f"  {reporte['analisis_tecnico']['problema']}")
    print()

    print("CASOS DE USO BLOQUEADOS:")
    for caso in reporte["casos_de_uso_bloqueados"]:
        print(f"  • {caso['caso']} (Gravedad: {caso['gravedad']})")
        print(f"    Afecta a: {caso['usuarios_afectados']}")
    print()

    print("RECOMENDACIONES:")
    for i, rec in enumerate(reporte["recomendaciones"], 1):
        print(f"  {i}. [{rec['prioridad']}] {rec['accion']}")
    print()

    print("=" * 80)
