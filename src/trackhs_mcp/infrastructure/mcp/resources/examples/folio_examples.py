"""
Examples resources para Folio Operations
Ejemplos de operaciones con folios
"""

from typing import TYPE_CHECKING, Any, Dict

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
        return """# TrackHS Folio Operations Examples

## Operaciones Básicas

### 1. Obtener Folio por ID
```python
# Obtener folio específico
folio = get_folio(folio_id=12345)

# Respuesta esperada
{
    "id": 12345,
    "type": "guest",
    "status": "open",
    "currentBalance": 1500.00,
    "realizedBalance": 1200.00,
    "contactId": 67890,
    "reservationId": 11111
}
```

### 2. Verificar Estado del Folio
```python
# Verificar si el folio está abierto
folio = get_folio(folio_id=12345)
if folio["status"] == "open":
    print("Folio activo")
elif folio["status"] == "closed":
    print("Folio cerrado")
```

### 3. Obtener Información Financiera
```python
# Obtener datos financieros
folio = get_folio(folio_id=12345)
financial_info = {
    "current_balance": folio["currentBalance"],
    "realized_balance": folio["realizedBalance"],
    "agent_commission": folio.get("agentCommission", 0),
    "owner_commission": folio.get("ownerCommission", 0),
    "owner_revenue": folio.get("ownerRevenue", 0)
}
```

## Casos de Uso Comunes

### Verificación de Balance
```python
def check_folio_balance(folio_id):
    folio = get_folio(folio_id)

    if folio["currentBalance"] > 0:
        return f"Folio {folio_id} tiene balance pendiente: ${folio['currentBalance']}"
    else:
        return f"Folio {folio_id} está balanceado"
```

### Análisis de Comisiones
```python
def analyze_commissions(folio_id):
    folio = get_folio(folio_id)

    analysis = {
        "folio_id": folio_id,
        "agent_commission": folio.get("agentCommission", 0),
        "owner_commission": folio.get("ownerCommission", 0),
        "total_commissions": (folio.get("agentCommission", 0) +
                            folio.get("ownerCommission", 0))
    }

    return analysis
```

### Verificación de Excepciones
```python
def check_folio_exceptions(folio_id):
    folio = get_folio(folio_id)

    if folio.get("hasException", False):
        return {
            "folio_id": folio_id,
            "has_exception": True,
            "exception_message": folio.get("exceptionMessage", "Sin mensaje")
        }
    else:
        return {
            "folio_id": folio_id,
            "has_exception": False
        }
```

### Obtener Información del Contacto
```python
def get_contact_from_folio(folio_id):
    folio = get_folio(folio_id)

    if "contact" in folio.get("embedded", {}):
        contact = folio["embedded"]["contact"]
        return {
            "contact_id": contact["id"],
            "name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}",
            "email": contact.get("primaryEmail", ""),
            "phone": contact.get("cellPhone", "")
        }
    return None
```

## Manejo de Errores

### Verificación de Folio Existente
```python
def safe_get_folio(folio_id):
    try:
        folio = get_folio(folio_id)
        return folio
    except Exception as e:
        if "404" in str(e):
            return {"error": "Folio no encontrado"}
        elif "401" in str(e):
            return {"error": "No autorizado"}
        else:
            return {"error": f"Error inesperado: {e}"}
```

### Validación de Datos
```python
def validate_folio_data(folio):
    required_fields = ["id", "type", "status"]
    missing_fields = [field for field in required_fields if field not in folio]

    if missing_fields:
        return {"valid": False, "missing_fields": missing_fields}

    if folio["type"] not in ["guest", "master"]:
        return {"valid": False, "error": "Tipo de folio inválido"}

    if folio["status"] not in ["open", "closed"]:
        return {"valid": False, "error": "Estado de folio inválido"}

    return {"valid": True}
```
"""
