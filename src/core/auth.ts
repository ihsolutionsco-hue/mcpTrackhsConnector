/**
 * Manejo de autenticación Basic Auth para Track HS API
 */

import { TrackHSConfig } from './types.js';

export class TrackHSAuth {
  private credentials: string;

  constructor(config: TrackHSConfig) {
    this.credentials = Buffer.from(`${config.username}:${config.password}`).toString('base64');
  }

  /**
   * Genera el header de autorización para las peticiones
   */
  getAuthHeader(): string {
    return `Basic ${this.credentials}`;
  }

  /**
   * Valida que las credenciales estén configuradas
   */
  validateCredentials(): boolean {
    return this.credentials.length > 0;
  }
}
