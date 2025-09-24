/**
 * Tipos específicos para el API de Units de Track HS
 */

export interface UnitType {
  id: number;
  name: string;
}

export interface LodgingType {
  id: number;
  name: string;
}

export interface BedType {
  id: number;
  name: string;
  count: number;
  airbnbType?: string;
  homeawayType?: string;
  marriottType?: string;
}

export interface RoomBedType {
  id: number;
  name: string;
  count: string;
  airbnbType?: string;
  homeawayType?: string;
  marriottType?: string;
}

export interface Room {
  name: string;
  type: 'bedroom' | 'half_bathroom' | 'three_quarter_bathroom' | 'full_bathroom' | 'kitchen' | 'common' | 'outside';
  sleeps: number;
  description: string;
  hasAttachedBathroom: boolean;
  beds: RoomBedType[];
  order?: number;
  homeawayType?: string;
  airbnbType?: string;
}

export interface Amenity {
  id: number;
  name: string;
  group: {
    id: number;
    name: string;
  };
}

export interface LocalOffice {
  name: string;
  directions: string;
  email: string;
  phone: string;
  latitude: string;
  longitude: string;
  streetAddress: string;
  extendedAddress: string;
  locality: string;
  region: string;
  postalCode: string;
  country: string;
}

export interface Node {
  id: number;
  name: string;
  shortDescription?: string;
  longDescription?: string;
  type: {
    id: number;
    name: string;
  };
  parentId?: number;
  parent?: any;
  directions?: string;
  checkinDetails?: string;
  timezone: string;
  checkinTime: string;
  hasEarlyCheckin: boolean;
  earlyCheckinTime?: string;
  checkoutTime: string;
  hasLateCheckout: boolean;
  lateCheckoutTime?: string;
  website?: string;
  phone?: string;
  streetAddress: string;
  extendedAddress?: string;
  locality: string;
  region: string;
  postal: string;
  country: string;
  latitude: number;
  longitude: number;
  petsFriendly: boolean;
  maxPets?: number;
  eventsAllowed: boolean;
  smokingAllowed: boolean;
  childrenAllowed: boolean;
  minimumAgeLimit?: number;
  isAccessible: boolean;
  area?: number;
  floors?: number;
  maxOccupancy: number;
  securityDeposit: string;
  bedrooms: number;
  fullBathrooms: number;
  threeQuarterBathrooms: number;
  halfBathrooms: number;
  bedTypes: BedType[];
  rooms: Room[];
  amenities: Amenity[];
  amenityDescription: string;
  coverImage: string;
  taxId: number;
  localOffice: LocalOffice;
  regulations: Regulation[];
  updated: {
    availability: string;
    content: string;
    pricing: string;
  };
  updatedAt: string;
  createdAt: string;
  isActive: boolean;
  _links: {
    self: { href: string };
  };
}

export interface Regulation {
  body: string;
  params: string;
}

export interface Unit {
  id: number;
  name: string;
  shortName: string;
  unitCode: string;
  headline?: string;
  shortDescription: string;
  longDescription: string;
  houseRules?: string;
  nodeId: number;
  unitType: UnitType;
  lodgingType: LodgingType;
  directions?: string;
  checkinDetails?: string;
  timezone: string;
  checkinTime: string;
  hasEarlyCheckin: boolean;
  earlyCheckinTime?: string;
  checkoutTime: string;
  hasLateCheckout: boolean;
  lateCheckoutTime?: string;
  minBookingWindow: number;
  maxBookingWindow: number;
  website?: string;
  phone?: string;
  streetAddress: string;
  extendedAddress?: string;
  locality: string;
  region: string;
  postalCode: string;
  country: string;
  longitude: number;
  latitude: number;
  petsFriendly: boolean;
  maxPets: number;
  eventsAllowed: boolean;
  smokingAllowed: boolean;
  childrenAllowed: boolean;
  minimumAgeLimit?: number;
  isAccessible: boolean;
  area?: number;
  floors?: number;
  maxOccupancy: number;
  securityDeposit: string;
  bedrooms: number;
  fullBathrooms: number;
  threeQuarterBathrooms: number;
  halfBathrooms: number;
  bedTypes: BedType[];
  rooms: Room[];
  amenities: Amenity[];
  amenityDescription: string;
  coverImage: string;
  taxId: number;
  localOffice: LocalOffice;
  regulations: Regulation[];
  updated: {
    availability: string;
    content: string;
    pricing: string;
  };
  updatedAt: string;
  createdAt: string;
  isActive: boolean;
  _links: {
    self: { href: string };
  };
}

export interface GetUnitsParams {
  // Paginación
  page?: number;
  size?: number;
  
  // Ordenamiento
  sortColumn?: 'id' | 'name' | 'nodeName' | 'unitTypeName';
  sortDirection?: 'asc' | 'desc';
  
  // Búsqueda
  search?: string;
  term?: string;
  unitCode?: string;
  shortName?: string;
  contentUpdatedSince?: string;
  updatedSince?: string;
  
  // Filtros por ID
  nodeId?: number | number[];
  unitTypeId?: number | number[];
  amenityId?: number | number[];
  
  // Filtros físicos
  bedrooms?: number;
  minBedrooms?: number;
  maxBedrooms?: number;
  bathrooms?: number;
  minBathrooms?: number;
  maxBathrooms?: number;
  
  // Filtros de políticas
  petsFriendly?: 0 | 1;
  eventsAllowed?: 0 | 1;
  smokingAllowed?: 0 | 1;
  childrenAllowed?: 0 | 1;
  
  // Filtros de disponibilidad
  arrival?: string;
  departure?: string;
  
  // Filtros de estado
  isActive?: 0 | 1;
  isBookable?: 0 | 1;
  unitStatus?: 'clean' | 'dirty' | 'occupied' | 'inspection' | 'inprogress';
  
  // Filtros adicionales
  computed?: 0 | 1;
  inherited?: 0 | 1;
  limited?: 0 | 1;
  includeDescriptions?: 0 | 1;
  allowUnitRates?: 0 | 1;
  calendarId?: number;
  roleId?: number;
  id?: number[];
}

export interface GetUnitsResponse {
  _embedded: {
    units: Unit[];
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

export interface UnitFilters {
  nodeId?: number;
  unitTypeId?: number;
  amenityId?: number;
  bedrooms?: number;
  bathrooms?: number;
  petsFriendly?: boolean;
  eventsAllowed?: boolean;
  smokingAllowed?: boolean;
  childrenAllowed?: boolean;
  isActive?: boolean;
  isBookable?: boolean;
  unitStatus?: string;
  arrival?: string;
  departure?: string;
}