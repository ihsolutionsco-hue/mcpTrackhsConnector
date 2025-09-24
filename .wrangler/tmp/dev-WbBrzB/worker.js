var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// .wrangler/tmp/bundle-jwNSZb/checked-fetch.js
var urls = /* @__PURE__ */ new Set();
function checkURL(request, init) {
  const url = request instanceof URL ? request : new URL(
    (typeof request === "string" ? new Request(request, init) : request).url
  );
  if (url.port && url.port !== "443" && url.protocol === "https:") {
    if (!urls.has(url.toString())) {
      urls.add(url.toString());
      console.warn(
        `WARNING: known issue with \`fetch()\` requests to custom HTTPS ports in published Workers:
 - ${url.toString()} - the custom port will be ignored when the Worker is published using the \`wrangler deploy\` command.
`
      );
    }
  }
}
__name(checkURL, "checkURL");
globalThis.fetch = new Proxy(globalThis.fetch, {
  apply(target, thisArg, argArray) {
    const [request, init] = argArray;
    checkURL(request, init);
    return Reflect.apply(target, thisArg, argArray);
  }
});

// src/core/auth.ts
var TrackHSAuth = class {
  static {
    __name(this, "TrackHSAuth");
  }
  credentials;
  constructor(config) {
    this.credentials = btoa(`${config.username}:${config.password}`);
  }
  /**
   * Genera el header de autorización para las peticiones
   */
  getAuthHeader() {
    return `Basic ${this.credentials}`;
  }
  /**
   * Valida que las credenciales estén configuradas
   */
  validateCredentials() {
    return this.credentials.length > 0;
  }
};

// src/core/api-client.ts
var TrackHSApiClient = class {
  static {
    __name(this, "TrackHSApiClient");
  }
  baseUrl;
  auth;
  constructor(config) {
    this.baseUrl = config.baseUrl;
    this.auth = new TrackHSAuth(config);
    if (!this.auth.validateCredentials()) {
      throw new Error("Credenciales de Track HS no configuradas correctamente");
    }
  }
  /**
   * Realiza una petición HTTP a la API de Track HS
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    try {
      const fetchOptions = {
        method: options.method || "GET",
        headers: {
          "Authorization": this.auth.getAuthHeader(),
          "Content-Type": "application/json",
          "Accept": "application/json",
          ...options.headers
        }
      };
      if (options.body) {
        fetchOptions.body = options.body;
      }
      const response = await fetch(url, fetchOptions);
      if (!response.ok) {
        const errorMessage = `Track HS API Error: ${response.status} ${response.statusText}`;
        throw new Error(errorMessage);
      }
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        return await response.json();
      } else {
        return await response.text();
      }
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Error en petici\xF3n a Track HS: ${error.message}`);
      }
      throw new Error("Error desconocido en petici\xF3n a Track HS");
    }
  }
  /**
   * Realiza una petición GET
   */
  async get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "GET" });
  }
  /**
   * Realiza una petición POST
   */
  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: data ? JSON.stringify(data) : void 0
    });
  }
};

// src/core/base-tool.ts
var BaseTrackHSTool = class {
  static {
    __name(this, "BaseTrackHSTool");
  }
  apiClient;
  constructor(apiClient) {
    this.apiClient = apiClient;
  }
  /**
   * Valida los parámetros de entrada según el schema
   */
  validateParams(params) {
    const schema = this.inputSchema;
    if (schema.required) {
      for (const requiredProp of schema.required) {
        if (!(requiredProp in params)) {
          throw new Error(`Par\xE1metro requerido faltante: ${requiredProp}`);
        }
      }
    }
    for (const [prop, propSchema] of Object.entries(schema.properties)) {
      if (prop in params) {
        const value = params[prop];
        const expectedType = propSchema.type;
        if (expectedType === "string" && typeof value !== "string") {
          throw new Error(`Par\xE1metro '${prop}' debe ser string`);
        }
        if (expectedType === "number" && typeof value !== "number") {
          throw new Error(`Par\xE1metro '${prop}' debe ser number`);
        }
        if (expectedType === "boolean" && typeof value !== "boolean") {
          throw new Error(`Par\xE1metro '${prop}' debe ser boolean`);
        }
      }
    }
    return true;
  }
};

