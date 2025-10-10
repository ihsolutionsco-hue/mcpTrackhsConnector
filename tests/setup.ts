/**
 * Configuración global para los tests
 */

// Configurar variables de entorno para testing
process.env.NODE_ENV = 'test';
process.env.TRACKHS_API_URL = 'https://api.trackhs.com';
process.env.TRACKHS_USERNAME = 'test_user';
process.env.TRACKHS_PASSWORD = 'test_password';

// Configurar timeout global para tests
jest.setTimeout(30000);

// Mock de console para evitar logs durante los tests
const originalConsole = console;
global.console = {
  ...originalConsole,
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  info: jest.fn(),
  debug: jest.fn(),
};

// Limpiar mocks después de cada test
afterEach(() => {
  jest.clearAllMocks();
});

// Configurar cleanup después de todos los tests
afterAll(() => {
  jest.restoreAllMocks();
});
