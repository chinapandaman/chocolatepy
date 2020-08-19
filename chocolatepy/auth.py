# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import jwt
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

    def register(self, username, password):
        user_existed = len(
            self.db(self.db.auth_user.username == username).select(
                self.db.auth_user.username
            )
        )

        if user_existed:
            return False

        hashed_password = self.encrypt(password)
        self.db.auth_user.insert(**{"username": username, "password": hashed_password})
        self.db.commit()

        return True

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
