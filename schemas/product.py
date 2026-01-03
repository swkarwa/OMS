# ---------------- Product ----------------
# id = Column(Integer , primary_key=True , nullable=False , autoincrement=True)
# supplier_id = Column(Integer , ForeignKey('suppliers.id') , nullable=False)
# name = Column(String , unique=True , nullable=False)
# price = Column(Float , nullable=False)
# created_at = Column(DateTime(timezone=True) , nullable=False , default=func.now())


from marshmallow import Schema, fields, validate

from schemas.base_schema import ProductBaseSchema, SupplierBaseSchema
from schemas.category import CategoryBaseSchema
from schemas.inventory import InventoryResponseSchema


class ProductRequestSchema(ProductBaseSchema):
    id = fields.Integer(dump_only=True)
    supplier_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    categories = fields.Nested(CategoryBaseSchema(many=True))


class ProductUpdateSchema(Schema):
    supplier_id = fields.Integer(required=False)
    name = fields.Str(required=False, validate=validate.Length(min=1))
    price = fields.Float(required=False)


class ProductResponseSchema(ProductBaseSchema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    categories = fields.List(fields.Nested(CategoryBaseSchema))
    supplier = fields.Nested(SupplierBaseSchema)
    inventory = fields.Nested(InventoryResponseSchema)

# passed in query_params for /products for filtering
class ProductFilterSchema(Schema):
    supplier_id = fields.Int(required=False)
    category_id = fields.Int(required=False)
    min_price = fields.Float(required=False)
    max_price = fields.Float(required=False)
