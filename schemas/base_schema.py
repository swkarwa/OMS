from marshmallow import Schema, fields, validate


class CategoryBaseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    slug = fields.Str(required=True, validate=validate.Length(min=1))


class ProductBaseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True)


class SupplierBaseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=False, validate=validate.Length(min=1))
    email = fields.Email(required=False, validate=validate.Length(min=1))
    phone = fields.Str(
        required=False,
        validate=validate.Regexp(
            r"^[0-9]{10}$", error="Phone number must be 10 digits"
        ),
    )


class UserBaseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=False, validate=validate.Length(min=1))
    email = fields.Email(required=False)
    password = fields.String(
        required=False, validate=validate.Length(min=8), load_only=True
    )

class InventoryBaseSchema(Schema):
    quantity = fields.Int(required=True)