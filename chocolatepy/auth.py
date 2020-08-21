# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import jwt
from bottle import abort, request
from pydal import Field
from pydal.validators import CRYPT


class Auth(object):
    def __init__(self, db):
        self.db = db

        self.db.define_table(
            "auth_user",
            Field("username", length=512, unique=True),
            Field("password", type="password"),
        )
        self.db.define_table(
            "auth_group", Field("role", length=512), Field("description", type="text")
        )
        self.db.define_table(
            "auth_permission",
            Field("group_id", "reference auth_group"),
            Field("name", length=512),
            Field("table_name", length=512),
        )
        self.db.define_table(
            "auth_membership",
            Field("user_id", "reference auth_user"),
            Field("group_id", "reference auth_group"),
        )

        self.jwt_secret = "secret"
        self.jwt_exp = 3600
        self.jwt_alg = "HS256"

    def create_group(self, role, description):
        group_id = self.db.auth_group.insert(
            **{"role": role, "description": description}
        )
        self.db.commit()
        return group_id

    def register(self, username, password):
        user_existed = len(
            self.db(self.db.auth_user.username == username).select(
                self.db.auth_user.username
            )
        )

        if user_existed:
            return False

        hashed_password = self.encrypt(password)
        user_id = self.db.auth_user.insert(
            **{"username": username, "password": hashed_password}
        )
        self.db.commit()

        return user_id

    def login(self, username, password):
        user = (
            self.db(
                (self.db.auth_user.username == username)
                & (self.db.auth_user.password == self.encrypt(password))
            )
            .select(self.db.auth_user.id)
            .first()
        )

        if not user:
            return False

        return self.encode_token(user["id"])

    @staticmethod
    def encrypt(string):
        return str(CRYPT(salt=False)(string)[0])

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(seconds=self.jwt_exp),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.jwt_secret, self.jwt_alg)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_alg])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Token expired."
        except jwt.InvalidTokenError:
            return "Invalid token."

    def requires_login(self):
        token = request.query.get("_token")

        sub = self.decode_token(token)

        if sub in ["Token expired.", "Invalid token."]:
            abort(401, sub)
        return sub
