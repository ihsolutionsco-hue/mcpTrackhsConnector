# 🎯 MEJORES PRÁCTICAS MCP - FORMATOS Y USO CORRECTO

## 📋 GUÍA PARA MODELOS DE IA

### **📅 FORMATOS DE FECHA**

#### ✅ **FORMATO CORRECTO:**
```
arrival_start: "2024-01-15"
arrival_end: "2024-12-31"
```

#### ❌ **FORMATOS INCORRECTOS:**
```
❌ arrival_start: "2024-01-15T10:00:00Z"  # Timestamps no funcionan
❌ arrival_start: "null"                   # No usar 'null' como string
❌ arrival_start: null                     # No usar null directamente
```

#### 💡 **PARA OMITIR FILTROS DE FECHA:**
```
✅ Simplemente no incluir el parámetro
❌ No usar 'null' o valores vacíos
```

---

### **🔍 FILTROS DE ESTADO**

#### ✅ **ESTADO ÚNICO:**
```
status: "Confirmed"
```

#### ✅ **MÚLTIPLES ESTADOS:**
```
status: "Confirmed,Cancelled"
status: "Hold,Confirmed,Checked Out"
```

#### ❌ **FORMATOS INCORRECTOS:**
```
❌ status: ["Confirmed", "Cancelled"]     # No usar arrays
❌ status: "confirmed"                    # Case sensitive
❌ status: "Confirmed;Cancelled"          # Usar comas, no punto y coma
```

#### 📋 **ESTADOS VÁLIDOS:**
- `"Hold"`
- `"Confirmed"`
- `"Cancelled"`
- `"Checked In"`
- `"Checked Out"`

---

### **📊 PAGINACIÓN**

#### ✅ **FORMATO CORRECTO:**
```
page: 0        # Primera página (0-based)
page: 1        # Segunda página
size: 10       # 10 resultados por página
size: 25       # 25 resultados por página
```

#### 📏 **LÍMITES:**
- `page`: 0-9999 (0-based indexing)
- `size`: 1-100 resultados por página
- **Máximo total**: 10,000 resultados

---

### **🔍 BÚSQUEDA DE TEXTO**

#### ✅ **EJEMPLOS CORRECTOS:**
```
search: "John Smith"           # Nombre de huésped
search: "Villa Paradise"       # Nombre de propiedad
search: "Beach House"          # Descripción
```

#### 📏 **LÍMITE:**
- Máximo 200 caracteres

---

### **🏷️ FILTROS POR ID**

#### ✅ **ID ÚNICO:**
```
unit_id: "10"
contact_id: "123"
```

#### ✅ **MÚLTIPLES IDs:**
```
unit_id: "10,20,30"
contact_id: "123,456,789"
```

#### 📋 **TIPOS DE ID DISPONIBLES:**
- `node_id`: IDs de nodos
- `unit_id`: IDs de unidades
- `contact_id`: IDs de contactos
- `travel_agent_id`: IDs de agentes de viaje
- `campaign_id`: IDs de campañas
- `user_id`: IDs de usuarios
- `unit_type_id`: IDs de tipos de unidad
- `rate_type_id`: IDs de tipos de tarifa
- `reservation_type_id`: IDs de tipos de reserva

---

### **📈 ORDENAMIENTO**

#### ✅ **COLUMNAS DISPONIBLES:**
```
sort_column: "name"           # Nombre de reserva
sort_column: "status"          # Estado de reserva
sort_column: "checkin"         # Fecha de check-in
sort_column: "checkout"       # Fecha de check-out
sort_column: "guest"          # Nombre de huésped
sort_column: "unit"           # Nombre de unidad
sort_column: "nights"         # Número de noches
```

#### ✅ **DIRECCIONES:**
```
sort_direction: "asc"         # Ascendente (A-Z, 0-9)
sort_direction: "desc"        # Descendente (Z-A, 9-0)
```

---

### **🏠 FILTROS ESPECIALES**

#### ✅ **EN CASA HOY:**
```
in_house_today: 1              # Huéspedes actualmente en casa
in_house_today: 0              # No en casa
```

#### ✅ **OTROS FILTROS:**
```
group_id: 123                  # ID de grupo
checkin_office_id: 1           # ID de oficina de check-in
folio_id: "12345"              # ID de folio
```

---

### **📜 SCROLL PARA GRANDES DATASETS**

#### ✅ **INICIAR SCROLL:**
```
scroll: "1"                    # Iniciar nuevo scroll
```

#### ✅ **CONTINUAR SCROLL:**
```
scroll: "scroll_id_123"        # Continuar scroll existente
```

#### ⚠️ **NOTA:**
- El scroll desactiva el ordenamiento
- Usar para datasets > 10,000 resultados

---

## 🎯 EJEMPLOS PRÁCTICOS

### **Ejemplo 1: Búsqueda básica**
```python
{
    "page": 0,
    "size": 10,
    "search": "John Smith"
}
```

### **Ejemplo 2: Filtro por fechas**
```python
{
    "page": 0,
    "size": 25,
    "arrival_start": "2024-01-01",
    "arrival_end": "2024-12-31",
    "status": "Confirmed"
}
```

### **Ejemplo 3: Múltiples filtros**
```python
{
    "page": 0,
    "size": 50,
    "unit_id": "10,20,30",
    "status": "Confirmed,Cancelled",
    "sort_column": "checkin",
    "sort_direction": "desc"
}
```

### **Ejemplo 4: Scroll para grandes datasets**
```python
{
    "scroll": "1",
    "size": 100
}
```

---

## ❌ ERRORES COMUNES A EVITAR

1. **❌ Usar timestamps en fechas**
   ```
   ❌ arrival_start: "2024-01-15T10:00:00Z"
   ✅ arrival_start: "2024-01-15"
   ```

2. **❌ Usar 'null' como string**
   ```
   ❌ arrival_start: "null"
   ✅ Simplemente omitir el parámetro
   ```

3. **❌ Usar arrays para múltiples valores**
   ```
   ❌ status: ["Confirmed", "Cancelled"]
   ✅ status: "Confirmed,Cancelled"
   ```

4. **❌ Usar 1-based indexing para páginas**
   ```
   ❌ page: 1  # Para primera página
   ✅ page: 0  # Para primera página
   ```

5. **❌ Usar case incorrecto en estados**
   ```
   ❌ status: "confirmed"
   ✅ status: "Confirmed"
   ```

---

## 🎯 RESUMEN DE MEJORES PRÁCTICAS

1. **📅 Fechas**: Usar formato ISO 8601 básico (YYYY-MM-DD)
2. **🔍 Estados**: Usar comas para múltiples valores
3. **📊 Paginación**: Usar 0-based indexing para páginas
4. **🏷️ IDs**: Usar comas para múltiples valores
5. **❌ Omisión**: Simplemente no incluir parámetros opcionales
6. **📏 Límites**: Respetar límites de tamaño y caracteres
7. **🎯 Claridad**: Usar ejemplos específicos en documentación

---

## 🚀 BENEFICIOS DE ESTAS PRÁCTICAS

- ✅ **Compatibilidad total** con la API de TrackHS
- ✅ **Mejor experiencia** para modelos de IA
- ✅ **Mensajes de error claros** con emojis y ejemplos
- ✅ **Documentación completa** con casos de uso
- ✅ **Validación robusta** con mensajes informativos
- ✅ **Formato estándar** ISO 8601 para fechas
- ✅ **Flexibilidad** para filtros simples y complejos
