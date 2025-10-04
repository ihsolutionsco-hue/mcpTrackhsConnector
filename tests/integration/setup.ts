/**
 * Setup para tests de integración
 */

// Configurar variables de entorno para testing
process.env.NODE_ENV = 'test';
process.env.TRACKHS_API_URL = process.env.TRACKHS_API_URL || 'https://api.trackhs.test';
process.env.TRACKHS_USERNAME = process.env.TRACKHS_USERNAME || 'test_user';
process.env.TRACKHS_PASSWORD = process.env.TRACKHS_PASSWORD || 'test_password';

// Configurar timeout para tests de integración
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

// Configurar cleanup después de cada test
afterEach(() => {
  jest.clearAllMocks();
});

// Configurar cleanup después de todos los tests
afterAll(() => {
  jest.restoreAllMocks();
});

// Configurar manejo de errores no capturados
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
});
