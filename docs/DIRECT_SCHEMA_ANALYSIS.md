================================================================================
ANÁLISIS DE ESQUEMAS MCP vs DOCUMENTACIÓN
================================================================================

📊 Total de discrepancias encontradas: 9

🔧 search_units
----------------------------------------
  📋 Parámetro: page
     ⚠️  Problema: Minimum esperado: 1, actual: None

  📋 Parámetro: page
     ⚠️  Problema: Documentación dice minimum=0, maximum=0 (posible error)

  📋 Parámetro: size
     ⚠️  Problema: Minimum esperado: 1, actual: None

  📋 Parámetro: pets_friendly
     ⚠️  Problema: Minimum esperado: 0, actual: None

🔧 search_amenities
----------------------------------------
  📋 Parámetro: page
     ⚠️  Problema: Documentación dice type=number, minimum=0, maximum=0

  📋 Parámetro: size
     ⚠️  Problema: Documentación dice type=number

  📋 Parámetro: sort_column
     ⚠️  Problema: Tipo esperado: string, actual: unknown

🔧 search_reservations
----------------------------------------
  📋 Parámetro: page
     ⚠️  Problema: Minimum esperado: 0, actual: None

  📋 Parámetro: size
     ⚠️  Problema: Minimum esperado: 1, actual: None

💡 RECOMENDACIONES GENERALES
----------------------------------------
1. Ejecutar tests reales contra la API para validar comportamiento
2. Priorizar comportamiento real sobre documentación oficial
3. Documentar discrepancias entre doc y realidad
4. Crear tests de regresión basados en comportamiento real