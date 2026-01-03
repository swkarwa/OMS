import logging
from typing import Any
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from models import User as UserModel
from models.base import get_session
from schemas import UserBaseSchema as UserSchema, UserOrderSchema

log = logging.getLogger(__name__)
blp = Blueprint("user", __name__, "operation on user")


@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        log.info("GET /users - fetching all users")

        with get_session() as session:
            users = session.query(UserModel).all()
            log.info("GET /users - fetched %d users", len(users))
            return users

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        log.info("POST /users - creating user")

        user: Any[UserModel] = UserModel(**user_data)
        user.password = pbkdf2_sha256.hash(user_data["password"])

        with get_session() as session:
            session.add(user)
            log.info("POST /users - user created successfully")
            return user


@blp.route("/user/<int:user_id>")
class UserOperation(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        log.info("GET /user/%s - fetching user", user_id)

        with get_session() as session:
            user = session.get(UserModel, user_id)
            if not user:
                log.warning("GET /user/%s - user not found", user_id)
                abort(404, message="resource not found")

            log.info("GET /user/%s - user fetched successfully", user_id)
            return user

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        log.info("PUT /user/%s - updating user", user_id)

        with get_session() as session:
            user = session.get(UserModel, user_id)
            if not user:
                log.warning("PUT /user/%s - user not found", user_id)
                abort(404, message="user not found")

            for f, v in user_data.items():
                if f == "password":
                    v = pbkdf2_sha256.hash(v)
                setattr(user, f, v)

            log.info("PUT /user/%s - user updated successfully", user_id)
            return user

    @blp.response(204, description="Resource deleted")
    def delete(self, user_id):
        log.info("DELETE /user/%s - deleting user", user_id)

        with get_session() as session:
            user = session.get(UserModel, user_id)
            if not user:
                log.warning("DELETE /user/%s - user not found", user_id)
                abort(404, message="resource not found")

            session.delete(user)
            log.info("DELETE /user/%s - user deleted successfully", user_id)


@blp.route("/user/<int:user_id>/orders")
class UserOrder(MethodView):
    @blp.response(200, UserOrderSchema(many=True))
    def get(self, user_id):
        log.info("GET /user/%s/orders - fetching user orders", user_id)

        with get_session() as session:
            user = session.get(UserModel, user_id)
            if not user:
                log.warning("GET /user/%s/orders - user not found", user_id)
                abort(404, message="user not found")

            log.info(
                "GET /user/%s/orders - fetched %d orders", user_id, len(user.orders)
            )
            return user.orders
