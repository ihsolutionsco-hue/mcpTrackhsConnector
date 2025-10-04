/**
 * Tests unitarios para TrackHSAuth
 */

import { TrackHSAuth } from '../../../src/core/auth.js';
import { TrackHSConfig } from '../../../src/core/types.js';

describe('TrackHSAuth', () => {
  let auth: TrackHSAuth;
  let config: TrackHSConfig;

  beforeEach(() => {
    config = {
      baseUrl: 'https://api.trackhs.test',
      username: 'test_user',
      password: 'test_password'
    };
  });

  describe('Constructor', () => {
    it('debe inicializar correctamente con credenciales válidas', () => {
      expect(() => {
        auth = new TrackHSAuth(config);
      }).not.toThrow();
    });

    it('debe codificar credenciales en base64', () => {
      auth = new TrackHSAuth(config);
      
      // Verificar que las credenciales se codifican correctamente
      const expectedCredentials = Buffer.from('test_user:test_password').toString('base64');
      expect(auth.getAuthHeader()).toBe(`Basic ${expectedCredentials}`);
    });

    it('debe manejar caracteres especiales en credenciales', () => {
      const specialConfig: TrackHSConfig = {
        ...config,
        username: 'user@domain.com',
        password: 'p@ssw0rd!'
      };

      auth = new TrackHSAuth(specialConfig);
      
      const expectedCredentials = Buffer.from('user@domain.com:p@ssw0rd!').toString('base64');
      expect(auth.getAuthHeader()).toBe(`Basic ${expectedCredentials}`);
    });

    it('debe manejar credenciales vacías', () => {
      const emptyConfig: TrackHSConfig = {
        ...config,
        username: '',
        password: ''
      };

      auth = new TrackHSAuth(emptyConfig);
      
      const expectedCredentials = Buffer.from(':').toString('base64');
      expect(auth.getAuthHeader()).toBe(`Basic ${expectedCredentials}`);
    });

    it('debe manejar espacios en credenciales', () => {
      const spacedConfig: TrackHSConfig = {
        ...config,
        username: ' test user ',
        password: ' test password '
      };

      auth = new TrackHSAuth(spacedConfig);
      
      const expectedCredentials = Buffer.from(' test user : test password ').toString('base64');
      expect(auth.getAuthHeader()).toBe(`Basic ${expectedCredentials}`);
    });
  });

  describe('getAuthHeader', () => {
    beforeEach(() => {
      auth = new TrackHSAuth(config);
    });

    it('debe retornar header de autorización correcto', () => {
      const header = auth.getAuthHeader();
      
      expect(header).toMatch(/^Basic /);
      expect(header.length).toBeGreaterThan(6); // "Basic " + base64 string
    });

    it('debe retornar el mismo header en múltiples llamadas', () => {
      const header1 = auth.getAuthHeader();
      const header2 = auth.getAuthHeader();
      
      expect(header1).toBe(header2);
    });

    it('debe generar header válido para diferentes credenciales', () => {
      const testCases = [
        { username: 'user1', password: 'pass1' },
        { username: 'user2', password: 'pass2' },
        { username: 'admin', password: 'admin123' }
      ];

      testCases.forEach(({ username, password }) => {
        const testConfig: TrackHSConfig = { ...config, username, password };
        const testAuth = new TrackHSAuth(testConfig);
        const header = testAuth.getAuthHeader();
        
        expect(header).toMatch(/^Basic /);
        
        // Verificar que el header contiene las credenciales codificadas
        const expectedCredentials = Buffer.from(`${username}:${password}`).toString('base64');
        expect(header).toBe(`Basic ${expectedCredentials}`);
      });
    });
  });

  describe('validateCredentials', () => {
    it('debe retornar true para credenciales válidas', () => {
      auth = new TrackHSAuth(config);
      expect(auth.validateCredentials()).toBe(true);
    });

    it('debe retornar true para credenciales no vacías', () => {
      const nonEmptyConfig: TrackHSConfig = {
        ...config,
        username: 'any_user',
        password: 'any_password'
      };

      auth = new TrackHSAuth(nonEmptyConfig);
      expect(auth.validateCredentials()).toBe(true);
    });

    it('debe retornar true para credenciales con espacios', () => {
      const spacedConfig: TrackHSConfig = {
        ...config,
        username: ' user ',
        password: ' pass '
      };

      auth = new TrackHSAuth(spacedConfig);
      expect(auth.validateCredentials()).toBe(true);
    });

    it('debe retornar true para credenciales con caracteres especiales', () => {
      const specialConfig: TrackHSConfig = {
        ...config,
        username: 'user@domain.com',
        password: 'p@ssw0rd!'
      };

      auth = new TrackHSAuth(specialConfig);
      expect(auth.validateCredentials()).toBe(true);
    });

    it('debe retornar true para credenciales vacías (técnicamente válidas)', () => {
      const emptyConfig: TrackHSConfig = {
        ...config,
        username: '',
        password: ''
      };

      auth = new TrackHSAuth(emptyConfig);
      expect(auth.validateCredentials()).toBe(true);
    });
  });

  describe('Integración con diferentes configuraciones', () => {
    it('debe funcionar con configuración de producción', () => {
      const prodConfig: TrackHSConfig = {
        baseUrl: 'https://api.trackhs.com',
        username: 'prod_user',
        password: 'prod_password'
      };

      auth = new TrackHSAuth(prodConfig);
      
      expect(auth.validateCredentials()).toBe(true);
      expect(auth.getAuthHeader()).toMatch(/^Basic /);
    });

    it('debe funcionar con configuración de desarrollo', () => {
      const devConfig: TrackHSConfig = {
        baseUrl: 'http://localhost:3000',
        username: 'dev_user',
        password: 'dev_password'
      };

      auth = new TrackHSAuth(devConfig);
      
      expect(auth.validateCredentials()).toBe(true);
      expect(auth.getAuthHeader()).toMatch(/^Basic /);
    });

    it('debe funcionar con credenciales largas', () => {
      const longConfig: TrackHSConfig = {
        ...config,
        username: 'very_long_username_that_might_be_used_in_production',
        password: 'very_long_password_with_special_characters_!@#$%^&*()_+'
      };

      auth = new TrackHSAuth(longConfig);
      
      expect(auth.validateCredentials()).toBe(true);
      expect(auth.getAuthHeader()).toMatch(/^Basic /);
    });
  });

  describe('Manejo de errores', () => {
    it('debe manejar credenciales undefined', () => {
      const undefinedConfig: TrackHSConfig = {
        baseUrl: 'https://api.trackhs.test',
        username: undefined as any,
        password: undefined as any
      };

      expect(() => {
        auth = new TrackHSAuth(undefinedConfig);
      }).not.toThrow();
    });

    it('debe manejar credenciales null', () => {
      const nullConfig: TrackHSConfig = {
        baseUrl: 'https://api.trackhs.test',
        username: null as any,
        password: null as any
      };

      expect(() => {
        auth = new TrackHSAuth(nullConfig);
      }).not.toThrow();
    });
  });

  describe('Consistencia de datos', () => {
    it('debe mantener consistencia entre getAuthHeader y validateCredentials', () => {
      auth = new TrackHSAuth(config);
      
      const header = auth.getAuthHeader();
      const isValid = auth.validateCredentials();
      
      expect(isValid).toBe(true);
      expect(header).toMatch(/^Basic /);
    });

    it('debe retornar el mismo resultado en múltiples validaciones', () => {
      auth = new TrackHSAuth(config);
      
      const validation1 = auth.validateCredentials();
      const validation2 = auth.validateCredentials();
      const validation3 = auth.validateCredentials();
      
      expect(validation1).toBe(validation2);
      expect(validation2).toBe(validation3);
    });
  });
});