// src/tools/get-reviews.ts
var GetReviewsTool = class extends BaseTrackHSTool {
  static {
    __name(this, "GetReviewsTool");
  }
  name = "get_reviews";
  description = "Retrieve paginated collection of property reviews from Track HS";
  inputSchema = {
    type: "object",
    properties: {
      page: {
        type: "number",
        description: "Page Number (default: 1)",
        minimum: 1
      },
      size: {
        type: "number",
        description: "Page Size (default: 10, max: 100)",
        minimum: 1,
        maximum: 100
      },
      sortColumn: {
        type: "string",
        enum: ["id"],
        default: "id",
        description: "Column to sort by"
      },
      sortDirection: {
        type: "string",
        enum: ["asc", "desc"],
        default: "asc",
        description: "Sort direction"
      },
      search: {
        type: "string",
        description: "Search by reviewId and publicReview content"
      },
      updatedSince: {
        type: "string",
        format: "date-time",
        description: "Filter reviews updated since this date (ISO 8601 format)"
      }
    },
    required: []
  };
  async execute(params = {}) {
    this.validateParams(params);
    const queryParams = new URLSearchParams();
    const page = params.page || 1;
    const size = params.size || 10;
    const sortColumn = params.sortColumn || "id";
    const sortDirection = params.sortDirection || "asc";
    queryParams.append("page", page.toString());
    queryParams.append("size", size.toString());
    queryParams.append("sortColumn", sortColumn);
    queryParams.append("sortDirection", sortDirection);
    if (params.search) {
      queryParams.append("search", params.search);
    }
    if (params.updatedSince) {
      queryParams.append("updatedSince", params.updatedSince);
    }
    const endpoint = `/channel-management/channel/reviews?${queryParams.toString()}`;
    try {
      const result = await this.apiClient.get(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener rese\xF1as: ${error instanceof Error ? error.message : "Error desconocido"}`);
    }
  }
};

// src/tools/get-reservation.ts
var GetReservationTool = class extends BaseTrackHSTool {
  static {
    __name(this, "GetReservationTool");
  }
  name = "get_reservation";
  description = "Get detailed information for a specific reservation by ID";
  inputSchema = {
    type: "object",
    properties: {
      reservationId: {
        type: "string",
        description: "The ID of the reservation to retrieve"
      }
    },
    required: ["reservationId"]
  };
  async execute(params) {
    this.validateParams(params);
    const { reservationId } = params;
    if (!reservationId || reservationId.trim() === "") {
      throw new Error("El ID de reservaci\xF3n no puede estar vac\xEDo");
    }
    const endpoint = `/v2/pms/reservations/${encodeURIComponent(reservationId)}`;
    try {
      const result = await this.apiClient.get(endpoint);
      return result;
    } catch (error) {
      if (error instanceof Error && error.message.includes("404")) {
        throw new Error(`Reservaci\xF3n con ID '${reservationId}' no encontrada`);
      }
      throw new Error(`Error al obtener reservaci\xF3n: ${error instanceof Error ? error.message : "Error desconocido"}`);
    }
  }
};

// src/tools/search-reservations.ts
var SearchReservationsTool = class extends BaseTrackHSTool {
  static {
    __name(this, "SearchReservationsTool");
  }
  name = "search_reservations";
  description = "Search reservations with advanced filtering options including pagination, sorting, date ranges, and multiple ID filters";
  inputSchema = {
    type: "object",
    properties: {
      // Paginación
      page: {
        type: "number",
        minimum: 0,
        description: "Page number of result set - Limited to 10k total results (page * size)"
      },
      size: {
        type: "number",
        minimum: 1,
        maximum: 100,
        description: "Size of page - Limited to 10k total results (page * size)"
      },
      scroll: {
        oneOf: [
          { type: "number", description: "Default to 1 for first page" },
          { type: "string", description: "Use scroll index string for subsequent pages" }
        ],
        description: "Elasticsearch scrolling, start with 1 and then string to continue scrolling"
      },
      // Ordenamiento
      sortColumn: {
        type: "string",
        enum: ["name", "status", "altConf", "agreementStatus", "type", "guest", "guests", "unit", "units", "checkin", "checkout", "nights"],
        default: "name",
        description: "Column to sort the result set"
      },
      sortDirection: {
        type: "string",
        enum: ["asc", "desc"],
        default: "asc",
        description: "Direction to sort result set"
      },
      // Búsqueda
      search: {
        type: "string",
        description: "Substring search matching on name or descriptions"
      },
      tags: {
        type: "string",
        description: "Search matching on tag Id"
      },
      updatedSince: {
        type: "string",
        format: "date-time",
        description: "Date as ISO 8601 format"
      },
      // Filtros por ID (soportan single value o array)
      nodeId: {
        oneOf: [
          { type: "number", title: "Single Node" },
          { type: "array", items: { type: "number" }, title: "Multiple Nodes" }
        ],
        description: "Return all reservations that are of the specific node ID(s). Can be single value or array."
      },
      unitId: {
        oneOf: [
          { type: "number", title: "Single Unit" },
          { type: "array", items: { type: "number" }, title: "Multiple Units" }
        ],
        description: "Return all reservations that are of the specific unit ID(s). Can be single value or array."
      },
      reservationTypeId: {
        oneOf: [
          { type: "number", title: "Single Reservation Type ID" },
          { type: "array", items: { type: "number" }, title: "Multiple Reservation Type IDs" }
        ],
        description: "Return all reservations that are of the specific reservation type ID(s). Can be single value or array."
      },
      contactId: {
        oneOf: [
          { type: "number", title: "Single Contact ID" },
          { type: "array", items: { type: "number" }, title: "Multiple Contact IDs" }
        ],
        description: "Return all reservations that are of the specific contact ID(s). Can be single value or array."
      },
      travelAgentId: {
        oneOf: [
          { type: "number", title: "Single Travel Agent ID" },
          { type: "array", items: { type: "number" }, title: "Multiple Travel Agent IDs" }
        ],
        description: "Return all reservations that are of the specific travel agent ID(s). Can be single value or array."
      },
      campaignId: {
        oneOf: [
          { type: "number", title: "Single Campaign ID" },
          { type: "array", items: { type: "number" }, title: "Multiple Campaign IDs" }
        ],
        description: "Return all reservations that are of the specific campaign ID(s). Can be single value or array."
      },
      userId: {
        oneOf: [
          { type: "number", title: "Single User ID" },
          { type: "array", items: { type: "number" }, title: "Multiple User IDs" }
        ],
        description: "Return all reservations that are of the specific user ID(s). Can be single value or array."
      },
      unitTypeId: {
        oneOf: [
          { type: "number", title: "Single Unit Type ID" },
          { type: "array", items: { type: "number" }, title: "Multiple Unit Type IDs" }
        ],
        description: "Return all reservations that are of the specific unit type ID(s). Can be single value or array."
      },
      rateTypeId: {
        oneOf: [
          { type: "number", title: "Single Rate Type ID" },
          { type: "array", items: { type: "number" }, title: "Multiple Rate Type IDs" }
        ],
        description: "Return all reservations that are of the specific rate type ID(s). Can be single value or array."
      },
      // Filtros por fechas
      bookedStart: {
        type: "string",
        format: "date-time",
        description: "Date as ISO 8601 format"
      },
      bookedEnd: {
        type: "string",
        format: "date-time",
        description: "Date as ISO 8601 format"
      },
      arrivalStart: {
        type: "string",
        format: "date-time",
        description: "Date as ISO 8601 format"
      },
      arrivalEnd: {
        type: "string",
        format: "date-time",
        description: "Date as ISO 8601 format"
      },
      departureStart: {
        type: "string",
        format: "date-time",
        description: "Date as ISO 8601 format"
      },
      departureEnd: {
        type: "string",
        format: "date-time",
        description: "Date as ISO 8601 format"
      },
      // Filtros especiales
      inHouseToday: {
        type: "number",
        enum: [0, 1],
        description: "Filter by in house today"
      },
      status: {
        oneOf: [
          { type: "string", title: "Single Status" },
          { type: "array", items: { type: "string" }, title: "Multiple Statuses" }
        ],
        description: "Return all reservations that are of the specific status(es). Can be single value or array. {Hold, Confirmed, Checked Out, Checked In, and Cancelled}"
      }
    },
    required: []
  };
  async execute(params = {}) {
    this.validateParams(params);
    const queryParams = new URLSearchParams();
    if (params.page !== void 0) {
      queryParams.append("page", params.page.toString());
    }
    if (params.size !== void 0) {
      queryParams.append("size", params.size.toString());
    }
    if (params.sortColumn) {
      queryParams.append("sortColumn", params.sortColumn);
    }
    if (params.sortDirection) {
      queryParams.append("sortDirection", params.sortDirection);
    }
    if (params.search) {
      queryParams.append("search", params.search);
    }
    if (params.tags) {
      queryParams.append("tags", params.tags);
    }
    if (params.updatedSince) {
      queryParams.append("updatedSince", params.updatedSince);
    }
    this.addIdFilter(queryParams, "nodeId", params.nodeId);
    this.addIdFilter(queryParams, "unitId", params.unitId);
    this.addIdFilter(queryParams, "reservationTypeId", params.reservationTypeId);
    this.addIdFilter(queryParams, "contactId", params.contactId);
    this.addIdFilter(queryParams, "travelAgentId", params.travelAgentId);
    this.addIdFilter(queryParams, "campaignId", params.campaignId);
    this.addIdFilter(queryParams, "userId", params.userId);
    this.addIdFilter(queryParams, "unitTypeId", params.unitTypeId);
    this.addIdFilter(queryParams, "rateTypeId", params.rateTypeId);
    if (params.bookedStart) {
      queryParams.append("bookedStart", params.bookedStart);
    }
    if (params.bookedEnd) {
      queryParams.append("bookedEnd", params.bookedEnd);
    }
    if (params.arrivalStart) {
      queryParams.append("arrivalStart", params.arrivalStart);
    }
    if (params.arrivalEnd) {
      queryParams.append("arrivalEnd", params.arrivalEnd);
    }
    if (params.departureStart) {
      queryParams.append("departureStart", params.departureStart);
    }
    if (params.departureEnd) {
      queryParams.append("departureEnd", params.departureEnd);
    }
    if (params.inHouseToday !== void 0) {
      queryParams.append("inHouseToday", params.inHouseToday.toString());
    }
    if (params.status !== void 0) {
      this.addStatusFilter(queryParams, params.status);
    }
    const endpoint = `/v2/pms/reservations?${queryParams.toString()}`;
    try {
      const result = await this.apiClient.get(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al buscar reservaciones: ${error instanceof Error ? error.message : "Error desconocido"}`);
    }
  }
  /**
   * Agrega filtros de ID a los query parameters, manejando tanto valores únicos como arrays
   */
  addIdFilter(queryParams, paramName, value) {
    if (value !== void 0) {
      if (Array.isArray(value)) {
        value.forEach((id) => queryParams.append(paramName, id.toString()));
      } else {
        queryParams.append(paramName, value.toString());
      }
    }
  }
  /**
   * Agrega filtros de estado a los query parameters, manejando tanto valores únicos como arrays
   */
  addStatusFilter(queryParams, status) {
    if (status !== void 0) {
      if (Array.isArray(status)) {
        status.forEach((s) => queryParams.append("status", s));
      } else {
        queryParams.append("status", status);
      }
    }
  }
};

