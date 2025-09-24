#!/usr/bin/env node

/**
 * Servidor local para desarrollo y pruebas del Track HS MCP Server
 */

import { TrackHSMCPServer } from './server.js';
import { createServer } from 'http';
import { readFileSync } from 'fs';
import { join } from 'path';

async function main() {
  try {
    // Cargar variables de entorno desde .env
    let envContent = readFileSync('.env', 'utf-8');
    
    // Remover BOM si existe
    if (envContent.charCodeAt(0) === 0xFEFF) {
      envContent = envContent.slice(1);
    }
    
    const env: { TRACKHS_API_URL: string; TRACKHS_USERNAME: string; TRACKHS_PASSWORD: string; ENVIRONMENT?: string } = {
      TRACKHS_API_URL: '',
      TRACKHS_USERNAME: '',
      TRACKHS_PASSWORD: '',
      ENVIRONMENT: 'development'
    };
    
    envContent.split('\n').forEach((line, index) => {
      const trimmedLine = line.trim();
      console.log(`Procesando línea ${index + 1}: "${trimmedLine}"`);
      
      // Ignorar comentarios y líneas vacías
      if (trimmedLine.startsWith('#') || trimmedLine === '') {
        console.log(`  -> Ignorada (comentario o vacía)`);
        return;
      }
      
      const equalIndex = trimmedLine.indexOf('=');
      if (equalIndex === -1) {
        console.log(`  -> Ignorada (sin =)`);
        return;
      }
      
      const key = trimmedLine.substring(0, equalIndex).trim();
      const value = trimmedLine.substring(equalIndex + 1).trim();
      
      console.log(`  -> Key: "${key}", Value: "${value}"`);
      
      if (key === 'TRACKHS_API_URL') {
        env.TRACKHS_API_URL = value;
        console.log(`  -> Asignado TRACKHS_API_URL: "${env.TRACKHS_API_URL}"`);
      }
      if (key === 'TRACKHS_USERNAME') {
        env.TRACKHS_USERNAME = value;
        console.log(`  -> Asignado TRACKHS_USERNAME: "${env.TRACKHS_USERNAME}"`);
      }
      if (key === 'TRACKHS_PASSWORD') {
        env.TRACKHS_PASSWORD = value;
        console.log(`  -> Asignado TRACKHS_PASSWORD: "${env.TRACKHS_PASSWORD}"`);
      }
      if (key === 'ENVIRONMENT') {
        env.ENVIRONMENT = value;
        console.log(`  -> Asignado ENVIRONMENT: "${env.ENVIRONMENT}"`);
      }
    });
    
    console.log('🔍 Variables finales:');
    console.log('TRACKHS_API_URL:', `"${env.TRACKHS_API_URL}"`);
    console.log('TRACKHS_USERNAME:', `"${env.TRACKHS_USERNAME}"`);
    console.log('TRACKHS_PASSWORD:', `"${env.TRACKHS_PASSWORD}"`);

    // Validar que las variables estén configuradas
    if (!env.TRACKHS_API_URL || !env.TRACKHS_USERNAME || !env.TRACKHS_PASSWORD) {
      console.error('❌ Error: Variables de entorno no configuradas en .env');
      console.error('Asegúrate de que .env contenga:');
      console.error('TRACKHS_API_URL=tu_url');
      console.error('TRACKHS_USERNAME=tu_usuario');
      console.error('TRACKHS_PASSWORD=tu_contraseña');
      process.exit(1);
    }

    const server = new TrackHSMCPServer(env);
    
    // Crear servidor HTTP local
    const httpServer = createServer(async (req, res) => {
      try {
        // Convertir request de Node.js a Request de Web API
        const url = `http://localhost:3000${req.url}`;
        // Leer el body si existe
        let requestBody: string | undefined;
        if (req.method !== 'GET' && req.method !== 'HEAD') {
          const chunks: Buffer[] = [];
          req.on('data', (chunk) => chunks.push(chunk));
          await new Promise(resolve => req.on('end', resolve));
          requestBody = Buffer.concat(chunks).toString();
        }

        const request = new Request(url, {
          method: req.method || 'GET',
          headers: req.headers as any,
          body: requestBody || null
        });

        const response = await server.handleRequest(request);
        
        // Convertir Response de Web API a response de Node.js
        res.statusCode = response.status;
        response.headers.forEach((value, key) => {
          res.setHeader(key, value);
        });
        
        const responseBody = await response.text();
        res.end(responseBody);
      } catch (error) {
        console.error('Error en servidor:', error);
        res.statusCode = 500;
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ error: 'Error interno del servidor' }));
      }
    });

    const PORT = process.env.PORT || 3000;
    
    httpServer.listen(PORT, () => {
      console.log('🚀 Track HS MCP Server iniciado localmente');
      console.log(`📡 Servidor corriendo en: http://localhost:${PORT}`);
      console.log(`🔍 Health check: http://localhost:${PORT}/health`);
      console.log(`🛠️  Endpoint MCP: http://localhost:${PORT}/mcp`);
      console.log('📋 Herramientas disponibles:', server.getToolsInfo().map(t => t.name).join(', '));
      console.log('\n💡 Para usar con Claude Desktop:');
      console.log(`   URL del conector: http://localhost:${PORT}`);
    });

    // Manejar señales de terminación
    process.on('SIGINT', () => {
      console.log('\n🛑 Deteniendo servidor...');
      httpServer.close(() => {
        console.log('✅ Servidor detenido correctamente');
        process.exit(0);
      });
    });

    process.on('SIGTERM', () => {
      console.log('\n🛑 Deteniendo servidor...');
      httpServer.close(() => {
        console.log('✅ Servidor detenido correctamente');
        process.exit(0);
      });
    });

  } catch (error) {
    console.error('❌ Error fatal al iniciar Track HS MCP Server:', error);
    process.exit(1);
  }
}

// Ejecutar el servidor
main();
