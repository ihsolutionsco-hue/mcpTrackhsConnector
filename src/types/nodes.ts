/**
 * Tipos específicos para el API de Nodes de Track HS
 */

export interface NodeType {
  id: number;
  name: string;
  description?: string;
  isReport?: boolean;
  isReservations?: boolean;
  isHousekeeping?: boolean;
  isMaintenance?: boolean;
  isOnline?: boolean;
  isOwners?: boolean;
  isActive?: boolean;
  createdAt?: string;
  createdBy?: string;
  updatedAt?: string;
  updatedBy?: string;
  _links?: {
    self: { href: string };
  };
}

export interface TaxDistrict {
  id: number;
  isActive?: boolean;
  name?: string;
  shortTermPolicyId?: number;
  longTermPolicyId?: number;
  hasBreakpoint?: boolean;
  breakpoint?: number;
  salesTaxPolicyId?: number;
  salesTaxPolicy?: any;
  taxMarkup?: number;
  createdAt?: string;
  createdBy?: string;
  updatedAt?: string;
  updatedBy?: string;
  _embedded?: {
    shortTermPolicy?: any;
    longTermPolicy?: any;
  };
  _links?: {
    self: { href: string };
  };
}

export interface CancellationPolicy {
  id: number;
  isDefault?: boolean;
  isActive?: boolean;
  name?: string;
  createdBy?: string;
  createdAt?: string;
  updatedBy?: string;
  updatedAt?: string;
  code?: string;
  chargeAs?: string;
  canExceedBalance?: boolean;
  cancelTime?: string;
  cancelTimezone?: string;
  postDate?: string;
  airbnbType?: string;
  tripadvisorType?: string;
  homeawayType?: string;
  breakpoints?: CancellationBreakpoint[];
  _links?: {
    self: { href: string };
  };
}

export interface CancellationBreakpoint {
  id: number;
  rangeStart: number;
  rangeEnd: number;
  nonRefundable: boolean;
  nonCancelable: boolean;
  penaltyNights: number;
  penaltyPercent: number;
  penaltyFlat: number;
  description: string;
}

export interface HousekeepingZone {
  id: number;
  isActive?: boolean;
  name?: string;
  type?: string;
  createdAt?: string;
  createdBy?: string;
  updatedAt?: string;
  updatedBy?: string;
  _links?: {
    self: { href: string };
  };
}

export interface MaintenanceZone {
  id: number;
  isActive?: boolean;
  name?: string;
  type?: string;
  createdAt?: string;
  createdBy?: string;
  updatedAt?: string;
  updatedBy?: string;
  _links?: {
    self: { href: string };
  };
}

export interface Node {
  id: number;
  name: string;
  maxPets?: number;
  phone?: string;
  websiteUrl?: string;
  streetAddress?: string;
  extendedAddress?: string;
  locality?: string;
  region?: string;
  postal?: string;
  country?: string;
  maxDiscount?: number;
  timezone?: string;
  longitude?: number;
  latitude?: number;
  housekeepingNotes?: string;
  petFriendly?: boolean;
  smokingAllowed?: boolean;
  childrenAllowed?: boolean;
  eventsAllowed?: boolean;
  isAccessible?: boolean;
  hasEarlyCheckin?: boolean;
  hasLateCheckout?: boolean;
  quickCheckin?: boolean;
  quickCheckout?: boolean;
  checkinTime?: string;
  checkoutTime?: string;
  earlyCheckinTime?: string;
  lateCheckoutTime?: string;
  description?: string;
  shortDescription?: string;
  longDescription?: string;
  directions?: string;
  checkinDetails?: string;
  houseRules?: string;
  parentId?: number;
  parent?: any;
  typeId?: number;
  type?: NodeType;
  taxDistrictId?: number;
  taxDistrict?: TaxDistrict;
  checkinOfficeId?: number;
  checkinOffice?: any;
  cancellationPolicyId?: number;
  cancellationPolicy?: CancellationPolicy;
  housekeepingZoneId?: number;
  housekeepingZone?: HousekeepingZone;
  maintenanceZoneId?: number;
  maintenanceZone?: MaintenanceZone;
  isReservations?: boolean;
  isHousekeeping?: boolean;
  isMaintenance?: boolean;
  isOnline?: boolean;
  isOwners?: boolean;
  isActive?: boolean;
  createdAt?: string;
  createdBy?: string;
  updatedAt?: string;
  updatedBy?: string;
  roles?: Array<{
    roleId: number;
    userId: number;
  }>;
  custom?: any;
  guaranteePoliciesIds?: number[];
  amenitiesIds?: number[];
  documentsIds?: number[];
  gatewaysIds?: number[];
  _embedded?: {
    parent?: {
      _links: {
        self: { href: string };
      };
    };
    type?: NodeType;
    taxDistrict?: TaxDistrict;
    cancellationPolicy?: CancellationPolicy;
    housekeepingZone?: HousekeepingZone;
    maintenanceZone?: MaintenanceZone;
  };
  _links?: {
    self: { href: string };
    images?: { href: string };
  };
}

export interface GetNodesParams {
  page?: number;
  size?: number;
  sortColumn?: 'id' | 'name';
  sortDirection?: 'asc' | 'desc';
  search?: string;
  term?: string;
  parentId?: number;
  typeId?: number;
  computed?: 0 | 1;
  inherited?: 0 | 1;
  includeDescriptions?: 0 | 1;
}

export interface GetNodesResponse {
  _embedded: {
    nodes: Node[];
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

export interface GetNodeParams {
  nodeId: number;
}

export interface GetNodeResponse extends Node {}

export interface NodeFilters {
  parentId?: number;
  typeId?: number;
  isActive?: boolean;
  isReservations?: boolean;
  isHousekeeping?: boolean;
  isMaintenance?: boolean;
  isOnline?: boolean;
  isOwners?: boolean;
  petFriendly?: boolean;
  smokingAllowed?: boolean;
  childrenAllowed?: boolean;
  eventsAllowed?: boolean;
  isAccessible?: boolean;
}
