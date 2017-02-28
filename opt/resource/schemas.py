sourceSchema = {
    "type": "object",
    "properties": {
        "access_key_id": {
            "type": "string"
        },
        "secret_access_key": {
            "type": "string"
        }
    },
    "required": [
        "access_key_id",
        "secret_access_key"
    ]
}

versionSchema = {
    "oneOf": [{
        "type": "object",
        "properties": {
            "schema": {
                "type": "string"
            }
        }
    }, {
        "type": "null"
    }]
}

checkSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": sourceSchema,
        "version": versionSchema
    },
    "required": [
        "source"
    ]
}

outSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": sourceSchema,
        "params": {
            "type": "object",
            "properties": {
                "env_file": {
                    "type": "string"
                },
                "env": {
                    "type": "string"
                },
                "deploy": {
                    "type": "boolean"
                },
                "delete": {
                    "type": "boolean"
                },
                "config_file": {
                    "type": "string"
                },
                "artifact_file": {
                    "type": "string"
                }
            },
            "oneOf": [{
                "required": ["deploy"]
            }, {
                "required": ["remove"]
            }],
            "dependencies": {
                "deploy": {
                    "required": {
                        "config_file",
                        "artifact_file"
                    }
                },
                "remove": {
                    "required": {
                        "config_file"
                    }
                }
            },
            "additionalProperties": "false"
        }
    },
    "required": [
        "source",
        "params"
    ]
}

inSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": sourceSchema,
        "version": versionSchema
    },
    "required": [
        "source",
        "version"
    ]
}