// src/tools/get-units.ts
var GetUnitsTool = class extends BaseTrackHSTool {
  static {
    __name(this, "GetUnitsTool");
  }
  name = "get_units";
  description = "Obtener colecci\xF3n de unidades de alojamiento con filtros avanzados incluyendo paginaci\xF3n, ordenamiento, filtros por ID, b\xFAsqueda de texto, filtros f\xEDsicos, pol\xEDticas y disponibilidad";
  inputSchema = {
    type: "object",
    properties: {
      // Paginación
      page: {
        type: "number",
        minimum: 0,
        description: "Page number of result set - Limited to 10k total results (page * size)"
      },
      size: {
        type: "number",
        minimum: 1,
        maximum: 100,
        description: "Size of page - Limited to 10k total results (page * size)"
      },
      // Ordenamiento
      sortColumn: {
        type: "string",
        enum: ["id", "name", "nodeName", "unitTypeName"],
        default: "name",
        description: "Column to sort the result set"
      },
      sortDirection: {
        type: "string",
        enum: ["asc", "desc"],
        default: "asc",
        description: "Direction to sort result set"
      },
      // Búsqueda
      search: {
        type: "string",
        description: "Substring search matching on name or descriptions"
      },
      term: {
        type: "string",
        description: "Substring search matching on term"
      },
      unitCode: {
        type: "string",
        description: "Search on unitCode, exact match or add % for wildcard"
      },
      shortName: {
        type: "string",
        description: "Search on shortName, exact match or add % for wildcard"
      },
      contentUpdatedSince: {
        type: "string",
        format: "date-time",
        description: "Date in ISO 8601 format. Will return all units with content changes since timestamp"
      },
      updatedSince: {
        type: "string",
        format: "date",
        description: "Date in ISO 8601 format. Will return all units updated since timestamp. @deprecated use contentUpdatedSince"
      },
      // Filtros por ID (soportan single value o array)
      nodeId: {
        oneOf: [
          { type: "number", title: "Single Node" },
          { type: "array", items: { type: "number" }, title: "Multiple Nodes" }
        ],
        description: "Return all units that are descendants of the specific node ID(s). Can be single value or array."
      },
      unitTypeId: {
        oneOf: [
          { type: "number", title: "Single Unit Type" },
          { type: "array", items: { type: "number" }, title: "Multiple Unit Types" }
        ],
        description: "Return all units of the specific unit type(s). Can be single value or array."
      },
      amenityId: {
        oneOf: [
          { type: "number", title: "Single Amenity" },
          { type: "array", items: { type: "number" }, title: "Multiple Amenities" }
        ],
        description: "Return all units that have these amenity ID(s). Can be single value or array."
      },
      // Filtros físicos
      bedrooms: {
        type: "number",
        description: "Return all units with this exact number of bedrooms"
      },
      minBedrooms: {
        type: "number",
        description: "Return all units with this or more number of bedrooms"
      },
      maxBedrooms: {
        type: "number",
        description: "Return all units with this or less number of bedrooms"
      },
      bathrooms: {
        type: "number",
        description: "Return all units with this exact number of bathrooms"
      },
      minBathrooms: {
        type: "number",
        description: "Return all units with this or more number of bathrooms"
      },
      maxBathrooms: {
        type: "number",
        description: "Return all units with this or less number of bathrooms"
      },
      // Filtros de políticas
      petsFriendly: {
        type: "number",
        enum: [0, 1],
        description: "Return all units that are pet friendly (1) or not (0)"
      },
      eventsAllowed: {
        type: "number",
        enum: [0, 1],
        description: "Return all units that allow events (1) or not (0)"
      },
      smokingAllowed: {
        type: "number",
        enum: [0, 1],
        description: "Return all units that allow smoking (1) or not (0)"
      },
      childrenAllowed: {
        type: "number",
        enum: [0, 1],
        description: "Return all units that allow children (1) or not (0)"
      },
      // Filtros de disponibilidad
      arrival: {
        type: "string",
        format: "date",
        description: "Date in ISO 8601 format. Will return all units available between this and departure"
      },
      departure: {
        type: "string",
        format: "date",
        description: "Date in ISO 8601 format. Will return all units available between this and arrival"
      },
      // Filtros de estado
      isActive: {
        type: "number",
        enum: [0, 1],
        description: "Return active (1), inactive (0), or all (null) units"
      },
      isBookable: {
        type: "number",
        enum: [0, 1],
        description: "Return all bookable units (1) or not (0)"
      },
      unitStatus: {
        type: "string",
        enum: ["clean", "dirty", "occupied", "inspection", "inprogress"],
        description: "Filter by unit status"
      },
      // Filtros adicionales
      computed: {
        type: "number",
        enum: [0, 1],
        description: "Return additional computed values attributes based on inherited attributes. 1 == true, 0 == false"
      },
      inherited: {
        type: "number",
        enum: [0, 1],
        description: "Return additional inherited attributes. 1 == true, 0 == false"
      },
      limited: {
        type: "number",
        enum: [0, 1],
        description: "Return very limited attributes (id, name, longitude latitude, isActive)"
      },
      includeDescriptions: {
        type: "number",
        enum: [0, 1],
        description: "Return descriptions of units, may be inherited from node if set to inherited. 1 == true, 0 == false"
      },
      allowUnitRates: {
        type: "number",
        enum: [0, 1],
        description: "Return all units who's type allows unit rates"
      },
      calendarId: {
        type: "number",
        description: "Return all units matching this unit's type with calendar group id"
      },
      roleId: {
        type: "number",
        description: "Return units by is a specific roleId is being used"
      },
      id: {
        type: "array",
        items: { type: "number" },
        description: "Filter by Unit IDs"
      }
    },
    required: []
  };
  async execute(params = {}) {
    this.validateParams(params);
    const queryParams = new URLSearchParams();
    if (params.page !== void 0) {
      queryParams.append("page", params.page.toString());
    }
    if (params.size !== void 0) {
      queryParams.append("size", params.size.toString());
    }
    if (params.sortColumn) {
      queryParams.append("sortColumn", params.sortColumn);
    }
    if (params.sortDirection) {
      queryParams.append("sortDirection", params.sortDirection);
    }
    if (params.search) {
      queryParams.append("search", params.search);
    }
    if (params.term) {
      queryParams.append("term", params.term);
    }
    if (params.unitCode) {
      queryParams.append("unitCode", params.unitCode);
    }
    if (params.shortName) {
      queryParams.append("shortName", params.shortName);
    }
    if (params.contentUpdatedSince) {
      queryParams.append("contentUpdatedSince", params.contentUpdatedSince);
    }
    if (params.updatedSince) {
      queryParams.append("updatedSince", params.updatedSince);
    }
    this.addIdFilter(queryParams, "nodeId", params.nodeId);
    this.addIdFilter(queryParams, "unitTypeId", params.unitTypeId);
    this.addIdFilter(queryParams, "amenityId", params.amenityId);
    if (params.bedrooms !== void 0) {
      queryParams.append("bedrooms", params.bedrooms.toString());
    }
    if (params.minBedrooms !== void 0) {
      queryParams.append("minBedrooms", params.minBedrooms.toString());
    }
    if (params.maxBedrooms !== void 0) {
      queryParams.append("maxBedrooms", params.maxBedrooms.toString());
    }
    if (params.bathrooms !== void 0) {
      queryParams.append("bathrooms", params.bathrooms.toString());
    }
    if (params.minBathrooms !== void 0) {
      queryParams.append("minBathrooms", params.minBathrooms.toString());
    }
    if (params.maxBathrooms !== void 0) {
      queryParams.append("maxBathrooms", params.maxBathrooms.toString());
    }
    if (params.petsFriendly !== void 0) {
      queryParams.append("petsFriendly", params.petsFriendly.toString());
    }
    if (params.eventsAllowed !== void 0) {
      queryParams.append("eventsAllowed", params.eventsAllowed.toString());
    }
    if (params.smokingAllowed !== void 0) {
      queryParams.append("smokingAllowed", params.smokingAllowed.toString());
    }
    if (params.childrenAllowed !== void 0) {
      queryParams.append("childrenAllowed", params.childrenAllowed.toString());
    }
    if (params.arrival) {
      queryParams.append("arrival", params.arrival);
    }
    if (params.departure) {
      queryParams.append("departure", params.departure);
    }
    if (params.isActive !== void 0) {
      queryParams.append("isActive", params.isActive.toString());
    }
    if (params.isBookable !== void 0) {
      queryParams.append("isBookable", params.isBookable.toString());
    }
    if (params.unitStatus) {
      queryParams.append("unitStatus", params.unitStatus);
    }
    if (params.computed !== void 0) {
      queryParams.append("computed", params.computed.toString());
    }
    if (params.inherited !== void 0) {
      queryParams.append("inherited", params.inherited.toString());
    }
    if (params.limited !== void 0) {
      queryParams.append("limited", params.limited.toString());
    }
    if (params.includeDescriptions !== void 0) {
      queryParams.append("includeDescriptions", params.includeDescriptions.toString());
    }
    if (params.allowUnitRates !== void 0) {
      queryParams.append("allowUnitRates", params.allowUnitRates.toString());
    }
    if (params.calendarId !== void 0) {
      queryParams.append("calendarId", params.calendarId.toString());
    }
    if (params.roleId !== void 0) {
      queryParams.append("roleId", params.roleId.toString());
    }
    if (params.id !== void 0) {
      this.addIdFilter(queryParams, "id", params.id);
    }
    const endpoint = `/pms/units?${queryParams.toString()}`;
    try {
      const result = await this.apiClient.get(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener unidades: ${error instanceof Error ? error.message : "Error desconocido"}`);
    }
  }
  /**
   * Agrega filtros de ID a los query parameters, manejando tanto valores únicos como arrays
   */
  addIdFilter(queryParams, paramName, value) {
    if (value !== void 0) {
      if (Array.isArray(value)) {
        value.forEach((id) => queryParams.append(paramName, id.toString()));
      } else {
        queryParams.append(paramName, value.toString());
      }
    }
  }
};

// src/tools/get-folios-collection.ts
var GetFoliosCollectionTool = class extends BaseTrackHSTool {
  static {
    __name(this, "GetFoliosCollectionTool");
  }
  name = "get_folios_collection";
  description = "Get a collection of folios (bills/receipts) with filtering, pagination, and sorting options";
  inputSchema = {
    type: "object",
    properties: {
      // Paginación
      page: {
        type: "number",
        minimum: 1,
        description: "Page number of result set"
      },
      size: {
        type: "number",
        minimum: 1,
        maximum: 100,
        description: "Page size - maximum 100 items per page"
      },
      // Ordenamiento
      sortColumn: {
        type: "string",
        enum: ["id", "name", "status", "type", "startDate", "endDate", "contactName", "companyName", "reservationId", "currentBalance", "realizedBalance", "masterFolioRule"],
        default: "id",
        description: "Column to sort the result set"
      },
      sortDirection: {
        type: "string",
        enum: ["asc", "desc"],
        default: "asc",
        description: "Direction to sort result set"
      },
      // Búsqueda
      search: {
        type: "string",
        description: "Search folios by id, name, company name, contact name, reservation id, unit id or unit name"
      },
      // Filtros por tipo
      type: {
        type: "string",
        enum: ["guest", "master", "guest-sub-folio", "master-sub-folio"],
        description: "Limit results to certain folio types"
      },
      status: {
        type: "string",
        enum: ["open", "closed"],
        description: "Search folios by their status"
      },
      // Filtros por ID
      masterFolioId: {
        type: "number",
        minimum: 1,
        description: "Search folios by master Folio Id - if type = guest"
      },
      contactId: {
        type: "number",
        minimum: 1,
        description: "Search folios by guest id"
      },
      companyId: {
        type: "number",
        minimum: 1,
        description: "Search folios by company id"
      }
    },
    required: []
  };
  async execute(params = {}) {
    this.validateParams(params);
    const queryParams = new URLSearchParams();
    if (params.page !== void 0) {
      queryParams.append("page", params.page.toString());
    }
    if (params.size !== void 0) {
      queryParams.append("size", params.size.toString());
    }
    if (params.sortColumn) {
      queryParams.append("sortColumn", params.sortColumn);
    }
    if (params.sortDirection) {
      queryParams.append("sortDirection", params.sortDirection);
    }
    if (params.search) {
      queryParams.append("search", params.search);
    }
    if (params.type) {
      queryParams.append("type", params.type);
    }
    if (params.status) {
      queryParams.append("status", params.status);
    }
    if (params.masterFolioId !== void 0) {
      queryParams.append("masterFolioId", params.masterFolioId.toString());
    }
    if (params.contactId !== void 0) {
      queryParams.append("contactId", params.contactId.toString());
    }
    if (params.companyId !== void 0) {
      queryParams.append("companyId", params.companyId.toString());
    }
    const endpoint = `/pms/folios?${queryParams.toString()}`;
    try {
      const result = await this.apiClient.get(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener folios: ${error instanceof Error ? error.message : "Error desconocido"}`);
    }
  }
};

