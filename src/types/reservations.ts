/**
 * Tipos específicos para el API de Reservations de Track HS
 */

export interface Guest {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  nationality?: string;
  documentType?: string;
  documentNumber?: string;
}

export interface Property {
  id: number;
  name: string;
  address: string;
  city: string;
  country: string;
  propertyType: string;
  bedrooms: number;
  bathrooms: number;
  maxGuests: number;
}

export interface Reservation {
  id: number;
  alternates?: string[];
  currency: string;
  unitId: number;
  isUnitLocked: boolean;
  isUnitAssigned: boolean;
  isUnitTypeLocked: boolean;
  unitTypeId: number;
  arrivalDate: string;
  departureDate: string;
  earlyArrival: boolean;
  lateDeparture: boolean;
  arrivalTime: string;
  departureTime: string;
  nights: number;
  status: 'Hold' | 'Confirmed' | 'Checked Out' | 'Checked In' | 'Cancelled';
  cancelledAt?: string;
  occupants: Occupant[];
  securityDeposit: {
    required: string;
  };
  updatedAt: string;
  createdAt: string;
  bookedAt: string;
  guestBreakdown: GuestBreakdown;
  type: {
    id: number;
    name: string;
  };
  guaranteePolicy: GuaranteePolicy;
  cancellationPolicy: CancellationPolicy;
  paymentPlan: PaymentPlan[];
  rateType: {
    id: number;
    name: string;
    code: string;
  };
  travelInsuranceProducts: TravelInsuranceProduct[];
  _embedded: {
    unit: Unit;
    contact: Contact;
  };
  _links: {
    self: { href: string };
    cancel: { href: string };
  };
}

export interface Occupant {
  typeId: number;
  name: string;
  handle: string;
  quantity: number;
  included: boolean;
  extraQuantity: number;
  ratePerPersonPerStay: string;
  ratePerStay: string;
}

export interface GuestBreakdown {
  grossRent: string;
  guestGrossDisplayRent: string;
  discount: string;
  promoValue: string;
  discountTotal: number;
  netRent: string;
  guestNetDisplayRent: string;
  actualAdr: string;
  guestAdr: string;
  totalGuestFees: string;
  totalRentFees: string;
  totalItemizedFees: string;
  totalTaxFees: string;
  totalServiceFees: string;
  folioCharges: string;
  subtotal: string;
  guestSubtotal: string;
  totalTaxes: string;
  totalGuestTaxes: string;
  total: string;
  grandTotal: string;
  netPayments: string;
  payments: string;
  refunds: string;
  netTransfers: string;
  balance: string;
  rates: Rate[];
  guestFees: GuestFee[];
  taxes: Tax[];
}

export interface Rate {
  date: string;
  rate: string;
  nights: number;
  isQuoted: boolean;
}

export interface GuestFee {
  id: string;
  name: string;
  displayAs: 'itemize' | 'rent' | 'tax' | 'service';
  quantity: string;
  unitValue: string;
  value: string;
}

export interface Tax {
  id: number;
  name: string;
  amount: string;
}

export interface GuaranteePolicy {
  id: number;
  name: string;
  type: 'Hold' | 'Guarantee' | 'FullDeposit';
  hold: {
    limit: number;
  };
}

export interface CancellationPolicy {
  id: number;
  name: string;
  time: string;
  timezone: string;
  breakpoints: CancellationBreakpoint[];
}

export interface CancellationBreakpoint {
  start: number;
  end: number;
  nonRefundable: boolean;
  nonCancelable: boolean;
  penaltyNights: number;
  penaltyPercent: string;
  penaltyFlat: string;
  description: string;
}

export interface PaymentPlan {
  date: string;
  amount: string;
}

export interface TravelInsuranceProduct {
  id: number;
  status: 'optin' | 'funded' | 'cancelled';
  type: 'Travel Insurance' | 'Master Cancel' | 'Damage Deposit';
  provider: string;
  providerId: number;
  amount: string;
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
  unitType: {
    id: number;
    name: string;
  };
  lodgingType: {
    id: number;
    name: string;
  };
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

export interface BedType {
  id: number;
  name: string;
  count: number;
}

export interface Room {
  name: string;
  type: string;
  sleeps: number;
  description: string;
  hasAttachedBathroom: boolean;
  order?: number;
  airbnbType: string;
  marriottType: string;
  homeawayType: string;
  bedTypes: RoomBedType[];
}

export interface RoomBedType {
  id: number;
  name: string;
  count: number;
  airbnbType: string;
  marriottType: string;
  homeawayType: string;
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

export interface Regulation {
  body: string;
  params: string;
}

export interface Contact {
  id: number;
  firstName: string;
  lastName: string;
  name: string;
  primaryEmail: string;
  secondaryEmail?: string;
  homePhone?: string;
  cellPhone?: string;
  workPhone?: string;
  otherPhone?: string;
  fax?: string;
  streetAddress?: string;
  extendedAddress?: string;
  locality?: string;
  region?: string;
  postalCode?: string;
  country: string;
  notes?: string;
  anniversary?: string;
  birthdate?: string;
  noIdentity?: boolean;
  isVip?: boolean;
  isBlacklist?: boolean;
  isDNR?: boolean;
  tags: Tag[];
  references: Reference[];
  custom: Record<string, any>;
  updatedBy: string;
  createdBy: string;
  updatedAt: string;
  createdAt: string;
  isOwnerContact: boolean;
  _links: {
    self: { href: string };
  };
}

export interface Tag {
  id: number;
}

export interface Reference {
  reference: string;
  salesLinkId?: number;
  channelId?: number;
}

// Tipos para búsqueda de reservaciones
export interface SearchReservationsParams {
  // Paginación
  page?: number;
  size?: number;
  scroll?: number | string;
  
  // Ordenamiento
  sortColumn?: 'name' | 'status' | 'altConf' | 'agreementStatus' | 'type' | 'guest' | 'guests' | 'unit' | 'units' | 'checkin' | 'checkout' | 'nights';
  sortDirection?: 'asc' | 'desc';
  
  // Búsqueda
  search?: string;
  tags?: string;
  updatedSince?: string;
  
  // Filtros por ID
  nodeId?: number | number[];
  unitId?: number | number[];
  reservationTypeId?: number | number[];
  contactId?: number | number[];
  travelAgentId?: number | number[];
  campaignId?: number | number[];
  userId?: number | number[];
  unitTypeId?: number | number[];
  rateTypeId?: number | number[];
  
  // Filtros por fechas
  bookedStart?: string;
  bookedEnd?: string;
  arrivalStart?: string;
  arrivalEnd?: string;
  departureStart?: string;
  departureEnd?: string;
  
  // Filtros especiales
  inHouseToday?: 0 | 1;
  status?: 'Hold' | 'Confirmed' | 'Checked Out' | 'Checked In' | 'Cancelled' | string[];
}

export interface SearchReservationsResponse {
  _embedded: {
    reservations: Reservation[];
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

export interface ReservationResponse {
  data: Reservation;
  success: boolean;
  message?: string;
}

export interface ReservationFilters {
  status?: 'Hold' | 'Confirmed' | 'Checked Out' | 'Checked In' | 'Cancelled';
  channel?: string;
  propertyId?: string;
  dateFrom?: string;
  dateTo?: string;
  guestEmail?: string;
  bookingReference?: string;
}
