/**
 * Tipos específicos para el API de Contacts de Track HS
 */

export interface Contact {
  id: number;
  firstName: string;
  lastName: string;
  primaryEmail: string;
  secondaryEmail?: string;
  homePhone?: string;
  cellPhone?: string;
  workPhone?: string;
  otherPhone?: string;
  fax?: string;
  streetAddress?: string;
  country?: string;
  postalCode?: string;
  region?: string;
  locality?: string;
  extendedAddress?: string;
  notes?: string;
  anniversary?: string;
  birthdate?: string;
  isVip: boolean;
  isBlacklist: boolean;
  taxId?: string;
  paymentType?: 'print' | 'direct';
  achAccountNumber?: string;
  achRoutingNumber?: string;
  achAccountType?: 'business-checking' | 'business-savings' | 'personal-checking' | 'personal-savings';
  references?: ContactReference[];
  tags?: ContactTag[];
  customValues?: Record<string, string | string[]>;
  _links?: ContactLinks;
  updatedAt: string;
  updatedBy: string;
  createdAt: string;
  createdBy: string;
  noIdentity: boolean;
}

export interface ContactReference {
  reference: string;
  salesLinkId: number;
  channelId: number;
}

export interface ContactTag {
  id: number;
  name: string;
}

export interface ContactLinks {
  self: {
    href: string;
  };
}

export interface GetContactsParams {
  sortColumn?: 'id' | 'name' | 'email' | 'cellPhone' | 'homePhone' | 'otherPhone' | 'vip';
  sortDirection?: 'asc' | 'desc';
  search?: string;
  term?: string;
  email?: string;
  page?: number;
  size?: number;
  updatedSince?: string;
}

export interface ContactsResponse {
  _embedded: {
    contacts: Contact[];
  };
}

export interface ContactFilters {
  isVip?: boolean;
  isBlacklist?: boolean;
  country?: string;
  region?: string;
  tags?: string[];
  dateFrom?: string;
  dateTo?: string;
}