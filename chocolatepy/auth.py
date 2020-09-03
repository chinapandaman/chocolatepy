# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta

import jwt
from helper import ChocolateHelper
from pydal import Field
from pydal.validators import CRYPT

from bottle import abort, request


class Auth(object):
    def __init__(self, db):
        self.db = db
        self.env = os

        if os.name == "nt":
            import nt

            self.env = nt

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

    def add_group(self, role, description):
        group_id = self.db.auth_group.insert(
            **{"role": role, "description": description}
        )
        self.db.commit()
        return group_id

    def add_permission(self, group_id, name, table_name):
        permission_id = self.db.auth_permission.insert(
            **{"group_id": group_id, "name": name, "table_name": table_name}
        )
        self.db.commit()
        return permission_id

    def add_membership(self, group_id, user_id):
        self.db.auth_membership.insert(**{"user_id": user_id, "group_id": group_id})
        self.db.commit()
        return True

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

    def encrypt(self, string):
        return str(
            CRYPT(
                salt=self.env.environ.get(
                    "{}.{}.{}".format(
                        ChocolateHelper().current_app_name(), "auth", "password_salt"
                    )
                )
            )(string)[0]
        )

    def encode_token(self, user_id):
        group_ids = [
            each["group_id"]
            for each in self.db(self.db.auth_membership.user_id == user_id).select(
                self.db.auth_membership.group_id,
            )
        ]

        groups = [
            each["role"]
            for each in self.db(self.db.auth_group.id.belongs(group_ids)).select(
                self.db.auth_group.role
            )
        ]

        permissions = [
            {"name": each["name"], "table_name": each["table_name"]}
            for each in self.db(
                self.db.auth_permission.group_id.belongs(group_ids)
            ).select(self.db.auth_permission.name, self.db.auth_permission.table_name)
        ]

        payload = {
            "exp": datetime.utcnow()
            + timedelta(
                seconds=int(
                    self.env.environ.get(
                        "{}.{}.{}".format(
                            ChocolateHelper().current_app_name(), "auth", "jwt_exp"
                        )
                    )
                )
            ),
            "iat": datetime.utcnow(),
            "sub": {"user_id": user_id, "groups": groups, "permissions": permissions},
        }
        return jwt.encode(
            payload,
            self.env.environ.get(
                "{}.{}.{}".format(
                    ChocolateHelper().current_app_name(), "auth", "jwt_secret"
                )
            ),
            self.env.environ.get(
                "{}.{}.{}".format(
                    ChocolateHelper().current_app_name(), "auth", "jwt_alg"
                )
            ),
        )

    def decode_token(self, token):
        return ChocolateHelper().decode_token(
            token,
            self.env.environ.get(
                "{}.{}.{}".format(
                    ChocolateHelper().current_app_name(), "auth", "jwt_secret"
                )
            ),
            [
                self.env.environ.get(
                    "{}.{}.{}".format(
                        ChocolateHelper().current_app_name(), "auth", "jwt_alg"
                    )
                )
            ],
        )

    def is_logged_in(self):
        token = request.query.get("_token")

        sub = self.decode_token(token)

        if sub in ["Token expired.", "Invalid token."]:
            return False
        return sub

    def has_membership(self, role):
        sub = self.is_logged_in()

        if not isinstance(sub, dict):
            return False

        if role not in sub["groups"]:
            return False

        return sub

    def has_permission(self, name, table_name):
        sub = self.is_logged_in()

        if not isinstance(sub, dict):
            return False

        for each in sub["permissions"]:
            if name == each["name"] and table_name == each["table_name"]:
                return sub

        return False


class RequiresLogin(object):
    def __init__(self, f):
        self.f = f
        self.env = os

        if os.name == "nt":
            import nt

            self.env = nt

    def __call__(self, *args, **kwargs):
        token = request.query.get("_token")

        sub = ChocolateHelper().decode_token(
            token,
            self.env.environ.get(
                "{}.{}.{}".format(
                    ChocolateHelper().current_app_name(), "auth", "jwt_secret"
                )
            ),
            [
                self.env.environ.get(
                    "{}.{}.{}".format(
                        ChocolateHelper().current_app_name(), "auth", "jwt_alg"
                    )
                )
            ],
        )

        if sub in ["Token expired.", "Invalid token."]:
            abort(401, sub)

        return self.f(*args, **kwargs)


class RequiresMembership(object):
    def __init__(self, role):
        self.role = role
        self.env = os

        if os.name == "nt":
            import nt

            self.env = nt

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            token = request.query.get("_token")

            sub = ChocolateHelper().decode_token(
                token,
                self.env.environ.get(
                    "{}.{}.{}".format(
                        ChocolateHelper().current_app_name(), "auth", "jwt_secret"
                    )
                ),
                [
                    self.env.environ.get(
                        "{}.{}.{}".format(
                            ChocolateHelper().current_app_name(), "auth", "jwt_alg"
                        )
                    )
                ],
            )

            if sub in ["Token expired.", "Invalid token."]:
                abort(401, sub)

            if self.role not in sub["groups"]:
                abort(401, "Invalid membership.")

            return f(*args, **kwargs)

        return wrapped_f


class RequiresPermission(object):
    def __init__(self, name, table_name):
        self.name = name
        self.table_name = table_name
        self.env = os

        if os.name == "nt":
            import nt

            self.env = nt

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            token = request.query.get("_token")

            sub = ChocolateHelper().decode_token(
                token,
                self.env.environ.get(
                    "{}.{}.{}".format(
                        ChocolateHelper().current_app_name(), "auth", "jwt_secret"
                    )
                ),
                [
                    self.env.environ.get(
                        "{}.{}.{}".format(
                            ChocolateHelper().current_app_name(), "auth", "jwt_alg"
                        )
                    )
                ],
            )

            if sub in ["Token expired.", "Invalid token."]:
                abort(401, sub)

            if not isinstance(sub, dict):
                abort(401)

            for each in sub["permissions"]:
                if self.name == each["name"] and self.table_name == each["table_name"]:
                    return f(*args, **kwargs)

            abort(401, "Invalid Permission.")

        return wrapped_f


class Requires(object):
    def __init__(self, expression):
        self.expression = expression

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            if not self.expression:
                abort(401)

            return f(*args, **kwargs)

        return wrapped_f
