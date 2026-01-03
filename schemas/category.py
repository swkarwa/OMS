from marshmallow import Schema, fields, validate

from schemas.base_schema import CategoryBaseSchema, ProductBaseSchema


class CategoryUpdateSchema(Schema):
    name = fields.Str(required=False, validate=validate.Length(min=1))
    slug = fields.Str(required=False, validate=validate.Length(min=1))


class CategoryResponseSchema(CategoryBaseSchema):
    products = fields.List(fields.Nested(ProductBaseSchema))
