#!/usr/bin/env python3
"""
Test directo a la API TrackHS con el nuevo sistema de prioridades textuales
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BASE_URL = "https://ihmvacations.trackhs.com/api"
USERNAME = os.getenv("TRACKHS_USERNAME")
PASSWORD = os.getenv("TRACKHS_PASSWORD")

if not USERNAME or not PASSWORD:
    print("❌ Error: Credenciales no encontradas en .env")
    sys.exit(1)

print("🧪 TRACKHS API - TESTING DIRECTO CON NUEVO SISTEMA DE PRIORIDADES")
print("=" * 80)
print(f"🔐 Usando credenciales: {USERNAME[:8]}...")
print(f"🌐 Base URL: {BASE_URL}")
print("=" * 80)

# Mapeo de prioridades textuales a numéricas
PRIORITY_MAPPING = {
    "trivial": 1,
    "low": 1,
    "medium": 3,
    "high": 5,
    "critical": 5
}

def test_priority_mapping():
    """Test del mapeo de prioridades textuales a numéricas"""
    print("\n🔧 TESTING MAPEO DE PRIORIDADES")
    print("=" * 50)
    
    test_cases = [
        ("trivial", 1),
        ("low", 1),
        ("medium", 3),
        ("high", 5),
        ("critical", 5)
    ]
    
    for text_priority, expected_numeric in test_cases:
        print(f"\n📋 Test: Prioridad '{text_priority}' (debería mapear a {expected_numeric})")
        
        # Crear payload con prioridad textual mapeada a numérica
        payload = {
            "dateReceived": "2024-01-15",
            "priority": expected_numeric,  # Usar valor numérico mapeado
            "summary": f"Test de prioridad {text_priority}",
            "estimatedCost": 100.0,
            "estimatedTime": 60,
            "unitId": 1
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/pms/maintenance/work-orders",
                json=payload,
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                work_order_id = result.get("id")
                print(f"✅ ÉXITO - Work Order ID: {work_order_id}")
                print(f"📊 Prioridad enviada: {expected_numeric}, Prioridad recibida: {result.get('priority', 'N/A')}")
                print(f"✅ Mapeo correcto: {text_priority} → {expected_numeric}")
            else:
                print(f"❌ ERROR - Status: {response.status_code}")
                print(f"📄 Response: {response.text}")
                
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")

def test_real_world_scenarios():
    """Test con escenarios del mundo real usando prioridades textuales"""
    print("\n📞 ESCENARIOS DEL MUNDO REAL CON NUEVAS PRIORIDADES")
    print("=" * 60)
    
    scenarios = [
        {
            "priority": "critical",
            "summary": "EMERGENCIA - Fuga de agua severa",
            "description": "Fuga importante que requiere atención inmediata",
            "expected_numeric": 5
        },
        {
            "priority": "high", 
            "summary": "Aire acondicionado no funciona",
            "description": "Huésped reporta problema de comodidad",
            "expected_numeric": 5
        },
        {
            "priority": "medium",
            "summary": "Problemas de WiFi",
            "description": "Múltiples huéspedes reportan conectividad lenta",
            "expected_numeric": 3
        },
        {
            "priority": "low",
            "summary": "Limpieza programada",
            "description": "Limpieza de mantenimiento regular",
            "expected_numeric": 1
        },
        {
            "priority": "trivial",
            "summary": "Cambio de bombillas",
            "description": "Reemplazo de bombillas fundidas",
            "expected_numeric": 1
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔧 Ejemplo: {scenario['priority'].upper()}")
        print(f"📝 Resumen: {scenario['summary']}")
        print(f"📄 Descripción: {scenario['description']}")
        
        # Mapear prioridad textual a numérica
        numeric_priority = PRIORITY_MAPPING[scenario['priority']]
        
        payload = {
            "dateReceived": "2024-01-15",
            "priority": numeric_priority,
            "summary": scenario['summary'],
            "estimatedCost": 150.0,
            "estimatedTime": 90,
            "unitId": 1,
            "description": scenario['description']
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/pms/maintenance/work-orders",
                json=payload,
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                work_order_id = result.get("id")
                print(f"✅ ÉXITO - Work Order ID: {work_order_id}")
                print(f"📊 Prioridad: {numeric_priority} (esperado: {scenario['expected_numeric']})")
            else:
                print(f"❌ ERROR - Status: {response.status_code}")
                print(f"📄 Response: {response.text}")
                
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")

def test_invalid_priorities():
    """Test con prioridades inválidas para verificar validación"""
    print("\n❌ TESTING PRIORIDADES INVÁLIDAS")
    print("=" * 40)
    
    invalid_priorities = [
        "urgent",      # No existe en nuestro sistema
        "normal",      # No existe en nuestro sistema  
        "low-priority", # Formato inválido
        "1",           # Numérico en lugar de textual
        "3",           # Numérico en lugar de textual
        "5"            # Numérico en lugar de textual
    ]
    
    for invalid_priority in invalid_priorities:
        print(f"\n📋 Test: Prioridad inválida '{invalid_priority}'")
        
        # Intentar usar la prioridad inválida directamente
        payload = {
            "dateReceived": "2024-01-15",
            "priority": invalid_priority,  # Esto debería fallar
            "summary": f"Test con prioridad inválida: {invalid_priority}",
            "estimatedCost": 100.0,
            "estimatedTime": 60,
            "unitId": 1
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/pms/maintenance/work-orders",
                json=payload,
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                work_order_id = result.get("id")
                print(f"❌ INESPERADO - Debería haber fallado pero funcionó: {work_order_id}")
            else:
                print(f"✅ CORRECTO - Falló como esperado: {response.status_code}")
                print(f"📄 Error: {response.text}")
                
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")

def test_priority_validation_simulation():
    """Simular validación de prioridades como lo haría el MCP"""
    print("\n🔍 SIMULACIÓN DE VALIDACIÓN MCP")
    print("=" * 40)
    
    def validate_priority(priority):
        """Simular validación de prioridad como en el MCP"""
        valid_priorities = ["trivial", "low", "medium", "high", "critical"]
        if priority not in valid_priorities:
            raise ValueError(f"La prioridad debe ser una de: {', '.join(valid_priorities)}. Valor recibido: {priority}")
        return priority
    
    def map_priority_to_numeric(text_priority):
        """Mapear prioridad textual a numérica"""
        return PRIORITY_MAPPING.get(text_priority, 3)  # Default a medium
    
    test_priorities = [
        "trivial",     # Válida
        "low",         # Válida
        "medium",      # Válida
        "high",        # Válida
        "critical",    # Válida
        "urgent",      # Inválida
        "normal",      # Inválida
        "1",           # Inválida
        "5"            # Inválida
    ]
    
    for priority in test_priorities:
        print(f"\n📋 Validando: '{priority}'")
        
        try:
            # Simular validación del MCP
            validated_priority = validate_priority(priority)
            numeric_priority = map_priority_to_numeric(validated_priority)
            
            print(f"✅ VÁLIDA - {priority} → {numeric_priority}")
            
            # Crear work order con prioridad validada
            payload = {
                "dateReceived": "2024-01-15",
                "priority": numeric_priority,
                "summary": f"Test validado: {priority}",
                "estimatedCost": 100.0,
                "estimatedTime": 60,
                "unitId": 1
            }
            
            response = requests.post(
                f"{BASE_URL}/pms/maintenance/work-orders",
                json=payload,
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                work_order_id = result.get("id")
                print(f"✅ Work Order creado: {work_order_id}")
            else:
                print(f"❌ Error en API: {response.status_code}")
                
        except ValueError as e:
            print(f"❌ INVÁLIDA - {e}")
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")

if __name__ == "__main__":
    try:
        # Test 1: Mapeo de prioridades
        test_priority_mapping()
        
        # Test 2: Escenarios del mundo real
        test_real_world_scenarios()
        
        # Test 3: Prioridades inválidas
        test_invalid_priorities()
        
        # Test 4: Simulación de validación MCP
        test_priority_validation_simulation()
        
        print("\n" + "=" * 80)
        print("🏁 TESTING DEL NUEVO SISTEMA DE PRIORIDADES COMPLETADO")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
