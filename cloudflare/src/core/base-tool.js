/**
 * Clase base para herramientas MCP de Track HS
 */
export class BaseTrackHSTool {
    apiClient;
    constructor(apiClient) {
        this.apiClient = apiClient;
    }
    /**
     * Valida los parámetros de entrada según el schema
     */
    validateParams(params) {
        const schema = this.inputSchema;
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
        return true;
    }
}
