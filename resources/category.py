import logging
from typing import Dict

from flask import session
from flask_smorest import Blueprint, abort
from flask_smorest.blueprint import MethodView
from models import Category as CategoryModel
from models import Product as ProductModel
from models.base import get_session
from schemas import CategoryBaseSchema as CategorySchema, CategoryResponseSchema, ProductBaseSchema
from schemas import CategoryUpdateSchema


log = logging.getLogger(__name__)
blp = Blueprint("categories", __name__, description="operation on categories")


@blp.route("/categories")
class Categories(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        log.info("/GET categories - fetching all categories")
        with get_session() as session:
            categories = session.query(CategoryModel).all()
            log.info(
                f"/GET categories - fetched {len(categories)} categories successfully"
            )
            return categories

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        log.info("/GET categories - creating category")

        with get_session() as session:
            category = CategoryModel(**category_data)
            session.add(category)
            session.flush()
            log.info("/GET categories - category added to session , pending commit")

        log.info("/GET categories - category created successfully")
        return category


@blp.route("/categories/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id: int):
        log.info("/GET categories/{category_id} - fetching category")

        with get_session() as session:
            category = session.get(CategoryModel, category_id)
            if not category:
                log.debug("GET /categories/{category_id} - category not found")
                abort(404, message=f"category not found with id : {category_id}")

        log.info(
            "/GET categories/{category_id} - category with id : {category_id} fetched successfully"
        )
        return category

    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200, CategorySchema)
    def put(self, category_data: Dict, category_id: int):
        log.info("/PUT categories/{category_id} - fetching category")
        with get_session() as session:
            category = session.get(CategoryModel, category_id)
            if not category:
                log.debug("/PUT categories/{category_id} - category not found")
                abort(404, message=f"category not found with id : {category_id}")

            for f, v in category_data.items():
                setattr(category, f, v)

        log.info(
            "/PUT categories/{category_id} - category with id : {category_id} updated successfully"
        )
        return category

    @blp.response(204, description="Category deleted successfully")
    def delete(self, category_id):
        log.info("/DELETE categories/{category_id} - fetching category")

        with get_session() as session:
            category = session.get(CategoryModel, category_id)
            if not category:
                log.info("/DELETE categories/{category_id} - category not found")
                return abort(404, message=f"category with id : {category_id} not found")

            session.delete(category)
            log.info(
                log.info("/DELETE categories/{category_id} - deleted successfully")
            )


# POST   /categories/{category_id}/products/{product_id}
# DELETE /categories/{category_id}/products/{product_id}


# GET    /categories/{category_id}/products
@blp.route("/categories/<int:category_id>/products/<int:product_id>")
class ProductCategoryLink(MethodView):
    @blp.response(200, CategoryResponseSchema)
    def post(self, category_id: int, product_id: int):
        log.info(
            f"/POST /categories/{category_id}/products/{product_id} - fetching product and category to link"
        )

        with get_session() as session:
            category = session.get(CategoryModel, category_id)
            product = session.get(ProductModel, product_id)
            if not category or not product:
                log.info(
                    f"/POST /categories/{category_id}/products/{product_id} - either category or product is not available to link"
                )
                raise RuntimeError("product or category not available to link")

            if product in category.products:
                log.info(
                    f"/POST /categories/{category_id}/products/{product_id} - product with id : {product_id} is already linked to category with id : {category_id}"
                )
                abort(400, message="already linked")
            category.products.append(product)
            _ = category.products
            return category

    @blp.response(200, CategoryResponseSchema)
    def delete(self, category_id: int, product_id: int):
        log.info(
            f"/DELETE /categories/{category_id}/products/{product_id} - fetching product and category to link"
        )

        with get_session() as session:
            category = session.get(CategoryModel, category_id)
            product = session.get(ProductModel, product_id)
            if not category or not product:
                log.info(
                    f"/DELETE /categories/{category_id}/products/{product_id} - either category or product is not available to link"
                )
                raise RuntimeError("product or category not available to link")

            if product not in category.products:
                log.info(
                    f"/DELETE /categories/{category_id}/products/{product_id} - product with id : {product_id} is already linked to category with id : {category_id}"
                )
                abort(400, message="already de linked")
            category.products.remove(product)
            _ = category.products
            return category

@blp.route('/category/<int:category_id>/products')
class ProductsByCategory(MethodView):

    @blp.response(200, ProductBaseSchema(many=True))
    def get(self , category_id):
        log.info(f'/GET /category/{category_id} - fetching products for category')
        with get_session() as session:
            category = session.get(CategoryModel , category_id)

            if not category:
                log.info(f'/GET /category/{category_id} - category not found')
                return abort(404 , message='category not found')

            products = category.products
        log.info(f'/GET /category/{category_id} - total : {products.__len__} fetched successfully')
        return products




