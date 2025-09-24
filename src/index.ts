#!/usr/bin/env node

/**
 * Punto de entrada para el servidor MCP de Track HS
 */

import { TrackHSMCPServer } from './server.js';

async function main() {
  try {
    // Obtener variables de entorno
    const env = {
      TRACKHS_API_URL: process.env.TRACKHS_API_URL || '',
      TRACKHS_USERNAME: process.env.TRACKHS_USERNAME || '',
      TRACKHS_PASSWORD: process.env.TRACKHS_PASSWORD || '',
      ENVIRONMENT: process.env.ENVIRONMENT || 'development'
    };

    const server = new TrackHSMCPServer(env);
    
    // Manejar señales de terminación
    process.on('SIGINT', async () => {
      console.error('Recibida señal SIGINT, deteniendo servidor...');
      process.exit(0);
    });

    process.on('SIGTERM', async () => {
      console.error('Recibida señal SIGTERM, deteniendo servidor...');
      process.exit(0);
    });

    // Manejar errores no capturados
    process.on('uncaughtException', (error: Error) => {
      console.error('Error no capturado:', error);
      process.exit(1);
    });

    process.on('unhandledRejection', (reason: any, promise: Promise<any>) => {
      console.error('Promesa rechazada no manejada:', reason);
      process.exit(1);
    });

    console.log('🚀 Track HS MCP Server iniciado correctamente');
    console.log('📋 Herramientas disponibles:', server.getToolsInfo().map(t => t.name).join(', '));
  } catch (error) {
    console.error('Error fatal al iniciar Track HS MCP Server:', error);
    process.exit(1);
  }
}

// Ejecutar el servidor
main();
