user_register_request_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "$id": "https://example.com/employee.schema.json",
    "title": "User registration request",
    "description": "Details of user object in register request",
    "type": "object",
    "properties": {
        "username": {"type": "string",
                     "format": "email",
                     "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                     "minLength": 10,
                     "maxLength": 50},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "password": {"type": "string"},
        "roles": {
                    "type": "array",
                    "items": {
                        "description": "List of roles",
                        "type": "string"
                    },
                    "minItems": 1,
                    "uniqueItems": True
        }
    },
    "required": ["username", "first_name", "last_name", "password", "roles"],
    "additionalProperties": False
}

user_login_request_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "$id": "https://example.com/employee.schema.json",
    "title": "User login request",
    "description": "Details of user object in login request",
    "type": "object",
    "properties": {
        "username": {"type": "string",
                     "format": "email",
                     "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                     "minLength": 10,
                     "maxLength": 50},
        "password": {"type": "string"},
    },
    "required": ["username", "password"],
    "additionalProperties": False
}