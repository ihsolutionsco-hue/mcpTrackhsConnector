"""
Examples resources para Folio Operations
Ejemplos de operaciones con folios
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_folio_examples(mcp, api_client: "ApiClientPort"):
    """Registra los ejemplos de operaciones con folios"""

    @mcp.resource(
        "trackhs://examples/folio-operations",
        name="Folio Operations Examples",
        description="Common folio operation examples",
        mime_type="text/plain",
    )
    async def folio_examples() -> str:
        """Ejemplos de operaciones con folios"""
        return '''# TrackHS Folio Operations Examples

## ¿Qué es un Folio?

Un **folio** es un registro financiero que contiene todas las transacciones y balances relacionados con una reserva o huésped. Es como una "cuenta" que rastrea:

- **Cargos**: Servicios, impuestos, comisiones
- **Pagos**: Dinero recibido del huésped
- **Comisiones**: Pagos a agentes y propietarios
- **Balance**: Dinero pendiente o a favor

## Para Principiantes - Primeros Pasos

### 1. Obtener Folio Básico
```python
# Obtener folio por ID
folio = get_folio(folio_id="12345")
```
**¿Qué hace?** Obtiene toda la información financiera de un folio específico.
**¿Cuándo usarlo?** Para revisar el estado financiero de una reserva.

### 2. Verificar Balance
```python
# Verificar si hay dinero pendiente
folio = get_folio(folio_id="12345")
if folio["currentBalance"] > 0:
    print(f"Balance pendiente: ${folio['currentBalance']}")
else:
    print("Folio balanceado")
```
**¿Qué hace?** Verifica si el folio tiene dinero pendiente de pago.
**¿Cuándo usarlo?** Para verificar si una reserva está completamente pagada.

### 3. Obtener Información del Huésped
```python
# Obtener datos del contacto desde el folio
folio = get_folio(folio_id="12345")
contact = folio.get("embedded", {}).get("contact", {})
print(f"Huésped: {contact.get('firstName')} {contact.get('lastName')}")
```
**¿Qué hace?** Extrae información del huésped desde el folio.
**¿Cuándo usarlo?** Para obtener datos de contacto del huésped.

## Operaciones Básicas

### 4. Obtener Folio Completo
```python
# Obtener folio con toda la información
folio = get_folio(folio_id="12345")

# Respuesta esperada completa
{
    "id": 12345,
    "type": "guest",
    "status": "open",
    "currentBalance": 1500.00,
    "realizedBalance": 1200.00,
    "agentCommission": 150.00,
    "ownerCommission": 300.00,
    "ownerRevenue": 750.00,
    "contactId": 67890,
    "reservationId": 11111,
    "hasException": false,
    "exceptionMessage": null,
    "embedded": {
        "contact": {
            "id": 67890,
            "firstName": "Juan",
            "lastName": "Pérez",
            "primaryEmail": "juan@email.com",
            "cellPhone": "+1234567890"
        },
        "company": null,
        "travelAgent": null
    }
}
```

### 5. Verificar Estado del Folio
```python
# Verificar si el folio está abierto o cerrado
folio = get_folio(folio_id="12345")

if folio["status"] == "open":
    print("✅ Folio activo - se pueden hacer cambios")
elif folio["status"] == "closed":
    print("🔒 Folio cerrado - no se pueden hacer cambios")
```

### 6. Análisis Financiero Completo
```python
# Obtener análisis financiero detallado
folio = get_folio(folio_id="12345")

financial_analysis = {
    "folio_id": folio["id"],
    "current_balance": folio["currentBalance"],
    "realized_balance": folio["realizedBalance"],
    "agent_commission": folio.get("agentCommission", 0),
    "owner_commission": folio.get("ownerCommission", 0),
    "owner_revenue": folio.get("ownerRevenue", 0),
    "total_commissions": (folio.get("agentCommission", 0) +
                         folio.get("ownerCommission", 0)),
    "net_revenue": folio.get("ownerRevenue", 0) - folio.get("ownerCommission", 0)
}

print(f"Balance actual: ${financial_analysis['current_balance']}")
print(f"Comisión agente: ${financial_analysis['agent_commission']}")
print(f"Comisión propietario: ${financial_analysis['owner_commission']}")
```

## Casos de Uso Comunes

### Verificación de Balance Pendiente
```python
def check_pending_balance(folio_id):
    """Verifica si hay balance pendiente en el folio"""
    folio = get_folio(folio_id)

    if folio["currentBalance"] > 0:
        return {
            "folio_id": folio_id,
            "has_pending_balance": True,
            "amount": folio["currentBalance"],
            "message": f"Folio {folio_id} tiene ${folio['currentBalance']} pendiente"
        }
    else:
        return {
            "folio_id": folio_id,
            "has_pending_balance": False,
            "message": f"Folio {folio_id} está completamente balanceado"
        }
```

### Análisis de Comisiones
```python
def analyze_commissions(folio_id):
    """Analiza las comisiones del folio"""
    folio = get_folio(folio_id)

    analysis = {
        "folio_id": folio_id,
        "agent_commission": folio.get("agentCommission", 0),
        "owner_commission": folio.get("ownerCommission", 0),
        "total_commissions": (folio.get("agentCommission", 0) +
                             folio.get("ownerCommission", 0)),
        "owner_revenue": folio.get("ownerRevenue", 0),
        "commission_percentage": 0
    }

    if analysis["owner_revenue"] > 0:
        analysis["commission_percentage"] = (
            analysis["total_commissions"] / analysis["owner_revenue"] * 100
        )

    return analysis
```

### Verificación de Excepciones
```python
def check_folio_exceptions(folio_id):
    """Verifica si el folio tiene excepciones"""
    folio = get_folio(folio_id)

    if folio.get("hasException", False):
        return {
            "folio_id": folio_id,
            "has_exception": True,
            "exception_message": folio.get("exceptionMessage", "Sin mensaje específico"),
            "status": "⚠️ Folio con excepciones - revisar manualmente"
        }
    else:
        return {
            "folio_id": folio_id,
            "has_exception": False,
            "status": "✅ Folio sin excepciones"
        }
```

### Obtener Información del Contacto
```python
def get_contact_info(folio_id):
    """Obtiene información del contacto desde el folio"""
    folio = get_folio(folio_id)

    if "embedded" in folio and "contact" in folio["embedded"]:
        contact = folio["embedded"]["contact"]
        return {
            "contact_id": contact["id"],
            "full_name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
            "email": contact.get("primaryEmail", ""),
            "phone": contact.get("cellPhone", ""),
            "has_company": "company" in folio["embedded"] and folio["embedded"]["company"] is not None,
            "has_travel_agent": "travelAgent" in folio["embedded"] and folio["embedded"]["travelAgent"] is not None
        }
    return None
```

### Análisis de Rentabilidad
```python
def analyze_profitability(folio_id):
    """Analiza la rentabilidad del folio"""
    folio = get_folio(folio_id)

    owner_revenue = folio.get("ownerRevenue", 0)
    owner_commission = folio.get("ownerCommission", 0)
    agent_commission = folio.get("agentCommission", 0)

    net_profit = owner_revenue - owner_commission - agent_commission

    return {
        "folio_id": folio_id,
        "gross_revenue": owner_revenue,
        "total_commissions": owner_commission + agent_commission,
        "net_profit": net_profit,
        "profit_margin": (net_profit / owner_revenue * 100) if owner_revenue > 0 else 0,
        "is_profitable": net_profit > 0
    }
```

## Manejo de Errores

### Verificación Segura de Folio
```python
def safe_get_folio(folio_id):
    """Obtiene folio con manejo de errores"""
    try:
        folio = get_folio(folio_id)
        return {
            "success": True,
            "folio": folio,
            "error": None
        }
    except Exception as e:
        error_message = str(e)
        if "404" in error_message:
            return {
                "success": False,
                "folio": None,
                "error": "Folio no encontrado",
                "message": f"El folio {folio_id} no existe"
            }
        elif "401" in error_message:
            return {
                "success": False,
                "folio": None,
                "error": "No autorizado",
                "message": "No tienes permisos para acceder a este folio"
            }
        else:
            return {
                "success": False,
                "folio": None,
                "error": "Error inesperado",
                "message": f"Error: {error_message}"
            }
```

### Validación de Datos del Folio
```python
def validate_folio_data(folio):
    """Valida que el folio tenga la estructura correcta"""
    required_fields = ["id", "type", "status", "currentBalance", "realizedBalance"]
    missing_fields = [field for field in required_fields if field not in folio]

    if missing_fields:
        return {
            "valid": False,
            "error": "Campos faltantes",
            "missing_fields": missing_fields
        }

    # Validar tipo de folio
    if folio["type"] not in ["guest", "master"]:
        return {
            "valid": False,
            "error": "Tipo de folio inválido",
            "message": f"Tipo '{folio['type']}' no es válido. Debe ser 'guest' o 'master'"
        }

    # Validar estado del folio
    if folio["status"] not in ["open", "closed"]:
        return {
            "valid": False,
            "error": "Estado de folio inválido",
            "message": f"Estado '{folio['status']}' no es válido. Debe ser 'open' o 'closed'"
        }

    # Validar balances numéricos
    try:
        float(folio["currentBalance"])
        float(folio["realizedBalance"])
    except (ValueError, TypeError):
        return {
            "valid": False,
            "error": "Balance inválido",
            "message": "Los balances deben ser números válidos"
        }

    return {
        "valid": True,
        "error": None,
        "message": "Folio válido"
    }
```

## Tipos de Folio

- **`"guest"`** - Folio de huésped individual
- **`"master"`** - Folio maestro (grupo de huéspedes)

## Estados de Folio

- **`"open"`** - Folio activo, se pueden hacer cambios
- **`"closed"`** - Folio cerrado, no se pueden hacer cambios

## Campos Financieros Importantes

- **`currentBalance`** - Balance actual (dinero pendiente)
- **`realizedBalance`** - Balance realizado (dinero procesado)
- **`agentCommission`** - Comisión del agente
- **`ownerCommission`** - Comisión del propietario
- **`ownerRevenue`** - Ingresos del propietario'''
