/**
 * Cliente HTTP base para Track HS API
 */

import { TrackHSConfig, RequestOptions, ApiError } from './types.js';
import { TrackHSAuth } from './auth.js';

export class TrackHSApiClient {
  private baseUrl: string;
  private auth: TrackHSAuth;

  constructor(config: TrackHSConfig) {
    this.baseUrl = config.baseUrl;
    this.auth = new TrackHSAuth(config);
    
    if (!this.auth.validateCredentials()) {
      throw new Error('Credenciales de Track HS no configuradas correctamente');
    }
  }

  /**
   * Realiza una petición HTTP a la API de Track HS
   */
  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const fetchOptions: RequestInit = {
        method: options.method || 'GET',
        headers: {
          'Authorization': this.auth.getAuthHeader(),
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers
        }
      };
      
      if (options.body) {
        fetchOptions.body = options.body;
      }
      
      const response = await fetch(url, fetchOptions);

      if (!response.ok) {
        const errorMessage = `Track HS API Error: ${response.status} ${response.statusText}`;
        throw new Error(errorMessage);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        return await response.text() as unknown as T;
      }
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Error en petición a Track HS: ${error.message}`);
      }
      throw new Error('Error desconocido en petición a Track HS');
    }
  }

  /**
   * Realiza una petición GET
   */
  async get<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  /**
   * Realiza una petición POST
   */
  async post<T>(endpoint: string, data?: any, options: RequestOptions = {}): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    });
  }
}