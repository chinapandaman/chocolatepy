# -*- coding: utf-8 -*-

import jwt
import pytest
from chocolatepy.auth import Auth
from pydal import DAL


@pytest.fixture
def db():
    return DAL("sqlite:memory")


def test_auth_tables(db):
    auth = Auth(db)

    for each in ["auth_user", "auth_group", "auth_permission", "auth_membership"]:
        assert each in auth.db.tables


def test_auth_user_fields(db):
    auth = Auth(db)

    assert auth.db.auth_user.username.type == "string"
    assert auth.db.auth_user.username.length == 512

    assert auth.db.auth_user.password.type == "password"


def test_auth_group_fields(db):
    auth = Auth(db)

    assert auth.db.auth_group.role.type == "string"
    assert auth.db.auth_group.role.length == 512

    assert auth.db.auth_group.description.type == "text"


def test_auth_permission_fields(db):
    auth = Auth(db)

    assert auth.db.auth_permission.group_id.type == "reference auth_group"

    assert auth.db.auth_permission.name.type == "string"
    assert auth.db.auth_permission.name.length == 512

    assert auth.db.auth_permission.table_name.type == "string"
    assert auth.db.auth_permission.table_name.length == 512


def test_auth_membership_fields(db):
    auth = Auth(db)

    assert auth.db.auth_membership.user_id.type == "reference auth_user"

    assert auth.db.auth_membership.group_id.type == "reference auth_group"


def test_auth_register(db):
    auth = Auth(db)

    username = "foo"
    password = "bar"

    assert auth.register(username=username, password=password)

    user = db(db.auth_user.username == username).select().first()

    assert user
    assert username == user.username
    assert auth.encrypt(password) == user.password


def test_auth_register_existed_user(db):
    auth = Auth(db)

    username = "foo"
    password = "bar"

    assert auth.register(username=username, password=password)
    assert not auth.register(username=username, password=password)


def test_auth_encode_token(db):
    auth = Auth(db)

    user_id = 1

    token = auth.encode_token(user_id)
    payload = jwt.decode(token, auth.jwt_secret)

    assert payload["sub"] == user_id


def test_auth_login_and_receive_token(db):
    auth = Auth(db)

    username = "foo"
    password = "bar"

    assert not auth.login(username, password)

    auth.register(username, password)
    assert auth.login(username, password)
