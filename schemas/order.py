from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    status = fields.Str(required=True, validate=OneOf(["Pending", "Paid", "Cancelled"]))
    total_amount = fields.Float(required=True)
    create_at = fields.DateTime(dump_only=True)
