from http.client import HTTPException
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        logger.exception("Database integrity error")
        return jsonify(
            {"error": "Integrity Error", "message": "Database constraint violated"}
        ), 409

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.name, "message": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Unhandled exception")
        return jsonify({"message": "something went wrong"}), 500
