from axial.schema import Schema
from axial.schema import fields


class StatusCheckSchema(Schema):
    name = fields.Str(1, required=True)
    datetime = fields.Str(2, required=True)
