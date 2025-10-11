# Ejemplos de MCP

Esta sección contiene ejemplos prácticos de implementaciones MCP organizados por nivel de complejidad y caso de uso.

## Índice de Ejemplos

### 🚀 Quickstart
**Ubicación**: [quickstart/](./quickstart/)

Ejemplos rápidos para comenzar con MCP:

- **mcp-client-python**: Cliente MCP básico en Python
- **mcp-client-typescript**: Cliente MCP básico en TypeScript
- **weather-server-python**: Servidor de clima en Python
- **weather-server-rust**: Servidor de clima en Rust
- **weather-server-typescript**: Servidor de clima en TypeScript

**¿Cuándo usar?** Para aprender los conceptos básicos de MCP y crear tu primer servidor o cliente.

### 🏗️ Servidor Remoto Completo
**Ubicación**: [servidor-remoto-completo/](./servidor-remoto-completo/)

Implementación completa de un servidor MCP remoto con autenticación OAuth 2.0:

- **auth-server**: Servidor de autorización OAuth 2.0
- **mcp-server**: Servidor MCP con autenticación
- **docs**: Documentación detallada del flujo OAuth
- **examples**: Ejemplos de cliente y curl

**¿Cuándo usar?** Para implementar servidores MCP remotos en producción con autenticación completa.

## Flujo de Aprendizaje Recomendado

### 1. Comienza con Quickstart
1. **Lee los fundamentos**: [01-fundamentos/](../01-fundamentos/)
2. **Ejecuta un ejemplo básico**: [quickstart/weather-server-python](./quickstart/weather-server-python/)
3. **Crea tu primer cliente**: [quickstart/mcp-client-python](./quickstart/mcp-client-python/)

### 2. Avanza a Servidores Remotos
1. **Entiende la autenticación**: [02-servidores-remotos/oauth-autenticacion.md](../02-servidores-remotos/oauth-autenticacion.md)
2. **Estudia el ejemplo completo**: [servidor-remoto-completo/](./servidor-remoto-completo/)
3. **Implementa tu propio servidor**: Sigue las [mejores prácticas](../02-servidores-remotos/mejores-practicas.md)

## Guías de Desarrollo

Para implementar tus propios ejemplos, consulta:

- **Crear servidor Python**: [03-guias-desarrollo/crear-servidor-python.md](../03-guias-desarrollo/crear-servidor-python.md)
- **Crear cliente**: [03-guias-desarrollo/crear-cliente.md](../03-guias-desarrollo/crear-cliente.md)
- **Conectar servidores locales**: [03-guias-desarrollo/conectar-servidores-locales.md](../03-guias-desarrollo/conectar-servidores-locales.md)
- **Conectar servidores remotos**: [03-guias-desarrollo/conectar-servidores-remotos.md](../03-guias-desarrollo/conectar-servidores-remotos.md)

## Herramientas de Desarrollo

- **MCP Inspector**: [06-herramientas/guia-inspector.md](../06-herramientas/guia-inspector.md)
- **Debugging**: Usa el Inspector para probar tus servidores

## Recursos Adicionales

- **Especificación MCP**: [05-referencias/especificacion/](../05-referencias/especificacion/)
- **SDK Python**: [07-repositorios-originales/python-sdk/](../07-repositorios-originales/python-sdk/)
- **Repositorio oficial**: [07-repositorios-originales/modelcontextprotocol/](../07-repositorios-originales/modelcontextprotocol/)
