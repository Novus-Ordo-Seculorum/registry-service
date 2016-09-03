from axial.schema import Schema
from axial.schema.fields import (
    Str, Bool, Int, Nested
    )


class SuccessSchema(Schema):
    success = Bool(1, required=True)


class FieldAttrsSchema(Schema):
    required = Bool(1, required=True, allow_none=True)
    field_number = Int(2, required=True)
    allow_none = Bool(3, required=True, allow_none=True)
    nested = Str(4, required=True, allow_none=True)
    many = Bool(5, required=True, allow_none=True)
    dump_to = Str(6, required=True, allow_none=True)
    load_from = Str(7, required=True, allow_none=True)


class FieldSchema(Schema):
    name = Str(1, required=True)
    type = Str(2, required=True)
    attrs = Nested(3, FieldAttrsSchema, required=True)


class SchemaMetaSchema(Schema):
    strict = Bool(1, required=False, default=True)


class SchemaSchema(Schema):
    name = Str(1, required=True)
    meta = Nested(2, SchemaMetaSchema, required=True)
    fields = Nested(3, FieldSchema, required=True, many=True)


class SchemaSetSchema(Schema):
    request = Str(1, required=True, allow_none=True)
    response = Str(2, required=True, allow_none=True)
    params = Str(3, required=True, allow_none=True)


class HandlerSchema(Schema):
    method = Str(1, required=True)
    version = Str(2, required=True)
    schemas = Nested(3, SchemaSetSchema, required=True)


class RouteSchema(Schema):
    name = Str(1, required=True)
    path = Str(2, required=True)
    handlers = Nested(3, HandlerSchema, required=True, many=True)


class ServiceSchema(Schema):
    name = Str(1, required=True)
    routes = Nested(2, RouteSchema, required=True, many=True)
    schemas = Nested(3, SchemaSchema, required=True, many=True)
    proto = Str(4, required=False, allow_none=True)


class ServicesSchema(Schema):
    services = Nested(1, ServiceSchema, required=True, many=True)


class ServiceNamesSchema(Schema):
    services = Str(1, required=True, many=True)
