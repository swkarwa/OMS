import logging
from typing import Any
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from models import User as UserModel
from models.base import get_session
from schemas import Login
from core import jwt_blocklist

log = logging.getLogger(__name__)
blp = Blueprint("auth", __name__, "identity of user")


@blp.route("/auth/login")
class UserLogin(MethodView):
    @blp.arguments(Login)
    def post(self, user_data):
        log.info("POST /auth/login - login attempt for email=%s", user_data["email"])

        with get_session() as session:
            user: Any[UserModel] = (
                session.query(UserModel)
                .filter_by(email=user_data["email"])
                .one_or_none()
            )

            if not user:
                log.warning(
                    "POST /auth/login - user not found for email=%s", user_data["email"]
                )
                abort(404, message="user not found")

            if not pbkdf2_sha256.verify(user_data["password"], user.password):
                log.warning(
                    "POST /auth/login - invalid credentials for email=%s",
                    user_data["email"],
                )
                abort(401, message="Invalid credentials")

            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            log.info("POST /auth/login - login successful for email=%s", user.email)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200


@blp.route("/auth/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        log.info("POST /auth/refresh - refreshing token for identity=%s", identity)

        access_token = create_access_token(identity=identity)

        log.info("POST /auth/refresh - access token issued for identity=%s", identity)

        return {"access_token": access_token}, 200


@blp.route("/auth/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        identity = get_jwt_identity()

        log.info("POST /auth/logout - logging out identity=%s, jti=%s", identity, jti)

        jwt_blocklist.add(jti)

        log.info("POST /auth/logout - logout successful for identity=%s", identity)

        return {"message": "Successfully logged out"}, 200
