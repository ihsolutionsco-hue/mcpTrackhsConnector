/**
 * Configuración para testing
 */

export const testConfig = {
  // URLs de API para testing
  api: {
    baseUrl: process.env.TRACKHS_API_URL || 'https://api.trackhs.test',
    timeout: 10000,
    retries: 3
  },

  // Configuración de autenticación para testing
  auth: {
    username: process.env.TRACKHS_USERNAME || 'test_user',
    password: process.env.TRACKHS_PASSWORD || 'test_password'
  },

  // Configuración de mocks
  mocks: {
    enabled: true,
    delay: 100, // Simular latencia de red
    timeout: 5000
  },

  // Configuración de datos de prueba
  testData: {
    // IDs de prueba
    reservationId: '123',
    unitId: '456',
    contactId: '101',
    nodeId: '401',
    ledgerAccountId: '201',
    
    // Fechas de prueba
    testDate: '2024-02-01',
    testDateTime: '2024-02-01T10:30:00Z',
    
    // Textos de prueba
    searchTerm: 'test',
    guestName: 'Test Guest'
  },

  // Configuración de paginación para testing
  pagination: {
    defaultPage: 1,
    defaultSize: 10,
    maxSize: 100
  },

  // Configuración de timeouts
  timeouts: {
    short: 1000,
    medium: 5000,
    long: 10000
  }
};

export default testConfig;
