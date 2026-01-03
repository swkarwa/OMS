from flask import Flask

from core import Config, jwt, api
from core.error_handling import register_error_handlers
from core.extension import setup_logging
from models.base import init_db
from resources.supplier import blp as supplier_blueprint
from resources.user import blp as user_blueprint
from resources.auth import blp as auth_blueprint
from resources.product import blp as product_blueprint
from resources.category import blp as category_blueprint
from resources.inventory import blp as inventory_blueprint


def create_app():
    app = Flask(__name__)

    Config.validate()
    app.config.from_object(Config)

    jwt.init_app(app)

    init_db(app.config["SQLALCHEMY_DATABASE_URI"])

    api.init_app(app)
    api.register_blueprint(supplier_blueprint)
    api.register_blueprint(user_blueprint)
    api.register_blueprint(auth_blueprint)
    api.register_blueprint(product_blueprint)
    api.register_blueprint(category_blueprint)
    api.register_blueprint(inventory_blueprint)

    register_error_handlers(app)
    setup_logging()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
