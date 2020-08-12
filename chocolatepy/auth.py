# -*- coding: utf-8 -*-

from pydal.pydal import Field


class Auth(object):
    def __init__(self, db):
        self.db = db

        self.db.define_table(
            "auth_user",
            Field("username", length=512),
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
