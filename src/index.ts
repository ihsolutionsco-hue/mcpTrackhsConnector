#!/usr/bin/env node

/**
 * Punto de entrada para el servidor MCP de Track HS
 */

import { TrackHSMCPServer } from './server.js';

async function main() {
  try {
    const server = new TrackHSMCPServer();
    
    // Manejar señales de terminación
    process.on('SIGINT', async () => {
      console.error('Recibida señal SIGINT, deteniendo servidor...');
      await server.stop();
      process.exit(0);
    });

    process.on('SIGTERM', async () => {
      console.error('Recibida señal SIGTERM, deteniendo servidor...');
      await server.stop();
      process.exit(0);
    });

    // Manejar errores no capturados
    process.on('uncaughtException', (error) => {
      console.error('Error no capturado:', error);
      process.exit(1);
    });

    process.on('unhandledRejection', (reason, promise) => {
      console.error('Promesa rechazada no manejada:', reason);
      process.exit(1);
    });

    await server.start();
  } catch (error) {
    console.error('Error fatal al iniciar Track HS MCP Server:', error);
    process.exit(1);
  }
}

// Ejecutar el servidor
main();