// src/tools/get-contacts.ts
var GetContactsTool = class extends BaseTrackHSTool {
  static {
    __name(this, "GetContactsTool");
  }
  name = "get_contacts";
  description = "Retrieve all contacts from Track HS CRM system. Contacts include guests, owners, or vendor employees.";
  inputSchema = {
    type: "object",
    properties: {
      sortColumn: {
        type: "string",
        enum: ["id", "name", "email", "cellPhone", "homePhone", "otherPhone", "vip"],
        description: "Sort by id, name, email, mobile phone, home phone, other phone, vip"
      },
      sortDirection: {
        type: "string",
        enum: ["asc", "desc"],
        default: "asc",
        description: "Sort ascending or descending"
      },
      search: {
        type: "string",
        description: "Search by first name, last name, email, mobile phone, home phone, other phone with right side wildcard"
      },
      term: {
        type: "string",
        description: "Locate contact based on a precise value such as ID or name"
      },
      email: {
        type: "string",
        format: "email",
        description: "Search contact by primary or secondary email address"
      },
      page: {
        type: "number",
        description: "Page Number",
        minimum: 1
      },
      size: {
        type: "number",
        description: "Page Size",
        minimum: 1,
        maximum: 100
      },
      updatedSince: {
        type: "string",
        format: "date-time",
        description: "Date in ISO 8601 format. Will return all contacts updated since timestamp"
      }
    },
    required: []
  };
  async execute(params = {}) {
    this.validateParams(params);
    const queryParams = new URLSearchParams();
    const sortDirection = params.sortDirection || "asc";
    if (params.sortColumn) {
      queryParams.append("sortColumn", params.sortColumn);
    }
    queryParams.append("sortDirection", sortDirection);
    if (params.search) {
      queryParams.append("search", params.search);
    }
    if (params.term) {
      queryParams.append("term", params.term);
    }
    if (params.email) {
      queryParams.append("email", params.email);
    }
    if (params.page) {
      queryParams.append("page", params.page.toString());
    }
    if (params.size) {
      queryParams.append("size", params.size.toString());
    }
    if (params.updatedSince) {
      queryParams.append("updatedSince", params.updatedSince);
    }
    const endpoint = `/crm/contacts?${queryParams.toString()}`;
    try {
      const result = await this.apiClient.get(endpoint);
      return result;
    } catch (error) {
      throw new Error(`Error al obtener contactos: ${error instanceof Error ? error.message : "Error desconocido"}`);
    }
  }
};

