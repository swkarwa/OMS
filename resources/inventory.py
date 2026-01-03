import logging
from operator import invert

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import Inventory
from models.base import get_session
from schemas import InventoryCreateSchema, InventoryResponseSchema, InventoryUpdateSchema

# POST   /inventory                      # create inventory
# GET    /inventory                      # list inventory
# GET    /inventory/product/{product_id} # get stock of product
# PUT    /inventory/{inventory_id}       # update stock

log = logging.getLogger(__name__)
blp = Blueprint('inventory', __name__, 'operations on inventory')


@blp.route('/inventory')
class InventoryList(MethodView):

    @blp.arguments(InventoryCreateSchema)
    @blp.response(201, InventoryResponseSchema)
    def post(self, inventory_data):
        log.info(f"POST /inventory - adding product id: {inventory_data['product_id']} to inventory")

        with get_session() as session:
            inventory = Inventory(**inventory_data)
            session.add(inventory)
            session.flush()
        log.info(f"POST /inventory - added product id: {inventory_data['product_id']} successfully")
        return inventory

    @blp.response(200, InventoryResponseSchema(many=True))
    def get(self):
        log.info("GET /inventory - fetching all inventory")
        with get_session() as session:
            inventories = session.query(Inventory).all()
            log.info(f"GET /inventory - fetched {len(inventories)} items successfully")
            return inventories


@blp.route('/inventory/<int:inventory_id>')
class InventoryUpdate(MethodView):

    @blp.arguments(InventoryUpdateSchema)
    @blp.response(200, InventoryResponseSchema)
    def put(self, inventory_data, inventory_id):
        log.info(f"PUT /inventory/{inventory_id} - updating inventory")
        with get_session() as session:
            inventory = session.get(Inventory, inventory_id)
            if not inventory:
                abort(404, message='Inventory not found')

            for field, value in inventory_data.items():
                setattr(inventory, field, value)

            session.add(inventory)

        log.info(f"PUT /inventory/{inventory_id} - updated successfully")
        return inventory


@blp.route('/inventory/product/<int:product_id>')
class ProductInventory(MethodView):

    @blp.response(200, InventoryResponseSchema)
    def get(self, product_id):
        log.info(f"GET /inventory/product/{product_id} - fetching inventory for product")

        with get_session() as session:
            inventory = session.query(Inventory).filter_by(product_id=product_id).one_or_none()
            if not inventory:
                abort(404, message=f'No inventory found for product id: {product_id}')

            log.info(f"GET /inventory/product/{product_id} - found successfully")
            return inventory
