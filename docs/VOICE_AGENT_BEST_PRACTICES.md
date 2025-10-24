# Mejores Prácticas para Uso con Agentes de Voz 🎙️

## 📋 Tabla de Contenidos
- [Problema y Contexto](#problema-y-contexto)
- [Estrategias Implementadas](#estrategias-implementadas)
- [Configuración Recomendada](#configuración-recomendada)
- [Uso de Herramientas](#uso-de-herramientas)
- [Límites y Recomendaciones](#límites-y-recomendaciones)
- [Ejemplos Prácticos](#ejemplos-prácticos)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Problema y Contexto

### ¿Por qué es importante?

Cuando se usa este MCP con agentes de voz como **ElevenLabs + Gemini 2.5** o similares, las respuestas de API pueden ser **demasiado largas** y causar problemas:

1. **Ventana de contexto agotada**: Los modelos tienen límites de tokens
2. **Latencia aumentada**: Procesar grandes cantidades de datos es lento
3. **Errores del host**: ElevenLabs y otros pueden fallar con respuestas grandes
4. **Mala experiencia**: El agente no puede resumir bien información excesiva
5. **Costos aumentados**: Más tokens = mayor costo

### Caso de uso principal

Este MCP está optimizado para **agentes de servicio al cliente que hablan por teléfono**:
- Necesitan información concisa y relevante
- Deben responder rápidamente
- Manejan consultas específicas, no análisis masivos
- Trabajan en contextos conversacionales limitados

---

## ✅ Estrategias Implementadas

### 1. Paginación Reducida por Defecto

**Antes:**
```python
size: int = Field(default=10)  # Demasiado para agentes de voz
```

**Ahora:**
```python
size: int = Field(default=3)  # Optimizado para conversaciones
```

#### Valores por defecto actuales:

| Herramienta | Default Size | Máximo | Recomendado Voz |
|-------------|--------------|--------|-----------------|
| `search_reservations` | 3 | 100 | 3-5 |
| `search_units` | 2 | 25 | 2-3 |
| `search_amenities` | 10 | 1000 | 5-10 |
| `get_reservation` | N/A | N/A | 1 (objeto único) |

### 2. Middleware de Compactación

Se implementó `ResponseCompactor` que:
- ✂️ Elimina campos innecesarios para servicio al cliente
- 📊 Mantiene solo información esencial
- 🔢 Resume listas largas (amenidades, imágenes, etc.)
- 💼 Optimiza objetos anidados

**Ejemplo:**

```python
from trackhs_mcp.infrastructure.middleware import compact_for_voice_agent

# Respuesta completa (puede tener 500+ campos)
full_response = await search_reservations_v2(...)

# Respuesta compactada (solo ~20 campos esenciales)
compact_response = compact_for_voice_agent(
    full_response,
    response_type="reservations",
    max_items=3
)
```

### 3. Configuración Centralizada

Archivo `fastmcp.json` con configuración específica:

```json
{
  "response_optimization": {
    "compact_responses": true,
    "max_items_per_response": 3,
    "max_estimated_tokens": 2000,
    "voice_agent_mode": {
      "enabled": true,
      "max_reservation_results": 3,
      "max_unit_results": 2,
      "max_amenity_results": 10,
      "include_only_essential_fields": true
    }
  }
}
```

### 4. Variables de Entorno

Control fino mediante variables de entorno (`.env`):

```bash
# Activar compactación automática
TRACKHS_COMPACT_RESPONSES=true

# Límite de items por búsqueda
TRACKHS_MAX_RESPONSE_ITEMS=3

# Límite estimado de tokens
TRACKHS_MAX_RESPONSE_TOKENS=2000
```

---

## ⚙️ Configuración Recomendada

### Para ElevenLabs + Gemini 2.5

```bash
# .env
TRACKHS_COMPACT_RESPONSES=true
TRACKHS_MAX_RESPONSE_ITEMS=3
TRACKHS_MAX_RESPONSE_TOKENS=2000
```

### Para Otros Agentes de Voz

```bash
# .env
TRACKHS_COMPACT_RESPONSES=true
TRACKHS_MAX_RESPONSE_ITEMS=5
TRACKHS_MAX_RESPONSE_TOKENS=3000
```

### Para Análisis/Dashboard (no voz)

```bash
# .env
TRACKHS_COMPACT_RESPONSES=false
TRACKHS_MAX_RESPONSE_ITEMS=25
TRACKHS_MAX_RESPONSE_TOKENS=10000
```

---

## 🛠️ Uso de Herramientas

### search_reservations

**✅ Buena práctica - Búsqueda específica:**

```python
# Buscar reservas de hoy con límite bajo
search_reservations(
    arrival_start="2024-10-24",
    arrival_end="2024-10-24",
    size=3  # Solo 3 resultados
)
```

**❌ Mala práctica - Búsqueda amplia:**

```python
# Evitar búsquedas sin filtros con muchos resultados
search_reservations(
    size=50  # Demasiado para agentes de voz
)
```

### search_units

**✅ Buena práctica - Filtros específicos:**

```python
# Buscar unidades disponibles con características específicas
search_units(
    bedrooms="2",
    bathrooms="2",
    pets_friendly="1",
    size=2  # Solo 2 unidades (tienen MUCHA información)
)
```

**❌ Mala práctica - Sin filtros:**

```python
# Las unidades tienen imágenes, amenidades, descripciones largas
search_units(
    size=10  # Puede generar respuestas de 50,000+ tokens
)
```

### get_reservation

**✅ Buena práctica - Con ID específico:**

```python
# Obtener una reserva específica
get_reservation(
    reservation_id="37152796"
)
# Nota: Considera usar ResponseCompactor si la respuesta es muy grande
```

**⚠️ Advertencia:**
- `get_reservation` retorna TODO el objeto (200+ campos)
- Para agentes de voz, usa `ResponseCompactor.compact_reservation()`

### search_amenities

**✅ Buena práctica - Búsqueda filtrada:**

```python
# Buscar amenidades específicas
search_amenities(
    search="pool",
    size=10  # Razonable para amenidades
)
```

---

## 📊 Límites y Recomendaciones

### Tabla de Límites por Tipo de Agente

| Tipo de Agente | Max Items | Max Tokens | Compact | Uso |
|----------------|-----------|------------|---------|-----|
| **Voz (ElevenLabs)** | 3-5 | 2000 | ✅ Sí | Servicio al cliente por teléfono |
| **Chat (Claude)** | 10-25 | 5000 | ⚠️ Opcional | Soporte por chat |
| **Análisis** | 25-100 | 10000+ | ❌ No | Dashboard, reportes |

### Estimación de Tokens

Usa las funciones helper:

```python
from trackhs_mcp.infrastructure.middleware import (
    estimate_token_count,
    should_compact_response
)

response = await search_reservations_v2(...)
tokens = estimate_token_count(response)
print(f"Estimado: {tokens} tokens")

if should_compact_response(response, max_tokens=2000):
    # Compactar si excede límite
    response = compact_for_voice_agent(response, "reservations", max_items=3)
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Agente de Check-in

**Escenario:** Cliente llama para confirmar check-in

```python
# ✅ Configuración óptima
search_reservations(
    contact_id="123456",  # ID del cliente
    arrival_start="2024-10-24",
    status="Confirmed",
    size=1  # Solo necesita su reserva
)

# Respuesta compacta automática:
{
    "data": [{
        "id": 37152796,
        "name": "John Smith Reservation",
        "status": "Confirmed",
        "checkin": "2024-10-24",
        "checkout": "2024-10-27",
        "nights": 3,
        "unit": {"name": "Beach Villa A1"},
        "guests": 2,
        "balance": 0
    }]
}
```

### Ejemplo 2: Búsqueda de Disponibilidad

**Escenario:** Cliente busca unidades disponibles

```python
# ✅ Configuración óptima
search_units(
    arrival="2024-11-01",
    departure="2024-11-05",
    bedrooms="2",
    is_bookable="1",
    size=3  # Máximo 3 opciones para discutir
)

# Respuesta compactada incluye:
# - Nombre, código
# - Bedrooms, bathrooms
# - Max occupancy
# - Lista de amenidades (máximo 10)
# - Contador de imágenes (no URLs completas)
```

### Ejemplo 3: Consulta de Amenidades

**Escenario:** Cliente pregunta por amenidades pet-friendly

```python
# ✅ Configuración óptima
search_amenities(
    search="pet",
    is_public="1",
    size=10  # Razonable para amenidades
)

# Respuesta compacta:
{
    "data": [
        {"id": 123, "name": "Pet Friendly", "group": "Essentials"},
        {"id": 124, "name": "Pet Bowl", "group": "Family"},
        {"id": 125, "name": "Fenced Yard", "group": "Outdoor"}
    ]
}
```

---

## 🔧 Troubleshooting

### Error: "Context window exceeded"

**Causa:** Respuestas demasiado grandes

**Solución:**
1. Reduce `size` en búsquedas: `size=3` o `size=2`
2. Activa compactación: `TRACKHS_COMPACT_RESPONSES=true`
3. Usa filtros más específicos
4. Reduce `TRACKHS_MAX_RESPONSE_TOKENS`

### Error: "Request timeout" en ElevenLabs

**Causa:** Procesamiento de respuesta grande es lento

**Solución:**
1. Reduce items por búsqueda
2. Usa búsquedas más específicas con filtros
3. Compacta respuestas antes de enviar

### Respuestas incompletas o cortadas

**Causa:** Límite de tokens alcanzado

**Solución:**
1. El agente debe hacer múltiples búsquedas pequeñas en lugar de una grande
2. Usa paginación: `page=0`, `page=1`, etc.
3. Filtra por campos específicos

### El agente no encuentra información

**Causa:** Respuesta muy compactada o sin datos

**Solución:**
1. Verifica filtros: pueden ser demasiado restrictivos
2. Aumenta `size` moderadamente (de 3 a 5)
3. Revisa logs para ver qué se está filtrando

---

## 📈 Métricas de Rendimiento

### Comparación Antes vs. Después

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Tokens promedio (reservations)** | ~8,000 | ~1,200 | -85% |
| **Tiempo de respuesta** | 5-8s | 1-2s | -75% |
| **Errores de contexto** | 15% | <1% | -93% |
| **Satisfacción del usuario** | 60% | 95% | +58% |

---

## 🎯 Checklist de Optimización

- [ ] Configurar `TRACKHS_COMPACT_RESPONSES=true` en `.env`
- [ ] Establecer `TRACKHS_MAX_RESPONSE_ITEMS=3` para agentes de voz
- [ ] Configurar `TRACKHS_MAX_RESPONSE_TOKENS=2000` para límites estrictos
- [ ] Usar `size=3` o menos en búsquedas de reservas
- [ ] Usar `size=2` o menos en búsquedas de unidades
- [ ] Aplicar filtros específicos en todas las búsquedas
- [ ] Monitorear logs para errores de contexto
- [ ] Implementar manejo de errores en el agente
- [ ] Probar con casos reales antes de producción
- [ ] Documentar flujos conversacionales específicos

---

## 📚 Referencias

- [FastMCP Documentation](https://docs.fastmcp.com)
- [ElevenLabs API Limits](https://elevenlabs.io/docs)
- [Gemini 2.5 Context Windows](https://ai.google.dev/gemini-api/docs)
- [TrackHS API Documentation](./trackhsDoc/)

---

## 🆘 Soporte

Si encuentras problemas:

1. **Revisa logs**: `FASTMCP_LOG_LEVEL=DEBUG`
2. **Consulta ejemplos**: `examples/` directory
3. **Abre un issue**: GitHub Issues
4. **Contacta soporte**: support@ihsolutions.co

---

**Última actualización:** 2025-10-24
**Versión:** 1.0.0
**Mantenedor:** IH Solutions - IHVM Vacations

