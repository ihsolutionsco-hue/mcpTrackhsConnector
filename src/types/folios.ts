/**
 * Tipos específicos para el API de Folios de Track HS
 */

export interface FolioContact {
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
  isVip?: boolean;
  isBlacklist?: boolean;
  taxId?: string;
  paymentType?: 'print' | 'direct';
  achAccountNumber?: string;
  achRoutingNumber?: string;
  achAccountType?: 'business-checking' | 'business-savings' | 'personal-checking' | 'personal-savings';
  references?: Array<{
    reference: string;
    salesLinkId?: number;
    channelId?: number;
  }>;
  tags?: Array<{
    id: number;
    name: string;
  }>;
  customValues?: Record<string, any>;
  noIdentity?: boolean;
  _links: {
    self: { href: string };
  };
  updatedAt: string;
  createdBy: string;
  createdAt: string;
}

export interface FolioCompany {
  id: number;
  type: 'company' | 'agent' | 'vendor' | 'owner';
  isActive: boolean;
  name: string;
  streetAddress?: string;
  extendedAddress?: string;
  locality?: string;
  region?: string;
  postal?: string;
  country?: string;
  taxType?: 'rents' | 'other' | 'none' | 'non_employee_compensation';
  taxName?: string;
  taxId?: string;
  achAccountNumber?: string;
  achRoutingNumber?: string;
  achAccountType?: 'business-checking' | 'business-savings' | 'personal-checking' | 'personal-savings';
  achVerifiedAt?: string;
  paymentType?: 'print' | 'direct';
  glExpirationDate?: string;
  glInsurancePolicy?: string;
  wcExpirationDate?: string;
  wcInsurancePolicy?: string;
  travelAgentDeductCommission?: boolean;
  travelAgentCommission?: number;
  travelAgentIataNumber?: string;
  enableWorkOrderApproval?: boolean;
  notes?: string;
  website?: string;
  email?: string;
  fax?: string;
  phone?: string;
  tags?: Array<{
    id: number;
    name: string;
  }>;
  _links: {
    self: { href: string };
    contacts?: { href: string };
    licences?: { href: string };
  };
  createdBy: string;
  createdAt: string;
  updatedBy: string;
  updatedAt: string;
}

export interface FolioRule {
  id: number;
  name: string;
  type: 'guest' | 'master' | 'guest-sub-folio' | 'master-sub-folio';
  status: 'open' | 'closed';
  startDate: string;
  endDate: string;
  contactName: string;
  companyName?: string;
  reservationId?: number;
  currentBalance: string;
  realizedBalance: string;
  masterFolioRule?: number;
  _links: {
    self: { href: string };
  };
  updatedAt: string;
  createdAt: string;
}

export interface GetFoliosCollectionParams {
  // Paginación
  page?: number;
  size?: number;
  
  // Ordenamiento
  sortColumn?: 'id' | 'name' | 'status' | 'type' | 'startDate' | 'endDate' | 'contactName' | 'companyName' | 'reservationId' | 'currentBalance' | 'realizedBalance' | 'masterFolioRule';
  sortDirection?: 'asc' | 'desc';
  
  // Búsqueda
  search?: string;
  
  // Filtros por tipo
  type?: 'guest' | 'master' | 'guest-sub-folio' | 'master-sub-folio';
  status?: 'open' | 'closed';
  
  // Filtros por ID
  masterFolioId?: number;
  contactId?: number;
  companyId?: number;
}

export interface GetFoliosCollectionResponse {
  _embedded: {
    folios: FolioRule[];
  };
  page: number;
  page_count: number;
  page_size: number;
  total_items: number;
  _links: {
    self: { href: string };
    first: { href: string };
    last: { href: string };
    next?: { href: string };
    prev?: { href: string };
  };
}

export interface FolioFilters {
  type?: 'guest' | 'master' | 'guest-sub-folio' | 'master-sub-folio';
  status?: 'open' | 'closed';
  masterFolioId?: number;
  contactId?: number;
  companyId?: number;
  dateFrom?: string;
  dateTo?: string;
}