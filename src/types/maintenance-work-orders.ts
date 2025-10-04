/**
 * Tipos específicos para el API de Maintenance Work Orders de Track HS
 */

export interface Problem {
  id: number;
  name: string;
}

export interface Assignee {
  id: number;
  name: string;
  email?: string;
}

export interface WorkOrderEmbedded {
  unit?: {
    id: number;
    name: string;
    // ... otros campos de unidad
  };
  vendor?: {
    id: number;
    name: string;
    // ... otros campos de vendor
  };
  owner?: {
    id: number;
    name: string;
    // ... otros campos de owner
  };
}

export interface WorkOrderLinks {
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

export interface MaintenanceWorkOrder {
  id: number;
  dateReceived: string;
  priority: 5 | 3 | 1; // High=5, Medium=3, Low=1
  status: 'open' | 'not-started' | 'in-progress' | 'completed' | 'processed' | 
          'vendor-not-start' | 'vendor-assigned' | 'vendor-declined' | 
          'vendor-completed' | 'user-completed' | 'cancelled';
  assignees?: Assignee[];
  summary: string;
  problems?: Problem[];
  estimatedCost?: number;
  estimatedTime?: number;
  actualTime?: number;
  dateCompleted?: string;
  completedById?: number;
  dateProcessed?: string;
  processedById?: number;
  userId?: number;
  vendorId?: number;
  unitId?: number;
  ownerId?: number;
  reservationId?: number;
  referenceNumber?: string;
  description?: string;
  workPerformed?: string;
  source?: string;
  sourceName?: string;
  sourcePhone?: string;
  blockCheckin?: boolean;
  createdAt: string;
  createdBy: string;
  updatedAt: string;
  updatedBy: string;
  _embedded?: WorkOrderEmbedded;
  _links?: WorkOrderLinks;
}

export interface GetMaintenanceWorkOrdersParams {
  updatedSince?: string;
  page?: number;
  size?: number;
  sortColumn?: 'id' | 'scheduledAt' | 'status' | 'priority' | 'dateReceived' | 
              'unitId' | 'vendorId' | 'userId' | 'summary';
  sortDirection?: 'asc' | 'desc';
  search?: string;
  isScheduled?: 0 | 1;
  unitId?: string;
  userId?: number[];
  nodeId?: number;
  roleId?: number;
  ownerId?: number;
  priority?: number[];
  reservationId?: number;
  vendorId?: number;
  status?: ('open' | 'not-started' | 'in-progress' | 'completed' | 'processed' | 
           'vendor-not-start' | 'vendor-assigned' | 'vendor-declined' | 
           'vendor-completed' | 'user-completed' | 'cancelled')[];
  dateScheduled?: string;
  startDate?: string;
  endDate?: string;
  problems?: number[];
}

export interface MaintenanceWorkOrdersResponse {
  _embedded: {
    workOrders: MaintenanceWorkOrder[];
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
