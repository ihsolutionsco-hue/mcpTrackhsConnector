Node Collection

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-nodes-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Nodes API",
    "version": "1.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\n\nThis API covers all endpoints related to unit, unit type and node configuration.\n\nWhen used externally, this API requires a server context key. \n\nWhen used in user context, endpoints may be restricted based on role.",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    }
  },
  "tags": [
    {
      "name": "Nodes",
      "description": "Node Related API"
    }
  ],
  "paths": {
    "/pms/nodes": {
      "get": {
        "summary": "Node Collection",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "nodes": {
                          "type": "array",
                          "items": {
                            "title": "Nodes Response",
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "integer",
                                "description": "ID"
                              },
                              "name": {
                                "type": "string",
                                "description": "Name of Node Type"
                              },
                              "maxPets": {
                                "type": "integer"
                              },
                              "phone": {
                                "type": "string"
                              },
                              "websiteUrl": {
                                "type": "string"
                              },
                              "streetAddress": {
                                "type": "string"
                              },
                              "extendedAddress": {
                                "type": "string"
                              },
                              "locality": {
                                "type": "string"
                              },
                              "region": {
                                "type": "string"
                              },
                              "postal": {
                                "type": "string"
                              },
                              "country": {
                                "type": "string"
                              },
                              "maxDiscount": {
                                "type": "number"
                              },
                              "timezone": {
                                "type": "string"
                              },
                              "longitude": {
                                "type": "number"
                              },
                              "latitude": {
                                "type": "number"
                              },
                              "housekeepingNotes": {
                                "type": "string"
                              },
                              "petFriendly": {
                                "type": "boolean"
                              },
                              "smokingAllowed": {
                                "type": "boolean"
                              },
                              "childrenAllowed": {
                                "type": "boolean"
                              },
                              "eventsAllowed": {
                                "type": "boolean"
                              },
                              "isAccessible": {
                                "type": "boolean"
                              },
                              "hasEarlyCheckin": {
                                "type": "boolean"
                              },
                              "hasLateCheckout": {
                                "type": "boolean"
                              },
                              "quickCheckin": {
                                "type": "boolean"
                              },
                              "quickCheckout": {
                                "type": "boolean"
                              },
                              "checkinTime": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date time in ISO 8601 format"
                              },
                              "checkoutTime": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date time in ISO 8601 format"
                              },
                              "earlyCheckinTime": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date time in ISO 8601 format"
                              },
                              "lateCheckoutTime": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date time in ISO 8601 format"
                              },
                              "description": {
                                "type": "string",
                                "nullable": true,
                                "description": "Description for Node Type."
                              },
                              "shortDescription": {
                                "type": "string"
                              },
                              "longDescription": {
                                "type": "string"
                              },
                              "directions": {
                                "type": "string"
                              },
                              "checkinDetails": {
                                "type": "string"
                              },
                              "houseRules": {
                                "type": "string"
                              },
                              "parentId": {
                                "type": "integer"
                              },
                              "parent": {
                                "type": "object"
                              },
                              "typeId": {
                                "type": "integer"
                              },
                              "type": {
                                "type": "object"
                              },
                              "taxDistrictId": {
                                "type": "integer"
                              },
                              "taxDistrict": {
                                "title": "taxDistrict Response",
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "number"
                                  },
                                  "isActive": {
                                    "type": "boolean"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "shortTermPolicyId": {
                                    "type": "number"
                                  },
                                  "longTermPolicyId": {
                                    "type": "number"
                                  },
                                  "hasBreakpoint": {
                                    "type": "boolean"
                                  },
                                  "breakpoint": {
                                    "type": "number"
                                  },
                                  "salesTaxPolicyId": {
                                    "type": "number"
                                  },
                                  "salesTaxPolicy": {
                                    "type": "object"
                                  },
                                  "taxMarkup": {
                                    "type": "number"
                                  },
                                  "createdAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "createdBy": {
                                    "type": "string"
                                  },
                                  "updatedAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "updatedBy": {
                                    "type": "string"
                                  },
                                  "_embedded": {
                                    "type": "object",
                                    "properties": {
                                      "shortTermPolicy": {
                                        "type": "object",
                                        "description": "this may be just links to policy if not fully hydrated",
                                        "properties": {
                                          "id": {
                                            "type": "number"
                                          },
                                          "isActive": {
                                            "type": "boolean"
                                          },
                                          "name": {
                                            "type": "string"
                                          },
                                          "description": {
                                            "type": "string"
                                          },
                                          "createdAt": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Date time in ISO 8601 format"
                                          },
                                          "createdBy": {
                                            "type": "string"
                                          },
                                          "updatedAt": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Date time in ISO 8601 format"
                                          },
                                          "updatedBy": {
                                            "type": "string"
                                          },
                                          "_embedded": {
                                            "type": "object",
                                            "properties": {
                                              "taxes": {
                                                "type": "array",
                                                "items": {
                                                  "type": "object",
                                                  "properties": {
                                                    "_links": {
                                                      "type": "object",
                                                      "properties": {
                                                        "self": {
                                                          "type": "object",
                                                          "properties": {
                                                            "href": {
                                                              "type": "string"
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          },
                                          "_links": {
                                            "type": "object",
                                            "properties": {
                                              "self": {
                                                "type": "object",
                                                "properties": {
                                                  "href": {
                                                    "type": "string"
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      },
                                      "longTermPolicy": {
                                        "type": "object",
                                        "description": "this may be just links to policy if not fully hydrated",
                                        "properties": {
                                          "id": {
                                            "type": "number"
                                          },
                                          "isActive": {
                                            "type": "boolean"
                                          },
                                          "name": {
                                            "type": "string"
                                          },
                                          "description": {
                                            "type": "string"
                                          },
                                          "createdAt": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Date time in ISO 8601 format"
                                          },
                                          "createdBy": {
                                            "type": "string"
                                          },
                                          "updatedAt": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Date time in ISO 8601 format"
                                          },
                                          "updatedBy": {
                                            "type": "string"
                                          },
                                          "_embedded": {
                                            "type": "object",
                                            "properties": {
                                              "taxes": {
                                                "type": "array",
                                                "items": {
                                                  "type": "object",
                                                  "properties": {
                                                    "_links": {
                                                      "type": "object",
                                                      "properties": {
                                                        "self": {
                                                          "type": "object",
                                                          "properties": {
                                                            "href": {
                                                              "type": "string"
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          },
                                          "_links": {
                                            "type": "object",
                                            "properties": {
                                              "self": {
                                                "type": "object",
                                                "properties": {
                                                  "href": {
                                                    "type": "string"
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  },
                                  "_links": {
                                    "type": "object",
                                    "properties": {
                                      "self": {
                                        "type": "object",
                                        "properties": {
                                          "href": {
                                            "type": "string"
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              },
                              "checkinOfficeId": {
                                "type": "integer"
                              },
                              "checkinOffice": {
                                "type": "object"
                              },
                              "cancellationPolicyId": {
                                "type": "integer"
                              },
                              "cancellationPolicy": {
                                "title": "cancellationPolicy Response",
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "number"
                                  },
                                  "isDefault": {
                                    "type": "boolean"
                                  },
                                  "isActive": {
                                    "type": "boolean"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "createdBy": {
                                    "type": "string"
                                  },
                                  "createdAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "updatedBy": {
                                    "type": "string"
                                  },
                                  "updatedAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "code": {
                                    "type": "string"
                                  },
                                  "chargeAs": {
                                    "type": "string"
                                  },
                                  "canExceedBalance": {
                                    "type": "boolean"
                                  },
                                  "cancelTime": {
                                    "type": "string"
                                  },
                                  "cancelTimezone": {
                                    "type": "string"
                                  },
                                  "postDate": {
                                    "type": "string"
                                  },
                                  "airbnbType": {
                                    "type": "string"
                                  },
                                  "tripadvisorType": {
                                    "type": "string"
                                  },
                                  "homeawayType": {
                                    "type": "string"
                                  },
                                  "breakpoints": {
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "id": {
                                          "type": "number"
                                        },
                                        "rangeStart": {
                                          "type": "number"
                                        },
                                        "rangeEnd": {
                                          "type": "number"
                                        },
                                        "nonRefundable": {
                                          "type": "boolean"
                                        },
                                        "nonCancelable": {
                                          "type": "boolean"
                                        },
                                        "penaltyNights": {
                                          "type": "number"
                                        },
                                        "penaltyPercent": {
                                          "type": "number"
                                        },
                                        "penaltyFlat": {
                                          "type": "number"
                                        },
                                        "description": {
                                          "type": "string"
                                        }
                                      }
                                    }
                                  },
                                  "_links": {
                                    "type": "object",
                                    "properties": {
                                      "self": {
                                        "type": "object",
                                        "properties": {
                                          "href": {
                                            "type": "string"
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              },
                              "housekeepingZoneId": {
                                "type": "integer"
                              },
                              "housekeepingZone": {
                                "title": "housekeepingZone Response",
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "number"
                                  },
                                  "isActive": {
                                    "type": "boolean"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "type": {
                                    "type": "string"
                                  },
                                  "createdAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "createdBy": {
                                    "type": "string"
                                  },
                                  "updatedAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "updatedBy": {
                                    "type": "string"
                                  },
                                  "_links": {
                                    "type": "object",
                                    "properties": {
                                      "self": {
                                        "type": "object",
                                        "properties": {
                                          "href": {
                                            "type": "string"
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              },
                              "maintenanceZoneId": {
                                "type": "integer"
                              },
                              "maintenanceZone": {
                                "title": "maintenanceZone Response",
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "number"
                                  },
                                  "isActive": {
                                    "type": "boolean"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "type": {
                                    "type": "string"
                                  },
                                  "createdAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "createdBy": {
                                    "type": "string"
                                  },
                                  "updatedAt": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Date time in ISO 8601 format"
                                  },
                                  "updatedBy": {
                                    "type": "string"
                                  },
                                  "_links": {
                                    "type": "object",
                                    "properties": {
                                      "self": {
                                        "type": "object",
                                        "properties": {
                                          "href": {
                                            "type": "string"
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              },
                              "isReservations": {
                                "type": "boolean",
                                "nullable": true
                              },
                              "isHousekeeping": {
                                "type": "boolean",
                                "nullable": true
                              },
                              "isMaintenance": {
                                "type": "boolean",
                                "nullable": true
                              },
                              "isOnline": {
                                "type": "boolean",
                                "nullable": true
                              },
                              "isOwners": {
                                "type": "boolean",
                                "nullable": true
                              },
                              "isActive": {
                                "type": "boolean",
                                "nullable": true
                              },
                              "createdAt": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date time in ISO 8601 format"
                              },
                              "createdBy": {
                                "type": "string",
                                "description": "User who created"
                              },
                              "updatedAt": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Date time in ISO 8601 format"
                              },
                              "updatedBy": {
                                "type": "string",
                                "description": "User who updated"
                              },
                              "roles": {
                                "type": "array",
                                "nullable": true,
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "roleId": {
                                      "type": "integer"
                                    },
                                    "userId": {
                                      "type": "integer"
                                    }
                                  }
                                }
                              },
                              "custom": {
                                "type": "object",
                                "description": "custom per install pms_nodes_*"
                              },
                              "guaranteePoliciesIds": {
                                "type": "array"
                              },
                              "amenitiesIds": {
                                "type": "array"
                              },
                              "documentsIds": {
                                "type": "array"
                              },
                              "gatewaysIds": {
                                "type": "array"
                              },
                              "_embedded": {
                                "type": "object",
                                "nullable": true,
                                "properties": {
                                  "parent": {
                                    "type": "object",
                                    "properties": {
                                      "_links": {
                                        "type": "object",
                                        "properties": {
                                          "self": {
                                            "type": "object",
                                            "properties": {
                                              "href": {
                                                "type": "string"
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  },
                                  "type": {
                                    "title": "Node Type Response",
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "integer",
                                        "description": "ID"
                                      },
                                      "name": {
                                        "type": "string"
                                      },
                                      "description": {
                                        "type": "string"
                                      },
                                      "isReport": {
                                        "type": "boolean"
                                      },
                                      "isReservations": {
                                        "type": "boolean"
                                      },
                                      "isHousekeeping": {
                                        "type": "boolean"
                                      },
                                      "isMaintenance": {
                                        "type": "boolean"
                                      },
                                      "isOnline": {
                                        "type": "boolean"
                                      },
                                      "isOwners": {
                                        "type": "boolean"
                                      },
                                      "isActive": {
                                        "type": "boolean"
                                      },
                                      "createdAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "createdBy": {
                                        "type": "string"
                                      },
                                      "updatedAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "updatedBy": {
                                        "type": "string"
                                      },
                                      "_links": {
                                        "type": "object",
                                        "properties": {
                                          "self": {
                                            "type": "object",
                                            "properties": {
                                              "href": {
                                                "type": "string"
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  },
                                  "taxDistrict": {
                                    "title": "taxDistrict Response",
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "number"
                                      },
                                      "isActive": {
                                        "type": "boolean"
                                      },
                                      "name": {
                                        "type": "string"
                                      },
                                      "shortTermPolicyId": {
                                        "type": "number"
                                      },
                                      "longTermPolicyId": {
                                        "type": "number"
                                      },
                                      "hasBreakpoint": {
                                        "type": "boolean"
                                      },
                                      "breakpoint": {
                                        "type": "number"
                                      },
                                      "salesTaxPolicyId": {
                                        "type": "number"
                                      },
                                      "salesTaxPolicy": {
                                        "type": "object"
                                      },
                                      "taxMarkup": {
                                        "type": "number"
                                      },
                                      "createdAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "createdBy": {
                                        "type": "string"
                                      },
                                      "updatedAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "updatedBy": {
                                        "type": "string"
                                      },
                                      "_embedded": {
                                        "type": "object",
                                        "properties": {
                                          "shortTermPolicy": {
                                            "type": "object",
                                            "description": "this may be just links to policy if not fully hydrated",
                                            "properties": {
                                              "id": {
                                                "type": "number"
                                              },
                                              "isActive": {
                                                "type": "boolean"
                                              },
                                              "name": {
                                                "type": "string"
                                              },
                                              "description": {
                                                "type": "string"
                                              },
                                              "createdAt": {
                                                "type": "string",
                                                "format": "date-time",
                                                "description": "Date time in ISO 8601 format"
                                              },
                                              "createdBy": {
                                                "type": "string"
                                              },
                                              "updatedAt": {
                                                "type": "string",
                                                "format": "date-time",
                                                "description": "Date time in ISO 8601 format"
                                              },
                                              "updatedBy": {
                                                "type": "string"
                                              },
                                              "_embedded": {
                                                "type": "object",
                                                "properties": {
                                                  "taxes": {
                                                    "type": "array",
                                                    "items": {
                                                      "type": "object",
                                                      "properties": {
                                                        "_links": {
                                                          "type": "object",
                                                          "properties": {
                                                            "self": {
                                                              "type": "object",
                                                              "properties": {
                                                                "href": {
                                                                  "type": "string"
                                                                }
                                                              }
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              },
                                              "_links": {
                                                "type": "object",
                                                "properties": {
                                                  "self": {
                                                    "type": "object",
                                                    "properties": {
                                                      "href": {
                                                        "type": "string"
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          },
                                          "longTermPolicy": {
                                            "type": "object",
                                            "description": "this may be just links to policy if not fully hydrated",
                                            "properties": {
                                              "id": {
                                                "type": "number"
                                              },
                                              "isActive": {
                                                "type": "boolean"
                                              },
                                              "name": {
                                                "type": "string"
                                              },
                                              "description": {
                                                "type": "string"
                                              },
                                              "createdAt": {
                                                "type": "string",
                                                "format": "date-time",
                                                "description": "Date time in ISO 8601 format"
                                              },
                                              "createdBy": {
                                                "type": "string"
                                              },
                                              "updatedAt": {
                                                "type": "string",
                                                "format": "date-time",
                                                "description": "Date time in ISO 8601 format"
                                              },
                                              "updatedBy": {
                                                "type": "string"
                                              },
                                              "_embedded": {
                                                "type": "object",
                                                "properties": {
                                                  "taxes": {
                                                    "type": "array",
                                                    "items": {
                                                      "type": "object",
                                                      "properties": {
                                                        "_links": {
                                                          "type": "object",
                                                          "properties": {
                                                            "self": {
                                                              "type": "object",
                                                              "properties": {
                                                                "href": {
                                                                  "type": "string"
                                                                }
                                                              }
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              },
                                              "_links": {
                                                "type": "object",
                                                "properties": {
                                                  "self": {
                                                    "type": "object",
                                                    "properties": {
                                                      "href": {
                                                        "type": "string"
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      },
                                      "_links": {
                                        "type": "object",
                                        "properties": {
                                          "self": {
                                            "type": "object",
                                            "properties": {
                                              "href": {
                                                "type": "string"
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  },
                                  "cancellationPolicy": {
                                    "title": "cancellationPolicy Response",
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "number"
                                      },
                                      "isDefault": {
                                        "type": "boolean"
                                      },
                                      "isActive": {
                                        "type": "boolean"
                                      },
                                      "name": {
                                        "type": "string"
                                      },
                                      "createdBy": {
                                        "type": "string"
                                      },
                                      "createdAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "updatedBy": {
                                        "type": "string"
                                      },
                                      "updatedAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "code": {
                                        "type": "string"
                                      },
                                      "chargeAs": {
                                        "type": "string"
                                      },
                                      "canExceedBalance": {
                                        "type": "boolean"
                                      },
                                      "cancelTime": {
                                        "type": "string"
                                      },
                                      "cancelTimezone": {
                                        "type": "string"
                                      },
                                      "postDate": {
                                        "type": "string"
                                      },
                                      "airbnbType": {
                                        "type": "string"
                                      },
                                      "tripadvisorType": {
                                        "type": "string"
                                      },
                                      "homeawayType": {
                                        "type": "string"
                                      },
                                      "breakpoints": {
                                        "type": "array",
                                        "items": {
                                          "type": "object",
                                          "properties": {
                                            "id": {
                                              "type": "number"
                                            },
                                            "rangeStart": {
                                              "type": "number"
                                            },
                                            "rangeEnd": {
                                              "type": "number"
                                            },
                                            "nonRefundable": {
                                              "type": "boolean"
                                            },
                                            "nonCancelable": {
                                              "type": "boolean"
                                            },
                                            "penaltyNights": {
                                              "type": "number"
                                            },
                                            "penaltyPercent": {
                                              "type": "number"
                                            },
                                            "penaltyFlat": {
                                              "type": "number"
                                            },
                                            "description": {
                                              "type": "string"
                                            }
                                          }
                                        }
                                      },
                                      "_links": {
                                        "type": "object",
                                        "properties": {
                                          "self": {
                                            "type": "object",
                                            "properties": {
                                              "href": {
                                                "type": "string"
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  },
                                  "housekeepingZone": {
                                    "title": "housekeepingZone Response",
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "number"
                                      },
                                      "isActive": {
                                        "type": "boolean"
                                      },
                                      "name": {
                                        "type": "string"
                                      },
                                      "type": {
                                        "type": "string"
                                      },
                                      "createdAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "createdBy": {
                                        "type": "string"
                                      },
                                      "updatedAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "updatedBy": {
                                        "type": "string"
                                      },
                                      "_links": {
                                        "type": "object",
                                        "properties": {
                                          "self": {
                                            "type": "object",
                                            "properties": {
                                              "href": {
                                                "type": "string"
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  },
                                  "maintenanceZone": {
                                    "title": "maintenanceZone Response",
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "number"
                                      },
                                      "isActive": {
                                        "type": "boolean"
                                      },
                                      "name": {
                                        "type": "string"
                                      },
                                      "type": {
                                        "type": "string"
                                      },
                                      "createdAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "createdBy": {
                                        "type": "string"
                                      },
                                      "updatedAt": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Date time in ISO 8601 format"
                                      },
                                      "updatedBy": {
                                        "type": "string"
                                      },
                                      "_links": {
                                        "type": "object",
                                        "properties": {
                                          "self": {
                                            "type": "object",
                                            "properties": {
                                              "href": {
                                                "type": "string"
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              },
                              "_links": {
                                "type": "object",
                                "properties": {
                                  "self": {
                                    "type": "object",
                                    "properties": {
                                      "href": {
                                        "type": "string"
                                      }
                                    }
                                  },
                                  "images": {
                                    "type": "object",
                                    "properties": {
                                      "href": {
                                        "type": "string"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    },
                    "page": {
                      "type": "number"
                    },
                    "page_count": {
                      "type": "number"
                    },
                    "page_size": {
                      "type": "number"
                    },
                    "total_items": {
                      "type": "number"
                    },
                    "_links": {
                      "title": "CollectionLinks",
                      "type": "object",
                      "properties": {
                        "self": {
                          "type": "object",
                          "required": [
                            "href"
                          ],
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "first": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "last": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "next": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "prev": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        }
                      },
                      "required": [
                        "self",
                        "first",
                        "last"
                      ],
                      "description": "All collections provide the following set of links. Next or prev will only be provided if there is a next or previous page.",
                      "x-examples": {}
                    }
                  },
                  "required": [
                    "_embedded",
                    "page",
                    "page_count",
                    "page_size",
                    "total_items",
                    "_links"
                  ]
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          },
          "500": {
            "description": "Internal Server Error",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          }
        },
        "operationId": "getNodes",
        "description": "This endpoint will return all nodes.\n\nData provided is considered public and can be distributed.",
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "page",
            "description": "Page Number"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "size",
            "description": "Page size, defaults to 25. No max currently but we may consider setting it at 100 or so."
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "id",
                "name"
              ],
              "default": "id"
            },
            "in": "query",
            "name": "sortColumn",
            "description": "Only id and name supported."
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ],
              "default": "asc"
            },
            "in": "query",
            "name": "sortDirection",
            "description": "asc or desc"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "search",
            "description": "Search with name or in short and long description"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "term",
            "description": "Will search node caption/name"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "parentId",
            "description": "Find nodes by parent ID, shows all children"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "typeId",
            "description": "Find nodes by node type id"
          },
          {
            "schema": {
              "type": "integer",
              "enum": [
                1,
                0
              ]
            },
            "in": "query",
            "name": "computed",
            "description": "Return additional computed values attributes based on inherited attributes"
          },
          {
            "schema": {
              "type": "integer",
              "enum": [
                1,
                0
              ]
            },
            "in": "query",
            "name": "inherited",
            "description": "Return additional inherited attributes"
          },
          {
            "schema": {
              "type": "integer",
              "enum": [
                1,
                0
              ]
            },
            "in": "query",
            "name": "includeDescriptions",
            "description": "Return descriptions of units, may be inherited from node if set to inherited"
          }
        ],
        "tags": [
          "Nodes"
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "hmac": {
        "type": "http",
        "scheme": "bearer",
        "description": "HMAC Authentication based on https://github.com/acquia/http-hmac-spec/tree/2.0"
      },
      "basic": {
        "type": "http",
        "scheme": "basic",
        "description": "Authentication is unique to each customer. Please request authorization keys from the customer you are integrating with."
      }
    }
  },
  "security": [
    {
      "basic": []
    },
    {
      "hmac": []
    }
  ],
  "servers": [
    {
      "url": "{customerDomain}/api",
      "variables": {
        "customerDomain": {
          "default": "https://api-integration-example.tracksandbox.io",
          "description": "API domain"
        }
      }
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```