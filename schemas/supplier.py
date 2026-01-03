# ---------------- SUPPLIER ----------------

from marshmallow import fields
from schemas.base_schema import SupplierBaseSchema, ProductBaseSchema


class SupplierResponseSchema(SupplierBaseSchema):
    # products = fields.Nested(ProductBaseSchema, many=True)
    pass
