#!/usr/bin/env python3
"""
Debug del esquema final para amenities
"""

import json
import sys

sys.path.append("src")
from trackhs_mcp.schemas import AmenitiesOutput

# Generar el esquema JSON
schema = AmenitiesOutput.model_json_schema()


# Buscar específicamente el campo tripadvisorType
def find_tripadvisor_type(schema_dict, path=""):
    if isinstance(schema_dict, dict):
        for key, value in schema_dict.items():
            current_path = f"{path}.{key}" if path else key
            if key == "tripadvisorType":
                print(f"Found tripadvisorType at: {current_path}")
                print(f"Value: {json.dumps(value, indent=2)}")
                return True
            elif isinstance(value, (dict, list)):
                if find_tripadvisor_type(value, current_path):
                    return True
    elif isinstance(schema_dict, list):
        for i, item in enumerate(schema_dict):
            if find_tripadvisor_type(item, f"{path}[{i}]"):
                return True
    return False


print("=== BUSCANDO tripadvisorType EN EL ESQUEMA ===")
found = find_tripadvisor_type(schema)

if not found:
    print("tripadvisorType no encontrado en el esquema")

print("\n=== ESQUEMA COMPLETO DE AMENITYITEM ===")
if "properties" in schema and "_embedded" in schema["properties"]:
    embedded_schema = schema["properties"]["_embedded"]
    if "properties" in embedded_schema and "amenities" in embedded_schema["properties"]:
        amenities_schema = embedded_schema["properties"]["amenities"]
        if "items" in amenities_schema and "properties" in amenities_schema["items"]:
            amenity_props = amenities_schema["items"]["properties"]
            print("Campos de AmenityItem:")
            for field_name, field_schema in amenity_props.items():
                print(
                    f"  {field_name}: {field_schema.get('type', 'unknown')} - required: {field_name in amenities_schema['items'].get('required', [])}"
                )
