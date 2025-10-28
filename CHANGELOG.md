# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-27

### 🚀 Agregado
- **Arquitectura de servicios**: Implementación completa de patrón de servicios con separación de responsabilidades
- **Repositorios**: Capa de acceso a datos con abstracción de la API de TrackHS
- **Middleware nativo**: Sistema completo de middleware para autenticación, logging, métricas y reintentos
- **Validación Pydantic**: Validación robusta de datos de entrada y salida con esquemas personalizados
- **Configuración centralizada**: Sistema de configuración usando Pydantic Settings
- **Manejo de errores avanzado**: Sistema de excepciones personalizadas con manejo granular
- **Logging estructurado**: Sistema de logging con sanitización de datos sensibles
- **Health check endpoint**: Endpoint de monitoreo con métricas dinámicas
- **Métricas Prometheus**: Exportación de métricas en formato Prometheus
- **Transformación automática de datos**: Limpieza y normalización automática de datos problemáticos
- **Cache de autenticación**: Sistema de cache para mejorar rendimiento
- **Rate limiting**: Control de velocidad de requests
- **Sanitización de logs**: Protección de datos sensibles en logs

### 🔧 Mejorado
- **Búsqueda de unidades**: Implementación completa de la API de TrackHS con todos los parámetros disponibles
- **Búsqueda de reservas**: Filtros avanzados con validación de fechas y filtrado del lado del cliente
- **Gestión de work orders**: Creación de órdenes de mantenimiento y housekeeping con validación robusta
- **Manejo de tipos de datos**: Conversión automática de strings a tipos numéricos y booleanos
- **Validación de fechas**: Validación y conversión de formatos de fecha
- **Limpieza de datos**: Normalización de campos problemáticos como `area`, `bedrooms`, `bathrooms`
- **Manejo de errores**: Mensajes de error más descriptivos y útiles para debugging
- **Documentación**: README completamente actualizado con información real del código

### 🐛 Corregido
- **Bug de filtros de fecha**: Implementación de filtrado del lado del cliente para compensar bug de API TrackHS
- **Conversión de tipos**: Corrección de problemas de conversión de strings a números
- **Validación de esquemas**: Mejora en la validación de respuestas de API
- **Manejo de valores nulos**: Mejor manejo de valores `null`, `undefined`, `N/A` en datos
- **Paginación**: Corrección de conversión entre páginas 0-based y 1-based
- **Campos de área**: Normalización robusta del campo `area` que causaba errores de esquema

### 🔄 Cambiado
- **Estructura del proyecto**: Reorganización completa en servicios, repositorios y middleware
- **Configuración**: Migración a Pydantic Settings para configuración centralizada
- **Validación**: Implementación de validación flexible con modo estricto y no estricto
- **Logging**: Migración a logging estructurado con niveles configurables
- **Manejo de excepciones**: Implementación de jerarquía de excepciones personalizadas
- **Documentación**: Eliminación de documentación obsoleta y actualización completa

### 🗑️ Eliminado
- **Documentación obsoleta**: Eliminación de archivos de documentación desactualizados
- **Código duplicado**: Eliminación de funciones duplicadas y código redundante
- **Configuración hardcodeada**: Eliminación de valores hardcodeados en favor de configuración centralizada
- **Logging básico**: Reemplazo de logging básico por sistema estructurado

### 🔒 Seguridad
- **Sanitización de logs**: Implementación de sanitización automática de datos sensibles
- **Validación de entrada**: Validación robusta de todos los parámetros de entrada
- **Manejo de credenciales**: Mejor manejo de credenciales con validación de configuración
- **Rate limiting**: Implementación de control de velocidad para prevenir abuso

### 📊 Rendimiento
- **Cache de autenticación**: Implementación de cache para reducir llamadas a API
- **Reintentos inteligentes**: Sistema de reintentos con backoff exponencial
- **Transformación de datos**: Optimización de limpieza y normalización de datos
- **Paginación eficiente**: Mejora en el manejo de paginación para grandes conjuntos de datos

### 🧪 Testing
- **Cobertura de tests**: Aumento significativo en la cobertura de tests
- **Tests de integración**: Implementación de tests de integración con API real
- **Tests de validación**: Tests específicos para validación de datos
- **Tests de middleware**: Tests para todos los middleware implementados

### 📚 Documentación
- **README actualizado**: Documentación completa basada en el código real
- **Ejemplos de uso**: Ejemplos prácticos para todas las herramientas MCP
- **Guía de configuración**: Documentación detallada de configuración
- **Troubleshooting**: Guía de solución de problemas comunes

## [1.0.0] - 2024-01-01

### 🚀 Agregado
- **Implementación inicial**: Primera versión del conector MCP para TrackHS
- **Herramientas básicas**: Implementación de herramientas MCP básicas
- **Autenticación**: Sistema de autenticación básico
- **Configuración**: Sistema de configuración inicial
- **Tests básicos**: Implementación de tests unitarios básicos

---

## Tipos de Cambios

- **🚀 Agregado**: Para nuevas funcionalidades
- **🔧 Mejorado**: Para cambios en funcionalidades existentes
- **🐛 Corregido**: Para correcciones de bugs
- **🔄 Cambiado**: Para cambios que no son nuevas funcionalidades ni correcciones de bugs
- **🗑️ Eliminado**: Para funcionalidades eliminadas
- **🔒 Seguridad**: Para mejoras de seguridad
- **📊 Rendimiento**: Para mejoras de rendimiento
- **🧪 Testing**: Para cambios relacionados con testing
- **📚 Documentación**: Para cambios en documentación
