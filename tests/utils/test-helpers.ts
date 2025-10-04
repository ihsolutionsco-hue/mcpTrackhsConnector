/**
 * Utilidades para testing
 */

import nock from 'nock';

/**
 * Configura un mock HTTP para la API de Track HS
 */
export function setupApiMock() {
  const baseUrl = process.env.TRACKHS_API_URL!;
  const scope = nock(baseUrl);

  return scope;
}

/**
 * Limpia todos los mocks HTTP
 */
export function cleanupApiMock() {
  nock.cleanAll();
}

/**
 * Simula autenticación exitosa
 */
export function mockSuccessfulAuth(scope: nock.Scope) {
  return scope
    .post('/auth/login')
    .reply(200, {
      token: 'mock-jwt-token',
      expires_in: 3600
    });
}

/**
 * Simula autenticación fallida
 */
export function mockFailedAuth(scope: nock.Scope) {
  return scope
    .post('/auth/login')
    .reply(401, {
      error: 'Unauthorized',
      message: 'Invalid credentials'
    });
}

/**
 * Simula error de servidor
 */
export function mockServerError(scope: nock.Scope, endpoint: string) {
  return scope
    .get(endpoint)
    .reply(500, {
      error: 'Internal Server Error',
      message: 'Something went wrong'
    });
}

/**
 * Simula timeout de red
 */
export function mockNetworkTimeout(scope: nock.Scope, endpoint: string) {
  return scope
    .get(endpoint)
    .replyWithError({ code: 'ETIMEDOUT' });
}

/**
 * Valida que un objeto tenga las propiedades requeridas
 */
export function validateRequiredProperties(obj: any, requiredProps: string[]): boolean {
  return requiredProps.every(prop => obj.hasOwnProperty(prop));
}

/**
 * Valida que una respuesta de API tenga la estructura correcta
 */
export function validateApiResponse(response: any): boolean {
  return response && 
         typeof response === 'object' && 
         (response.data !== undefined || response.error !== undefined);
}

/**
 * Crea un mock de cliente API
 */
export function createMockApiClient() {
  return {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
    authenticate: jest.fn()
  };
}

/**
 * Simula delay para testing de timeouts
 */
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Valida parámetros de entrada
 */
export function validateInputParams(params: any, requiredParams: string[]): boolean {
  if (!params || typeof params !== 'object') {
    return false;
  }
  
  return requiredParams.every(param => 
    params.hasOwnProperty(param) && 
    params[param] !== undefined && 
    params[param] !== null
  );
}

/**
 * Genera datos de prueba aleatorios
 */
export function generateTestData(type: 'reservation' | 'unit' | 'contact' | 'review') {
  const baseData = {
    reservation: {
      guest_name: `Test Guest ${Math.random().toString(36).substr(2, 9)}`,
      check_in: '2024-02-01',
      check_out: '2024-02-05',
      status: 'confirmed'
    },
    unit: {
      name: `Test Unit ${Math.random().toString(36).substr(2, 9)}`,
      type: 'room',
      capacity: Math.floor(Math.random() * 4) + 1,
      price_per_night: Math.floor(Math.random() * 200) + 50
    },
    contact: {
      name: `Test Contact ${Math.random().toString(36).substr(2, 9)}`,
      email: `test${Math.random().toString(36).substr(2, 9)}@example.com`,
      phone: `+123456789${Math.floor(Math.random() * 10)}`
    },
    review: {
      rating: Math.floor(Math.random() * 5) + 1,
      comment: `Test review ${Math.random().toString(36).substr(2, 9)}`,
      guest_name: `Test Guest ${Math.random().toString(36).substr(2, 9)}`
    }
  };

  return baseData[type];
}
