/**
 * Tests unitarios para tipos de Contacts
 */

import {
  Contact,
  ContactReference,
  ContactTag,
  ContactLinks,
  GetContactsParams,
  ContactsResponse,
  ContactFilters
} from '../../../src/types/contacts.js';

describe('Contacts Types', () => {
  describe('Contact interface', () => {
    it('debe permitir contacto completo', () => {
      const contact: Contact = {
        id: 1,
        firstName: 'Juan',
        lastName: 'Pérez',
        primaryEmail: 'juan@example.com',
        secondaryEmail: 'juan.secondary@example.com',
        homePhone: '+1234567890',
        cellPhone: '+0987654321',
        workPhone: '+1122334455',
        otherPhone: '+5566778899',
        fax: '+1234567890',
        streetAddress: '123 Main St',
        country: 'México',
        postalCode: '12345',
        region: 'CDMX',
        locality: 'Ciudad de México',
        extendedAddress: 'Apt 4B',
        notes: 'Cliente VIP',
        anniversary: '2024-01-15',
        birthdate: '1990-05-20',
        isVip: true,
        isBlacklist: false,
        taxId: 'RFC123456789',
        paymentType: 'direct',
        achAccountNumber: '1234567890',
        achRoutingNumber: '987654321',
        achAccountType: 'business-checking',
        references: [
          {
            reference: 'REF-001',
            salesLinkId: 1,
            channelId: 2
          }
        ],
        tags: [
          {
            id: 1,
            name: 'VIP'
          }
        ],
        customValues: {
          'custom_field_1': 'value1',
          'custom_field_2': ['value2', 'value3']
        },
        _links: {
          self: {
            href: '/contacts/1'
          }
        },
        updatedAt: '2024-01-15T10:30:00Z',
        updatedBy: 'admin',
        createdAt: '2024-01-01T00:00:00Z',
        createdBy: 'system',
        noIdentity: false
      };

      expect(contact.id).toBe(1);
      expect(contact.firstName).toBe('Juan');
      expect(contact.lastName).toBe('Pérez');
      expect(contact.primaryEmail).toBe('juan@example.com');
      expect(contact.secondaryEmail).toBe('juan.secondary@example.com');
      expect(contact.homePhone).toBe('+1234567890');
      expect(contact.cellPhone).toBe('+0987654321');
      expect(contact.workPhone).toBe('+1122334455');
      expect(contact.otherPhone).toBe('+5566778899');
      expect(contact.fax).toBe('+1234567890');
      expect(contact.streetAddress).toBe('123 Main St');
      expect(contact.country).toBe('México');
      expect(contact.postalCode).toBe('12345');
      expect(contact.region).toBe('CDMX');
      expect(contact.locality).toBe('Ciudad de México');
      expect(contact.extendedAddress).toBe('Apt 4B');
      expect(contact.notes).toBe('Cliente VIP');
      expect(contact.anniversary).toBe('2024-01-15');
      expect(contact.birthdate).toBe('1990-05-20');
      expect(contact.isVip).toBe(true);
      expect(contact.isBlacklist).toBe(false);
      expect(contact.taxId).toBe('RFC123456789');
      expect(contact.paymentType).toBe('direct');
      expect(contact.achAccountNumber).toBe('1234567890');
      expect(contact.achRoutingNumber).toBe('987654321');
      expect(contact.achAccountType).toBe('business-checking');
      expect(contact.references).toHaveLength(1);
      expect(contact.tags).toHaveLength(1);
      expect(contact.customValues).toBeDefined();
      expect(contact._links).toBeDefined();
      expect(contact.updatedAt).toBe('2024-01-15T10:30:00Z');
      expect(contact.updatedBy).toBe('admin');
      expect(contact.createdAt).toBe('2024-01-01T00:00:00Z');
      expect(contact.createdBy).toBe('system');
      expect(contact.noIdentity).toBe(false);
    });

    it('debe permitir contacto mínimo', () => {
      const contact: Contact = {
        id: 1,
        firstName: 'Juan',
        lastName: 'Pérez',
        primaryEmail: 'juan@example.com',
        isVip: false,
        isBlacklist: false,
        noIdentity: false,
        updatedAt: '2024-01-15T10:30:00Z',
        updatedBy: 'admin',
        createdAt: '2024-01-01T00:00:00Z',
        createdBy: 'system'
      };

      expect(contact.id).toBe(1);
      expect(contact.firstName).toBe('Juan');
      expect(contact.lastName).toBe('Pérez');
      expect(contact.primaryEmail).toBe('juan@example.com');
      expect(contact.isVip).toBe(false);
      expect(contact.isBlacklist).toBe(false);
      expect(contact.noIdentity).toBe(false);
    });

    it('debe permitir diferentes tipos de pago', () => {
      const paymentTypes: Contact['paymentType'][] = ['print', 'direct'];
      
      paymentTypes.forEach(paymentType => {
        const contact: Contact = {
          id: 1,
          firstName: 'Juan',
          lastName: 'Pérez',
          primaryEmail: 'juan@example.com',
          isVip: false,
          isBlacklist: false,
          noIdentity: false,
          updatedAt: '2024-01-15T10:30:00Z',
          updatedBy: 'admin',
          createdAt: '2024-01-01T00:00:00Z',
          createdBy: 'system'
        };
        
        if (paymentType) {
          contact.paymentType = paymentType;
        }
        
        expect(contact.paymentType).toBe(paymentType);
      });
    });

    it('debe permitir diferentes tipos de cuenta ACH', () => {
      const accountTypes: Contact['achAccountType'][] = [
        'business-checking',
        'business-savings',
        'personal-checking',
        'personal-savings'
      ];
      
      accountTypes.forEach(achAccountType => {
        const contact: Contact = {
          id: 1,
          firstName: 'Juan',
          lastName: 'Pérez',
          primaryEmail: 'juan@example.com',
          isVip: false,
          isBlacklist: false,
          noIdentity: false,
          updatedAt: '2024-01-15T10:30:00Z',
          updatedBy: 'admin',
          createdAt: '2024-01-01T00:00:00Z',
          createdBy: 'system'
        };
        
        if (achAccountType) {
          contact.achAccountType = achAccountType;
        }
        
        expect(contact.achAccountType).toBe(achAccountType);
      });
    });
  });

  describe('ContactReference interface', () => {
    it('debe permitir referencia completa', () => {
      const reference: ContactReference = {
        reference: 'REF-001',
        salesLinkId: 1,
        channelId: 2
      };

      expect(reference.reference).toBe('REF-001');
      expect(reference.salesLinkId).toBe(1);
      expect(reference.channelId).toBe(2);
    });

    it('debe permitir referencia mínima', () => {
      const reference: ContactReference = {
        reference: 'REF-001',
        salesLinkId: 1,
        channelId: 2
      };

      expect(reference.reference).toBe('REF-001');
      expect(reference.salesLinkId).toBe(1);
      expect(reference.channelId).toBe(2);
    });
  });

  describe('ContactTag interface', () => {
    it('debe permitir tag completo', () => {
      const tag: ContactTag = {
        id: 1,
        name: 'VIP'
      };

      expect(tag.id).toBe(1);
      expect(tag.name).toBe('VIP');
    });

    it('debe permitir diferentes tags', () => {
      const tags: ContactTag[] = [
        { id: 1, name: 'VIP' },
        { id: 2, name: 'Frequent Guest' },
        { id: 3, name: 'Corporate' }
      ];

      tags.forEach(tag => {
        expect(tag.id).toBeGreaterThan(0);
        expect(tag.name).toBeDefined();
      });
    });
  });

  describe('ContactLinks interface', () => {
    it('debe permitir links completos', () => {
      const links: ContactLinks = {
        self: {
          href: '/contacts/1'
        }
      };

      expect(links.self.href).toBe('/contacts/1');
    });

    it('debe permitir diferentes URLs', () => {
      const testUrls = [
        '/contacts/1',
        '/api/v1/contacts/1',
        'https://api.trackhs.com/contacts/1'
      ];

      testUrls.forEach(href => {
        const links: ContactLinks = {
          self: { href }
        };
        expect(links.self.href).toBe(href);
      });
    });
  });

  describe('GetContactsParams interface', () => {
    it('debe permitir parámetros completos', () => {
      const params: GetContactsParams = {
        sortColumn: 'name',
        sortDirection: 'asc',
        search: 'Juan',
        term: 'Pérez',
        email: 'juan@example.com',
        page: 1,
        size: 10,
        updatedSince: '2024-01-01T00:00:00Z'
      };

      expect(params.sortColumn).toBe('name');
      expect(params.sortDirection).toBe('asc');
      expect(params.search).toBe('Juan');
      expect(params.term).toBe('Pérez');
      expect(params.email).toBe('juan@example.com');
      expect(params.page).toBe(1);
      expect(params.size).toBe(10);
      expect(params.updatedSince).toBe('2024-01-01T00:00:00Z');
    });

    it('debe permitir parámetros opcionales', () => {
      const params: GetContactsParams = {};

      expect(params.sortColumn).toBeUndefined();
      expect(params.sortDirection).toBeUndefined();
      expect(params.search).toBeUndefined();
      expect(params.term).toBeUndefined();
      expect(params.email).toBeUndefined();
      expect(params.page).toBeUndefined();
      expect(params.size).toBeUndefined();
      expect(params.updatedSince).toBeUndefined();
    });

    it('debe permitir diferentes sortColumn', () => {
      const sortColumns: GetContactsParams['sortColumn'][] = [
        'id', 'name', 'email', 'cellPhone', 'homePhone', 'otherPhone', 'vip'
      ];
      
      sortColumns.forEach(sortColumn => {
        const params: GetContactsParams = {};
        if (sortColumn) {
          params.sortColumn = sortColumn;
        }
        expect(params.sortColumn).toBe(sortColumn);
      });
    });

    it('debe permitir diferentes sortDirection', () => {
      const sortDirections: GetContactsParams['sortDirection'][] = ['asc', 'desc'];
      
      sortDirections.forEach(sortDirection => {
        const params: GetContactsParams = {};
        if (sortDirection) {
          params.sortDirection = sortDirection;
        }
        expect(params.sortDirection).toBe(sortDirection);
      });
    });
  });

  describe('ContactsResponse interface', () => {
    it('debe permitir respuesta completa', () => {
      const response: ContactsResponse = {
        _embedded: {
          contacts: [
            {
              id: 1,
              firstName: 'Juan',
              lastName: 'Pérez',
              primaryEmail: 'juan@example.com',
              isVip: false,
              isBlacklist: false,
              noIdentity: false,
              updatedAt: '2024-01-15T10:30:00Z',
              updatedBy: 'admin',
              createdAt: '2024-01-01T00:00:00Z',
              createdBy: 'system'
            }
          ]
        }
      };

      expect(response._embedded.contacts).toHaveLength(1);
      expect(response._embedded.contacts[0]?.id).toBe(1);
      expect(response._embedded.contacts[0]?.firstName).toBe('Juan');
    });

    it('debe permitir respuesta vacía', () => {
      const response: ContactsResponse = {
        _embedded: {
          contacts: []
        }
      };

      expect(response._embedded.contacts).toHaveLength(0);
    });

    it('debe permitir múltiples contactos', () => {
      const response: ContactsResponse = {
        _embedded: {
          contacts: [
            {
              id: 1,
              firstName: 'Juan',
              lastName: 'Pérez',
              primaryEmail: 'juan@example.com',
              isVip: false,
              isBlacklist: false,
              noIdentity: false,
              updatedAt: '2024-01-15T10:30:00Z',
              updatedBy: 'admin',
              createdAt: '2024-01-01T00:00:00Z',
              createdBy: 'system'
            },
            {
              id: 2,
              firstName: 'María',
              lastName: 'García',
              primaryEmail: 'maria@example.com',
              isVip: true,
              isBlacklist: false,
              noIdentity: false,
              updatedAt: '2024-01-15T10:30:00Z',
              updatedBy: 'admin',
              createdAt: '2024-01-01T00:00:00Z',
              createdBy: 'system'
            }
          ]
        }
      };

      expect(response._embedded.contacts).toHaveLength(2);
      expect(response._embedded.contacts[0]?.id).toBe(1);
      expect(response._embedded.contacts[1]?.id).toBe(2);
    });
  });

  describe('ContactFilters interface', () => {
    it('debe permitir filtros completos', () => {
      const filters: ContactFilters = {
        isVip: true,
        isBlacklist: false,
        country: 'México',
        region: 'CDMX',
        tags: ['VIP', 'Corporate'],
        dateFrom: '2024-01-01T00:00:00Z',
        dateTo: '2024-12-31T23:59:59Z'
      };

      expect(filters.isVip).toBe(true);
      expect(filters.isBlacklist).toBe(false);
      expect(filters.country).toBe('México');
      expect(filters.region).toBe('CDMX');
      expect(filters.tags).toEqual(['VIP', 'Corporate']);
      expect(filters.dateFrom).toBe('2024-01-01T00:00:00Z');
      expect(filters.dateTo).toBe('2024-12-31T23:59:59Z');
    });

    it('debe permitir filtros opcionales', () => {
      const filters: ContactFilters = {};

      expect(filters.isVip).toBeUndefined();
      expect(filters.isBlacklist).toBeUndefined();
      expect(filters.country).toBeUndefined();
      expect(filters.region).toBeUndefined();
      expect(filters.tags).toBeUndefined();
      expect(filters.dateFrom).toBeUndefined();
      expect(filters.dateTo).toBeUndefined();
    });

    it('debe permitir diferentes valores booleanos', () => {
      const testCases = [
        { isVip: true, isBlacklist: false },
        { isVip: false, isBlacklist: true },
        { isVip: true, isBlacklist: true },
        { isVip: false, isBlacklist: false }
      ];

      testCases.forEach(({ isVip, isBlacklist }) => {
        const filters: ContactFilters = { isVip, isBlacklist };
        expect(filters.isVip).toBe(isVip);
        expect(filters.isBlacklist).toBe(isBlacklist);
      });
    });

    it('debe permitir diferentes tags', () => {
      const tags = ['VIP', 'Corporate', 'Frequent Guest', 'Blacklist'];
      const filters: ContactFilters = { tags };
      expect(filters.tags).toEqual(tags);
    });
  });

  describe('Integración entre tipos', () => {
    it('debe permitir flujo completo de datos', () => {
      const contact: Contact = {
        id: 1,
        firstName: 'Juan',
        lastName: 'Pérez',
        primaryEmail: 'juan@example.com',
        isVip: true,
        isBlacklist: false,
        noIdentity: false,
        updatedAt: '2024-01-15T10:30:00Z',
        updatedBy: 'admin',
        createdAt: '2024-01-01T00:00:00Z',
        createdBy: 'system'
      };

      const params: GetContactsParams = {
        sortColumn: 'name',
        sortDirection: 'asc',
        search: 'Juan',
        page: 1,
        size: 10
      };

      const response: ContactsResponse = {
        _embedded: {
          contacts: [contact]
        }
      };

      const filters: ContactFilters = {
        isVip: true,
        country: 'México'
      };

      expect(contact).toBeDefined();
      expect(params).toBeDefined();
      expect(response).toBeDefined();
      expect(filters).toBeDefined();
    });
  });
});
