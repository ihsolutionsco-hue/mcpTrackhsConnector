/**
 * Cliente HTTP base para Track HS API
 */
import { TrackHSAuth } from './auth.js';
export class TrackHSApiClient {
    baseUrl;
    auth;
    constructor(config) {
        this.baseUrl = config.baseUrl;
        this.auth = new TrackHSAuth(config);
        if (!this.auth.validateCredentials()) {
            throw new Error('Credenciales de Track HS no configuradas correctamente');
        }
    }
    /**
     * Realiza una petición HTTP a la API de Track HS
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        try {
            const fetchOptions = {
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
            }
            else {
                return await response.text();
            }
        }
        catch (error) {
            if (error instanceof Error) {
                throw new Error(`Error en petición a Track HS: ${error.message}`);
            }
            throw new Error('Error desconocido en petición a Track HS');
        }
    }
    /**
     * Realiza una petición GET
     */
    async get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }
    /**
     * Realiza una petición POST
     */
    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            body: data ? JSON.stringify(data) : undefined
        });
    }
}
