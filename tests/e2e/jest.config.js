/**
 * Configuración de Jest para tests E2E
 */

module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests/e2e'],
  testMatch: [
    '**/tests/e2e/**/*.test.ts',
    '**/tests/e2e/**/*.e2e.test.ts'
  ],
  transform: {
    '^.+\\.ts$': ['ts-jest', {
      useESM: true
    }],
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/index.ts',
    '!src/server.ts'
  ],
  coverageDirectory: 'coverage/e2e',
  coverageReporters: ['text', 'lcov', 'html'],
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  testTimeout: 60000, // 60 segundos para tests E2E
  verbose: true,
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  extensionsToTreatAsEsm: ['.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  moduleNameMapper: {
    '^(\\.{1,2}/.*)\\.js$': '$1'
  },
  // Configuración específica para tests E2E
  testEnvironmentOptions: {
    url: 'https://api.trackhs.test'
  },
  // Configurar variables de entorno para tests E2E
  setupFiles: ['<rootDir>/tests/e2e/setup.ts'],
  // Configuración para tests de performance
  maxWorkers: 1, // Ejecutar tests E2E secuencialmente
  // Configuración para tests de usuario
  testSequencer: '<rootDir>/tests/e2e/sequencer.js'
};
