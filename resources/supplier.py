import logging

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from models.base import get_session
from schemas import SupplierResponseSchema, SupplierBaseSchema, ProductBaseSchema
from models import Supplier

log = logging.getLogger(__name__)
blp = Blueprint("supplier", __name__, "operation on supplier")


@blp.route("/suppliers")
class SupplierList(MethodView):
    @blp.response(200, SupplierResponseSchema(many=True))
    def get(self):
        log.info("GET /suppliers - fetching all suppliers")

        with get_session() as session:
            suppliers = session.query(Supplier).all()
            log.info(
                "GET /suppliers - fetched %d suppliers successfully", len(suppliers)
            )
            return suppliers

    @blp.arguments(SupplierBaseSchema)
    @blp.response(201, SupplierBaseSchema, description="resource created")
    def post(self, supplier_data):
        log.info("POST /suppliers - creating supplier")

        with get_session() as session:
            supplier = Supplier(**supplier_data)
            session.add(supplier)
            session.flush()  # Flush to get the ID assigned
            log.info("POST /suppliers - supplier created successfully")
            return supplier


@blp.route("/supplier/<int:supplier_id>")
class SupplierOperation(MethodView):
    @blp.response(200, SupplierBaseSchema)
    def get(self, supplier_id):
        log.info("GET /supplier/%s - fetching supplier", supplier_id)

        with get_session() as session:
            supplier = session.get(Supplier, supplier_id)
            if not supplier:
                log.warning("GET /supplier/%s - supplier not found", supplier_id)
                abort(404, message="Supplier not found")

            log.info("GET /supplier/%s - supplier fetched successfully", supplier_id)
            return supplier

    @blp.arguments(SupplierBaseSchema)
    @blp.response(200, SupplierBaseSchema)
    def put(self, supplier_data, supplier_id):
        log.info("PUT /supplier/%s - updating supplier", supplier_id)

        with get_session() as session:
            supplier = session.get(Supplier, supplier_id)
            if not supplier:
                log.warning("PUT /supplier/%s - supplier not found", supplier_id)
                abort(404, message="Supplier not found")

            for field, value in supplier_data.items():
                setattr(supplier, field, value)

            log.info("PUT /supplier/%s - supplier updated successfully", supplier_id)
            return supplier

    @blp.response(204, description="resource deleted")
    def delete(self, supplier_id):
        log.info("DELETE /supplier/%s - deleting supplier", supplier_id)

        with get_session() as session:
            supplier = session.get(Supplier, supplier_id)
            if not supplier:
                log.warning("DELETE /supplier/%s - supplier not found", supplier_id)
                abort(404, message="resource not found")

            session.delete(supplier)
            log.info("DELETE /supplier/%s - supplier deleted successfully", supplier_id)


@blp.route('/supplier/<int:supplier_id>/products')
class ProductSupplier(MethodView):

    @blp.response(200 , ProductBaseSchema(many=True))
    def get(self, supplier_id):

        log.info(f'GET /supplier/{supplier_id}/products - fetching supplier by id')
        with get_session() as session:
            supplier = session.get(Supplier , supplier_id)
            if not supplier:
                log.info(f'GET /supplier/{supplier_id}/products - supplier not  found')

            log.info(f'GET /supplier/{supplier_id}/products - fetched supplier successfully')
            products = supplier.products

        log.info(f'GET /supplier/{supplier_id}/products - total : {products.__len__} products fetched successfully')

        return products
