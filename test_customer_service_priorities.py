#!/usr/bin/env python3
"""
Test de casos de servicio al cliente con el nuevo sistema de prioridades
Simula llamadas reales de huéspedes y asigna prioridades apropiadas
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

print("📞 TRACKHS API - CASOS DE SERVICIO AL CLIENTE CON NUEVAS PRIORIDADES")
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

def simulate_customer_call(call_number, customer_issue, priority, expected_numeric):
    """Simular una llamada de servicio al cliente"""
    print(f"\n📞 Llamada #{call_number}")
    print(f"🔧 Problema: {customer_issue}")
    print(f"⚡ Prioridad asignada: {priority.upper()} (nivel {expected_numeric})")
    
    # Crear payload con la prioridad mapeada
    payload = {
        "dateReceived": datetime.now().strftime("%Y-%m-%d"),
        "priority": expected_numeric,
        "summary": customer_issue,
        "estimatedCost": 100.0,
        "estimatedTime": 60,
        "unitId": 1,
        "description": f"Llamada de servicio al cliente - {customer_issue}",
        "source": "Guest Request",
        "sourceName": "Huésped"
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
            print(f"✅ Work Order creado: {work_order_id}")
            print(f"📊 Prioridad aplicada: {expected_numeric}")
            return work_order_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None

def test_emergency_scenarios():
    """Test de escenarios de emergencia - CRITICAL priority"""
    print("\n🚨 ESCENARIOS DE EMERGENCIA (CRITICAL)")
    print("=" * 50)
    
    emergency_calls = [
        "Fuga de agua en el baño principal - agua corriendo por el piso",
        "Cortocircuito en el panel eléctrico - olor a quemado",
        "Puerta de entrada bloqueada - huéspedes no pueden salir",
        "Fuga de gas detectada - olor fuerte en la cocina",
        "Vidrio roto en ventana - riesgo de cortes"
    ]
    
    for i, issue in enumerate(emergency_calls, 1):
        simulate_customer_call(
            call_number=i,
            customer_issue=issue,
            priority="critical",
            expected_numeric=5
        )

def test_high_priority_scenarios():
    """Test de escenarios de alta prioridad - HIGH priority"""
    print("\n🔥 ESCENARIOS DE ALTA PRIORIDAD (HIGH)")
    print("=" * 50)
    
    high_priority_calls = [
        "Aire acondicionado no funciona - habitación muy caliente",
        "Calentador de agua roto - sin agua caliente",
        "WiFi completamente caído - huéspedes no pueden trabajar",
        "Cerradura de habitación no funciona - huésped bloqueado",
        "Refrigerador no enfría - comida se está echando a perder"
    ]
    
    for i, issue in enumerate(high_priority_calls, 1):
        simulate_customer_call(
            call_number=i,
            customer_issue=issue,
            priority="high",
            expected_numeric=5
        )

def test_medium_priority_scenarios():
    """Test de escenarios de prioridad media - MEDIUM priority"""
    print("\n⚡ ESCENARIOS DE PRIORIDAD MEDIA (MEDIUM)")
    print("=" * 50)
    
    medium_priority_calls = [
        "WiFi lento - velocidad reducida pero funcional",
        "Luz del baño parpadeando - funciona pero molesta",
        "Cerradura de ventana floja - cierra pero no segura",
        "Grifo goteando - desperdicio de agua",
        "Persiana rota - no se puede cerrar completamente"
    ]
    
    for i, issue in enumerate(medium_priority_calls, 1):
        simulate_customer_call(
            call_number=i,
            customer_issue=issue,
            priority="medium",
            expected_numeric=3
        )

def test_low_priority_scenarios():
    """Test de escenarios de baja prioridad - LOW priority"""
    print("\n🔧 ESCENARIOS DE BAJA PRIORIDAD (LOW)")
    print("=" * 50)
    
    low_priority_calls = [
        "Limpieza profunda programada - mantenimiento regular",
        "Pintura descascarada en pared - cosmético",
        "Cortina desalineada - ajuste menor",
        "Estante flojo en cocina - no urgente",
        "Limpieza de filtros de aire - mantenimiento preventivo"
    ]
    
    for i, issue in enumerate(low_priority_calls, 1):
        simulate_customer_call(
            call_number=i,
            customer_issue=issue,
            priority="low",
            expected_numeric=1
        )

def test_trivial_scenarios():
    """Test de escenarios triviales - TRIVIAL priority"""
    print("\n🔨 ESCENARIOS TRIVIALES (TRIVIAL)")
    print("=" * 50)
    
    trivial_calls = [
        "Cambio de bombilla fundida - reemplazo simple",
        "Ajuste de perilla de ducha - calibración menor",
        "Limpieza de manchas en pared - cosmético",
        "Ajuste de bisagra de puerta - lubricación",
        "Reemplazo de filtro de aire - mantenimiento rutinario"
    ]
    
    for i, issue in enumerate(trivial_calls, 1):
        simulate_customer_call(
            call_number=i,
            customer_issue=issue,
            priority="trivial",
            expected_numeric=1
        )

def test_priority_decision_logic():
    """Test de lógica de decisión de prioridades"""
    print("\n🧠 TESTING LÓGICA DE DECISIÓN DE PRIORIDADES")
    print("=" * 60)
    
    def determine_priority(issue_description):
        """Determinar prioridad basada en la descripción del problema"""
        issue_lower = issue_description.lower()
        
        # Palabras clave para CRITICAL
        critical_keywords = ["fuga", "agua", "gas", "fuego", "cortocircuito", "bloqueado", "emergencia", "riesgo", "peligro"]
        if any(keyword in issue_lower for keyword in critical_keywords):
            return "critical", 5
        
        # Palabras clave para HIGH
        high_keywords = ["no funciona", "roto", "caído", "caliente", "frío", "bloqueado", "trabajo", "comodidad"]
        if any(keyword in issue_lower for keyword in high_keywords):
            return "high", 5
        
        # Palabras clave para MEDIUM
        medium_keywords = ["lento", "parpadeando", "flojo", "goteando", "molesta", "reducida"]
        if any(keyword in issue_lower for keyword in medium_keywords):
            return "medium", 3
        
        # Palabras clave para LOW
        low_keywords = ["programada", "cosmético", "mantenimiento", "preventivo", "regular"]
        if any(keyword in issue_lower for keyword in low_keywords):
            return "low", 1
        
        # Por defecto, TRIVIAL
        return "trivial", 1
    
    test_issues = [
        "Fuga de agua en el baño - emergencia",
        "Aire acondicionado no funciona - muy caliente",
        "WiFi lento pero funcional",
        "Limpieza programada para mañana",
        "Cambio de bombilla en el pasillo"
    ]
    
    for issue in test_issues:
        priority, numeric = determine_priority(issue)
        print(f"\n📋 Problema: {issue}")
        print(f"🧠 Prioridad determinada: {priority.upper()} (nivel {numeric})")
        
        # Crear work order con la prioridad determinada automáticamente
        simulate_customer_call(
            call_number="AUTO",
            customer_issue=issue,
            priority=priority,
            expected_numeric=numeric
        )

if __name__ == "__main__":
    try:
        # Test 1: Escenarios de emergencia
        test_emergency_scenarios()
        
        # Test 2: Escenarios de alta prioridad
        test_high_priority_scenarios()
        
        # Test 3: Escenarios de prioridad media
        test_medium_priority_scenarios()
        
        # Test 4: Escenarios de baja prioridad
        test_low_priority_scenarios()
        
        # Test 5: Escenarios triviales
        test_trivial_scenarios()
        
        # Test 6: Lógica de decisión automática
        test_priority_decision_logic()
        
        print("\n" + "=" * 80)
        print("🏁 TESTING DE CASOS DE SERVICIO AL CLIENTE COMPLETADO")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
