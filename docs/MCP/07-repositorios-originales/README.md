# Repositorios Originales MCP

Esta sección contiene los repositorios originales de MCP sin modificaciones, preservando su estructura y contenido original.

## Repositorios Incluidos

### 📚 modelcontextprotocol
**Ubicación**: [modelcontextprotocol/](./modelcontextprotocol/)

Repositorio oficial del protocolo MCP:
- **Especificación**: Documentación oficial del protocolo
- **Schemas**: Definiciones JSON Schema y TypeScript
- **Documentación**: Sitio web oficial (Mintlify)
- **Blog**: Artículos y actualizaciones

**Enlaces**:
- [GitHub oficial](https://github.com/modelcontextprotocol/modelcontextprotocol)
- [Sitio web](https://modelcontextprotocol.io)
- [Especificación](https://spec.modelcontextprotocol.io)

### 🛠️ servers
**Ubicación**: [servers/](./servers/)

Colección oficial de servidores MCP de referencia:
- **70k+ estrellas**: Repositorio muy popular con ejemplos de alta calidad
- **812 contribuidores**: Mantenido por una gran comunidad
- **Servidores TypeScript**: Implementaciones con `npx`
- **Servidores Python**: Implementaciones con `uvx` y `pip`
- **Recursos de la comunidad**: Enlaces a herramientas y plataformas

**Enlaces**:
- [GitHub oficial](https://github.com/modelcontextprotocol/servers)
- [70k+ estrellas](https://github.com/modelcontextprotocol/servers/stargazers)
- [812 contribuidores](https://github.com/modelcontextprotocol/servers/graphs/contributors)

### 🐍 python-sdk
**Ubicación**: [python-sdk/](./python-sdk/)

SDK oficial de Python para MCP:
- **FastMCP**: Framework de alto nivel para servidores
- **Cliente MCP**: Implementación completa del cliente
- **Ejemplos**: Servidores y clientes de ejemplo
- **Tests**: Suite completa de pruebas

**Enlaces**:
- [GitHub oficial](https://github.com/modelcontextprotocol/python-sdk)
- [Documentación](https://modelcontextprotocol.github.io/python-sdk/)
- [PyPI](https://pypi.org/project/mcp/)

### 🔍 inspector
**Ubicación**: [inspector/](./inspector/)

Herramienta de desarrollo para MCP:
- **CLI**: Interfaz de línea de comandos
- **Web UI**: Interfaz web para debugging
- **Testing**: Herramientas de testing automatizado

**Enlaces**:
- [GitHub oficial](https://github.com/modelcontextprotocol/inspector)
- [NPM](https://www.npmjs.com/package/@modelcontextprotocol/inspector)

### 🌐 example-remote-server
**Ubicación**: [example-remote-server/](./example-remote-server/)

Ejemplo completo de servidor MCP remoto:
- **Auth Server**: Servidor de autorización OAuth 2.0
- **MCP Server**: Servidor MCP con autenticación
- **Documentación**: Guías detalladas de implementación
- **Ejemplos**: Clientes y scripts de prueba

**Enlaces**:
- [GitHub oficial](https://github.com/modelcontextprotocol/example-remote-server)

## Uso de los Repositorios

### Actualización
Para mantener los repositorios actualizados:

```bash
# Actualizar repositorio principal
cd 07-repositorios-originales/modelcontextprotocol
git pull origin main

# Actualizar Python SDK
cd ../python-sdk
git pull origin main

# Actualizar Inspector
cd ../inspector
git pull origin main

# Actualizar ejemplo remoto
cd ../example-remote-server
git pull origin main
```

### Desarrollo
Para contribuir a los repositorios originales:

1. **Fork** el repositorio en GitHub
2. **Clone** tu fork localmente
3. **Desarrolla** en una rama separada
4. **Envía** un Pull Request

### Referencias
Para documentación curada y ejemplos organizados, consulta:

- **Fundamentos**: [01-fundamentos/](../01-fundamentos/)
- **Servidores Remotos**: [02-servidores-remotos/](../02-servidores-remotos/)
- **Guías de Desarrollo**: [03-guias-desarrollo/](../03-guias-desarrollo/)
- **Ejemplos**: [04-ejemplos/](../04-ejemplos/)
- **Referencias**: [05-referencias/](../05-referencias/)
- **Herramientas**: [06-herramientas/](../06-herramientas/)

## Estructura de Repositorios

### modelcontextprotocol/
```
modelcontextprotocol/
├── docs/                    # Documentación del sitio web
├── schema/                  # Schemas por versión
├── blog/                    # Artículos del blog
└── README.md               # Información del proyecto
```

### servers/
```
servers/
├── src/                     # Servidores MCP implementados
│   ├── filesystem/         # Servidor de sistema de archivos
│   ├── git/                # Servidor de Git
│   ├── memory/             # Servidor de memoria
│   ├── time/               # Servidor de tiempo
│   └── ...                 # Otros servidores
├── scripts/                # Scripts de construcción
└── README.md               # Información del proyecto
```

### python-sdk/
```
python-sdk/
├── src/mcp/                # Código fuente del SDK
├── examples/               # Ejemplos de uso
├── tests/                  # Tests del SDK
├── docs/                   # Documentación API
└── README.md               # Información del proyecto
```

### inspector/
```
inspector/
├── cli/                    # Interfaz de línea de comandos
├── client/                 # Interfaz web
├── server/                 # Servidor de desarrollo
└── README.md               # Información del proyecto
```

### example-remote-server/
```
example-remote-server/
├── auth-server/            # Servidor de autorización
├── mcp-server/             # Servidor MCP
├── docs/                   # Documentación
├── examples/               # Ejemplos de cliente
└── README.md               # Información del proyecto
```

## Licencias

Todos los repositorios están bajo la **MIT License**:

- **modelcontextprotocol**: [LICENSE](./modelcontextprotocol/LICENSE)
- **python-sdk**: [LICENSE](./python-sdk/LICENSE)
- **inspector**: [LICENSE](./inspector/LICENSE)
- **example-remote-server**: [LICENSE](./example-remote-server/LICENSE)

## Contribución

Para contribuir a los proyectos oficiales:

1. **Revisa** las guías de contribución de cada repositorio
2. **Sigue** las convenciones de código establecidas
3. **Envía** issues y pull requests en GitHub
4. **Participa** en las discusiones de la comunidad

## Enlaces de la Comunidad

- **GitHub**: [@modelcontextprotocol](https://github.com/modelcontextprotocol)
- **Discord**: [Servidor oficial MCP](https://discord.gg/modelcontextprotocol)
- **Twitter**: [@ModelContextProtocol](https://twitter.com/ModelContextProtocol)
- **Sitio web**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
