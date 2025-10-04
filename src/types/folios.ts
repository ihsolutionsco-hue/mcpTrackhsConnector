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
  code: string;
  isActive: boolean;
  type: 'percent' | 'breakdown';
  percentAmount?: number;
  breakdownRentMode?: 'percent' | 'nights';
  breakdownRentIncludeTax?: boolean;
  breakdownRentPercent?: number;
  breakdownRentNights?: number;
  breakdownFeeMode?: 'percent' | 'required';
  breakdownFeeIncludeTax?: boolean;
  breakdownFeePercent?: number;
  breakdownChargesMode?: 'percent' | 'required';
  breakdownChargesIncludeTax?: boolean;
  _links: {
    self: { href: string };
  };
  createdBy: string;
  createdAt: string;
  updatedBy: string;
  updatedAt: string;
}

export interface MasterFolioRule {
  id: number;
  ruleId: number;
  startDate?: string;
  endDate?: string;
  minNights?: number;
  maxNights?: number;
  maxSpend?: number;
  createdBy: string;
  createdAt: string;
  updatedBy: string;
  updatedAt: string;
  _embedded?: {
    rule: FolioRule;
  };
  _links: {
    self: { href: string };
  };
}

export interface Folio {
  id: number;
  status: 'open' | 'closed';
  type: 'guest' | 'master';
  currentBalance: number;
  realizedBalance: number;
  closedDate?: string;
  endDate?: string;
  startDate?: string;
  taxEmpty: boolean;
  companyId?: number;
  contactId: number;
  
  // Campos opcionales según tipo de folio
  masterFolioRuleId?: number;
  masterFolioId?: number;
  agentCommission?: number;
  ownerCommission?: number;
  ownerRevenue?: number;
  checkOutDate?: string;
  checkInDate?: string;
  exceptionMessage?: string;
  hasException?: boolean;
  travelAgentId?: number;
  reservationId?: number;
  name?: string;
  
  _links: {
    self: { href: string };
    logs?: { href: string };
  };
  updatedAt: string;
  updatedBy: string;
  createdAt: string;
  createdBy: string;
  
  _embedded?: {
    contact?: FolioContact;
    travelAgent?: FolioCompany;
    company?: FolioCompany;
    masterFolioRule?: MasterFolioRule;
    masterFolio?: Folio;
  };
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
    folios: Folio[];
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
