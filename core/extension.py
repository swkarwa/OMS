from flask_jwt_extended import JWTManager
from flask_smorest import Api
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


jwt = JWTManager()
jwt_blocklist = set()


@jwt.token_in_blocklist_loader  # checks if logged out
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in jwt_blocklist


@jwt.invalid_token_loader  # checks if token is valid
def invalid_token_callback(error):
    return {"message": "Invalid authentication token."}, 401


@jwt.expired_token_loader  # token is valid, but checks if it is expired
def expired_token_callback(jwt_header, jwt_payload):
    return {"message": "Token has expired. Please refresh or login again."}, 401


@jwt.revoked_token_loader  # token is valid, but this token is being refreshed
def revoked_token_callback(jwt_header, jwt_payload):
    return {"message": "Token has been revoked. Please login again."}, 401


api = Api()
