/**
 * Clase base para herramientas MCP de Track HS
 */

import { TrackHSApiClient } from './api-client.js';

export interface MCPToolSchema {
  type: 'object';
  properties: Record<string, any>;
  required?: string[];
}

export abstract class BaseTrackHSTool {
  protected apiClient: TrackHSApiClient;

  constructor(apiClient: TrackHSApiClient) {
    this.apiClient = apiClient;
  }

  abstract name: string;
  abstract description: string;
  abstract inputSchema: MCPToolSchema;
  
  abstract execute(params: any): Promise<any>;

  /**
   * Valida los parámetros de entrada según el schema
   */
  protected validateParams(params: any): boolean {
    const schema = this.inputSchema;
    
    // Verificar que params no sea null o undefined
    if (params === null || params === undefined) {
      if (schema.required && schema.required.length > 0) {
        throw new Error(`Parámetro requerido faltante: ${schema.required[0]}`);
      }
      return true;
    }
    
    // Verificar propiedades requeridas
    if (schema.required) {
      for (const requiredProp of schema.required) {
        if (!(requiredProp in params)) {
          throw new Error(`Parámetro requerido faltante: ${requiredProp}`);
        }
      }
    }

    // Validar tipos básicos
    for (const [prop, propSchema] of Object.entries(schema.properties)) {
      if (prop in params) {
        const value = params[prop];
        const expectedType = propSchema.type;
        
        // Solo validar si el valor no es undefined
        if (value !== undefined) {
          if (expectedType === 'string' && typeof value !== 'string') {
            throw new Error(`Parámetro '${prop}' debe ser string`);
          }
          if (expectedType === 'number' && typeof value !== 'number') {
            throw new Error(`Parámetro '${prop}' debe ser number`);
          }
          if (expectedType === 'boolean' && typeof value !== 'boolean') {
            throw new Error(`Parámetro '${prop}' debe ser boolean`);
          }
        }
      }
    }

    return true;
  }
}