// src/core/simple-mcp-server.ts
var SimpleTrackHSMCPServer = class {
  constructor(env) {
    this.env = env;
    this.validateEnvironment();
    this.apiClient = new TrackHSApiClient({
      baseUrl: this.env.TRACKHS_API_URL,
      username: this.env.TRACKHS_USERNAME,
      password: this.env.TRACKHS_PASSWORD
    });
    this.tools = [
      new GetReviewsTool(this.apiClient),
      new GetReservationTool(this.apiClient),
      new SearchReservationsTool(this.apiClient),
      new GetUnitsTool(this.apiClient),
      new GetFoliosCollectionTool(this.apiClient),
      new GetContactsTool(this.apiClient)
    ];
  }
  static {
    __name(this, "SimpleTrackHSMCPServer");
  }
  tools;
  apiClient;
  /**
   * Valida las variables de entorno requeridas
   */
  validateEnvironment() {
    const requiredVars = ["TRACKHS_API_URL", "TRACKHS_USERNAME", "TRACKHS_PASSWORD"];
    for (const varName of requiredVars) {
      if (!this.env[varName]) {
        throw new Error(`Variable de entorno requerida no configurada: ${varName}`);
      }
    }
    try {
      new URL(this.env.TRACKHS_API_URL);
    } catch {
      throw new Error("TRACKHS_API_URL debe ser una URL v\xE1lida");
    }
  }
  /**
   * Maneja las peticiones HTTP entrantes
   */
  async handleRequest(request) {
    try {
      const url = new URL(request.url);
      console.log(`Simple MCP Server: ${request.method} ${url.pathname}`);
      const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
        "Access-Control-Allow-Credentials": "true"
      };
      if (request.method === "OPTIONS") {
        return new Response(null, { headers: corsHeaders });
      }
      if (url.pathname === "/.well-known/oauth-authorization-server") {
        return new Response(JSON.stringify({
          issuer: "https://trackhs-mcp-remote.ihsolutionsco.workers.dev",
          authorization_endpoint: "https://trackhs-mcp-remote.ihsolutionsco.workers.dev/auth/authorize",
          token_endpoint: "https://trackhs-mcp-remote.ihsolutionsco.workers.dev/auth/token",
          response_types_supported: ["code"],
          grant_types_supported: ["authorization_code"],
          scopes_supported: ["trackhs:read", "trackhs:write"],
          client_id: "trackhs-mcp-client"
        }), {
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json"
          }
        });
      }
      if (url.pathname === "/.well-known/oauth-protected-resource") {
        return new Response(JSON.stringify({
          resource: "https://trackhs-mcp-remote.ihsolutionsco.workers.dev",
          scopes: ["trackhs:read", "trackhs:write"],
          authorization_servers: ["https://trackhs-mcp-remote.ihsolutionsco.workers.dev"]
        }), {
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json"
          }
        });
      }
      if (url.pathname === "/register" && request.method === "POST") {
        return new Response(JSON.stringify({
          client_id: "trackhs-mcp-client",
          client_secret: "trackhs-mcp-secret",
          registration_access_token: "reg_token_" + Math.random().toString(36).substring(2, 15),
          registration_client_uri: "https://trackhs-mcp-remote.ihsolutionsco.workers.dev/register/trackhs-mcp-client",
          client_id_issued_at: Math.floor(Date.now() / 1e3),
          client_secret_expires_at: 0
        }), {
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json"
          }
        });
      }
      if (url.pathname === "/auth/authorize" && request.method === "GET") {
        const responseType = url.searchParams.get("response_type");
        const clientId = url.searchParams.get("client_id");
        const redirectUri = url.searchParams.get("redirect_uri");
        const scope = url.searchParams.get("scope");
        const state = url.searchParams.get("state");
        if (responseType === "code" && clientId === "trackhs-mcp-client") {
          const authCode = "auth_" + Math.random().toString(36).substring(2, 15);
          const redirectUrl = new URL(redirectUri || "https://claude.ai/api/mcp/auth_callback");
          redirectUrl.searchParams.set("code", authCode);
          if (state) {
            redirectUrl.searchParams.set("state", state);
          }
          return Response.redirect(redirectUrl.toString(), 302);
        }
      }
      if (url.pathname === "/auth/token" && request.method === "POST") {
        const body = await request.json();
        const { grant_type, code, redirect_uri, client_id, client_secret } = body;
        if (grant_type === "authorization_code" && client_id === "trackhs-mcp-client") {
          const accessToken = "access_" + Math.random().toString(36).substring(2, 15);
          const refreshToken = "refresh_" + Math.random().toString(36).substring(2, 15);
          return new Response(JSON.stringify({
            access_token: accessToken,
            refresh_token: refreshToken,
            token_type: "Bearer",
            expires_in: 3600,
            scope: "trackhs:read trackhs:write"
          }), {
            headers: {
              ...corsHeaders,
              "Content-Type": "application/json"
            }
          });
        }
      }
      if (url.pathname === "/mcp" && request.method === "POST") {
        const body = await request.json();
        if (body.method === "initialize") {
          return new Response(JSON.stringify({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              protocolVersion: "2024-11-05",
              capabilities: {
                tools: {},
                prompts: {},
                resources: {}
              },
              serverInfo: {
                name: "trackhs-mcp-server",
                version: "1.0.0"
              }
            }
          }), {
            headers: {
              ...corsHeaders,
              "Content-Type": "application/json"
            }
          });
        }
        if (body.method === "tools/list") {
          return new Response(JSON.stringify({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              tools: this.tools.map((tool) => ({
                name: tool.name,
                description: tool.description,
                inputSchema: tool.inputSchema
              }))
            }
          }), {
            headers: {
              ...corsHeaders,
              "Content-Type": "application/json"
            }
          });
        }
        if (body.method === "tools/call") {
          const { name, arguments: args } = body.params;
          const tool = this.tools.find((t) => t.name === name);
          if (!tool) {
            return new Response(JSON.stringify({
              jsonrpc: "2.0",
              id: body.id,
              error: {
                code: -32601,
                message: `Herramienta desconocida: ${name}`
              }
            }), {
              status: 400,
              headers: {
                ...corsHeaders,
                "Content-Type": "application/json"
              }
            });
          }
          try {
            const result = await tool.execute(args || {});
            return new Response(JSON.stringify({
              jsonrpc: "2.0",
              id: body.id,
              result: {
                content: [
                  {
                    type: "text",
                    text: JSON.stringify(result, null, 2)
                  }
                ]
              }
            }), {
              headers: {
                ...corsHeaders,
                "Content-Type": "application/json"
              }
            });
          } catch (error) {
            return new Response(JSON.stringify({
              jsonrpc: "2.0",
              id: body.id,
              error: {
                code: -32603,
                message: "Error interno del servidor",
                data: error instanceof Error ? error.message : "Error desconocido"
              }
            }), {
              status: 500,
              headers: {
                ...corsHeaders,
                "Content-Type": "application/json"
              }
            });
          }
        }
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id: body.id,
          error: {
            code: -32601,
            message: `M\xE9todo MCP no reconocido: ${body.method}`
          }
        }), {
          status: 400,
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json"
          }
        });
      }
      if (url.pathname === "/health" && request.method === "GET") {
        return new Response(JSON.stringify({
          status: "ok",
          server: "trackhs-mcp-server",
          version: "1.0.0",
          tools: this.tools.length
        }), {
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json"
          }
        });
      }
      if (url.pathname === "/" && request.method === "GET") {
        return new Response(JSON.stringify({
          name: "TrackHS MCP Server",
          version: "1.0.0",
          description: "Servidor MCP remoto para integraci\xF3n con Track HS API",
          endpoints: {
            mcp: "/mcp",
            health: "/health",
            oauth: "/auth/authorize"
          },
          tools: this.tools.map((t) => ({
            name: t.name,
            description: t.description
          }))
        }), {
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json"
          }
        });
      }
      console.log(`Simple MCP Server: No route found for ${url.pathname}`);
      return new Response("Not Found", {
        status: 404,
        headers: corsHeaders
      });
    } catch (error) {
      console.error("Error en servidor MCP:", error);
      return new Response(JSON.stringify({
        error: "Error interno del servidor",
        message: error instanceof Error ? error.message : "Error desconocido"
      }), {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      });
    }
  }
  /**
   * Obtiene información sobre las herramientas disponibles
   */
  getToolsInfo() {
    return this.tools.map((tool) => ({
      name: tool.name,
      description: tool.description
    }));
  }
};

// cloudflare/worker.js
var worker_default = {
  async fetch(request, env) {
    try {
      const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
        "Access-Control-Allow-Credentials": "true"
      };
      if (request.method === "OPTIONS") {
        return new Response(null, {
          status: 204,
          headers: corsHeaders
        });
      }
      const server = new SimpleTrackHSMCPServer(env);
      return await server.handleRequest(request);
    } catch (error) {
      console.error("Error en Cloudflare Worker:", error);
      const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
        "Access-Control-Allow-Credentials": "true"
      };
      return new Response(JSON.stringify({
        error: "Error interno del servidor",
        message: error instanceof Error ? error.message : "Error desconocido",
        timestamp: (/* @__PURE__ */ new Date()).toISOString()
      }), {
        status: 500,
        headers: {
          ...corsHeaders,
          "Content-Type": "application/json"
        }
      });
    }
  }
};

// ../../../AppData/Roaming/npm/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// ../../../AppData/Roaming/npm/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// .wrangler/tmp/bundle-jwNSZb/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = worker_default;

// ../../../AppData/Roaming/npm/node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// .wrangler/tmp/bundle-jwNSZb/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=worker.js.map
