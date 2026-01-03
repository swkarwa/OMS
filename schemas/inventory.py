from marshmallow import fields, Schema

from schemas.base_schema import InventoryBaseSchema


class InventoryCreateSchema(InventoryBaseSchema):
    product_id = fields.Int(required=True)

class InventoryResponseSchema(InventoryBaseSchema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class InventoryUpdateSchema(Schema):
    quantity = fields.Int(required=True)
    product_id = fields.Int(required=False)