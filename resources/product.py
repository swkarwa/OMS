import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import Product, Category
from models.base import get_session
from schemas import ProductResponseSchema, ProductUpdateSchema, ProductFilterSchema
from schemas.product import ProductRequestSchema

log = logging.getLogger(__name__)
blp = Blueprint("products", __name__, "operation on products")


@blp.route("/products")
class ProductList(MethodView):
    @blp.arguments(ProductFilterSchema, location="query")
    @blp.response(200, ProductResponseSchema(many=True))
    def get(self, filters):
        log.info("GET /products - fetching products with filters=%s", filters)
        with get_session() as session:
            query = session.query(Product)
            if "supplier_id" in filters:
                query = query.filter(Product.supplier_id == filters["supplier_id"])
            if "category_id" in filters:
                # method 1:
                query = query.filter(
                    Product.categories.any(Category.id == filters["category_id"])
                )

                # method 2:
                # query = query.join(Product.categories).filter(Category.id == filters['category_id'])
            if "min_price" in filters:
                query = query.filter(Product.price >= filters["min_price"])

            if "max_price" in filters:
                query = query.filter(Product.price <= filters["max_price"])

            products = query.all()
            # Access relationships to trigger eager load
            for p in products:
                _ = p.categories, p.supplier, p.inventory
            log.info("GET /products - fetched %d products", len(products))
            return products

    @blp.arguments(ProductRequestSchema)
    @blp.response(201, ProductResponseSchema)
    def post(self, product_data):
        log.info(f"creating product with data : {product_data}")
        with get_session() as session:
            product = Product(**product_data)
            session.add(product)
            session.flush()
            # Access relationships to trigger eager load
            _ = product.categories, product.supplier, product.inventory
            return product


@blp.route("/products/<int:product_id>")
class SingleProduct(MethodView):
    @blp.response(200, ProductResponseSchema)
    def get(self, product_id):
        log.info(f"fetching product with id : {product_id}")
        with get_session() as session:
            product = session.get(Product, product_id)
            if not product:
                log.info(f"product with id : {product_id} does not exist")
                abort(404, message="resource not found")

            # Access relationships to trigger eager load
            _ = product.categories, product.supplier, product.inventory
            log.info(f"product with id : {product_id} found successfully")
            return product

    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductResponseSchema)
    def put(self, product_data, product_id):
        log.info(f"updating product with id : {product_id}")
        with get_session() as session:
            product = session.get(Product, product_id)
            if not product:
                log.info(f"product with id : {product_id} does not exist")
                abort(404, message="product not found")

            for f, v in product_data.items():
                setattr(product, f, v)

            # Access relationships to trigger eager load
            _ = product.categories, product.supplier, product.inventory
            log.info(f"updated product with id : {product_id} successfully")
            return product

    @blp.response(204, description="Delete product")
    def delete(self, product_id):
        log.info(f"fetching product with id : {product_id}")
        with get_session() as session:
            product = session.get(Product, product_id)
            if not product:
                log.info(f"product with id : {product_id} does not exist")
                return abort(404, message="resource not found")
            session.delete(product)
            log.info(f"deleted product with id : {product_id} successfully")
