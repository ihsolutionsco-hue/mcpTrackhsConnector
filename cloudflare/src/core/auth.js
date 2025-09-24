/**
 * Manejo de autenticación Basic Auth para Track HS API
 */
export class TrackHSAuth {
    credentials;
    constructor(config) {
        this.credentials = btoa(`${config.username}:${config.password}`);
    }
    /**
     * Genera el header de autorización para las peticiones
     */
    getAuthHeader() {
        return `Basic ${this.credentials}`;
    }
    /**
     * Valida que las credenciales estén configuradas
     */
    validateCredentials() {
        return this.credentials.length > 0;
    }
}
