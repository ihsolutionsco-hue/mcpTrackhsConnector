/**
 * Tipos específicos para el API de Ledger Accounts de Track HS
 */

export interface LedgerAccount {
  id: number;
  code: string;
  name: string;
  description?: string;
  category: 'revenue' | 'asset' | 'equity' | 'expense' | 'liability';
  accountType: 'bank' | 'current' | 'fixed' | 'other-asset' | 'receivable';
  parentId?: number;
  isActive: boolean;
  externalId?: number;
  externalName?: string;
  bankName?: string;
  achEnabled: boolean;
  allowOwnerPayments: boolean;
  achOrginId?: number;
  routingNumber?: number;
  accountNumber?: number;
  currency?: string;
  currentBalance?: number;
  recursiveBalance?: number;
  immediateDestination?: number;
  immediateDestinationName?: string;
  immediateOriginName?: string;
  companyName?: string;
  companyIdentification?: number;
  stakeholderId?: number;
  enableRefunds: boolean;
  defaultRefundAccount?: number;
  createdBy: string;
  createdAt: string;
  updatedBy: string;
  updatedAt: string;
  _embedded?: {
    parent?: LedgerAccount;
    stakeholder?: Stakeholder;
  };
  _links?: LedgerAccountLinks;
}

export interface Stakeholder {
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
  createdBy: string;
  createdAt: string;
  updatedBy: string;
  updatedAt: string;
  tags?: StakeholderTag[];
  _links?: StakeholderLinks;
}

export interface StakeholderTag {
  id: number;
  name: string;
}

export interface StakeholderLinks {
  self: {
    href: string;
  };
  contacts?: {
    href: string;
  };
  licences?: {
    href: string;
  };
}

export interface LedgerAccountLinks {
  self: {
    href: string;
  };
}

export interface GetLedgerAccountsParams {
  page?: number;
  size?: number;
  sortColumn?: 'id' | 'name' | 'type' | 'relativeOrder' | 'isActive';
  sortDirection?: 'asc' | 'desc';
  search?: string;
  isActive?: number;
  category?: 'Revenue' | 'Asset' | 'Equity' | 'Liability' | 'Expense';
  accountType?: string;
  parentId?: number;
  includeRestricted?: number;
  sortByCategoryValue?: number;
}

export interface LedgerAccountsResponse {
  _embedded: {
    accounts: LedgerAccount[];
  };
}

export interface GetLedgerAccountParams {
  accountId: number;
}

export interface LedgerAccountResponse {
  // Reutiliza la interfaz LedgerAccount existente
  // No necesita paginación ni _embedded wrapper
}

export interface LedgerAccountFilters {
  category?: string;
  accountType?: string;
  isActive?: boolean;
  parentId?: number;
  stakeholderId?: number;
  currency?: string;
  dateFrom?: string;
  dateTo?: string;
}
