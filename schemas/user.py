# ---------------- USER ----------------


from marshmallow import fields
from schemas.base_schema import UserBaseSchema
from schemas.order import OrderSchema


class UserOrderSchema(UserBaseSchema):
    orders = fields.Nested(OrderSchema, many=True, dump_only=True)
