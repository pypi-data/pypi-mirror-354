schema_notam = {
    "type": "object",
    "properties": {
        "state": {
            "type": "string",
        },
        "id": {
            "type": "string",
            "minLength": 1
        },
        "notam_type": {
            "type": "string",
            "enum": ["NEW", "REPLACE", "CANCEL"]
        },
        "referenced_notam": {
            "type": ["string", "null"],
            "pattern": "^[A-Z]\\d{4}/\\d{2}$"
        },
        "fir": {
            "type": "string",
            "pattern": "^[A-Z]{4}$"
        },
        "notam_code": {
            "type": "string",
            "pattern": "^[A-Z]{5}$"
        },
        "entity": {
            "type": "string",
            "pattern": "^[A-Z]{2}$"
        },
        "status": {
            "type": "string",
            "pattern": "^[A-Z]{2}$"
        },
        "category_area": {
            "type": "string",
        },
        "sub_area": {
            "type": "string",
        },
        "subject": {
            "type": "string",
        },
        "condition": {
            "type": "string",
        },
        "modifier": {
            "type": "string",
        },
        "coordinate": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "string",
                },
                "lon": {
                    "type": "string",
                },
                "radius": {
                    "type": "number",
                    "minimum": 0
                }
            },
            "required": ["lat", "lon", "radius"]
        },
        "location": {
            "type": "string",
            "pattern": "^[A-Z]{4}$"
        },
        "valid_from": {
            "type": "string",
            "format": "date-time"
        },
        "valid_till": {
            "type": "string",
            "format": "date-time"
        },
        "schedule": {
            "type": ["string", "null"]
        },
        "body": {
            "type": "string",
        },
        "lower_limit": {
            "type": ["string", "null"]
        },
        "upper_limit": {
            "type": ["string", "null"]
        }
    },
    "allOf": [
        {
            "if": {
                "properties": {
                    "notam_type": {"const": "NEW"}
                }
            },
            "then": {
                "properties": {
                    "referenced_notam": {"type": "null"}
                }
            }
        },
        {
            "if": {
                "properties": {
                    "notam_type": {"const": "REPLACE"}
                }
            },
            "then": {
                "properties": {
                    "referenced_notam": {
                        "type": "string",
                        "pattern": "^[A-Z]\\d{4}/\\d{2}$"
                    }
                },
                "required": ["referenced_notam"]
            }
        },
        {
            "if": {
                "properties": {
                    "notam_type": {"const": "CANCEL"}
                }
            },
            "then": {
                "properties": {
                    "referenced_notam": {
                        "type": "string",
                        "pattern": "^[A-Z]\\d{4}/\\d{2}$"
                    }
                },
                "required": ["referenced_notam"]
            }
        }
    ],
    "dependentRequired": {
        "notam_code": ["entity", "status", "category_area", "sub_area", "subject", "condition", "modifier"]
    },
    "required": ["id", "notam_type", "notam_code", "body", "valid_till", "valid_from", "fir", "coordinate", "location"]
}
