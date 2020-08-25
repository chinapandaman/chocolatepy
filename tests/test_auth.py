# -*- coding: utf-8 -*-

import time

import jwt
import pytest
from chocolatepy import ChocolateApp
from chocolatepy.auth import Auth
from pydal import DAL
from webtest import TestApp
from webtest.app import AppError


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


def test_auth_add_group(db):
    auth = Auth(db)

    role = "foo"
    description = "bar"

    group = (
        db(db.auth_group.id == auth.add_group(role, description))
        .select(db.auth_group.role, db.auth_group.description)
        .first()
    )

    assert group["role"] == role
    assert group["description"] == description


def test_auth_add_permission(db):
    auth = Auth(db)

    role = "foo"
    description = "bar"

    group_id = auth.add_group(role, description)

    permissions = [
        ("create", "foobar"),
        ("read", "foobar"),
        ("update", "foobar"),
        ("delete", "foobar"),
    ]

    for each in permissions:
        auth.add_permission(group_id, each[0], each[1])

    for each in db(db.auth_permission.group_id == group_id).select(
        db.auth_permission.name, db.auth_permission.table_name
    ):
        assert (each["name"], each["table_name"]) in permissions


def test_auth_add_membership(db):
    auth = Auth(db)

    groups = [("admin", "admin of the app"), ("user", "normal user")]

    username = "user"
    password = "password"

    user_id = auth.register(username, password)

    group_ids = []

    for each in groups:
        group_id = auth.add_group(each[0], each[1])
        auth.add_membership(group_id, user_id)
        group_ids.append(group_id)

    assert [
        each["group_id"]
        for each in db(db.auth_membership.user_id == user_id).select(
            db.auth_membership.group_id
        )
    ] == group_ids


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
    payload = jwt.decode(token, auth.jwt_secret, algorithms=[auth.jwt_alg])

    assert payload["sub"]["user_id"] == user_id


def test_auth_login_and_receive_token(db):
    auth = Auth(db)

    username = "foo"
    password = "bar"

    assert not auth.login(username, password)

    auth.register(username, password)
    assert auth.login(username, password)


def test_auth_decode_token(db):
    auth = Auth(db)

    username = "foo"
    password = "bar"

    user_id = auth.register(username, password)

    token = ""

    assert auth.decode_token(token) == "Invalid token."

    auth.jwt_exp = 1

    token = auth.login(username, password)

    time.sleep(5)

    assert auth.decode_token(token) == "Token expired."

    auth.jwt_exp = 3600

    token = auth.login(username, password)
    assert auth.decode_token(token)["user_id"] == user_id


@pytest.fixture
def app():
    app = ChocolateApp("app")

    @app.route("/")
    def index():
        app.auth.requires_login()
        return "app"

    @app.route("/foo")
    def foo():
        app.auth.requires_membership("admin")
        return "foo"

    @app.route("/bar")
    def bar():
        app.auth.requires_permission("read", "bar")
        return "bar"

    return app


def test_auth_requires_login(app):
    test_app = TestApp(app.app)

    try:
        test_app.get("/")
        assert False
    except AppError:
        assert True

    username = "foo"
    password = "bar"

    app.auth.register(username, password)

    token = app.auth.login(username, password)

    assert test_app.get("/", {"_token": token}).status == "200 OK"
    assert test_app.get("/", {"_token": token}).text == "app"


def test_auth_requires_membership(app):
    test_app = TestApp(app.app)

    username = "foo"
    password = "bar"

    user_id = app.auth.register(username, password)

    token = app.auth.login(username, password)

    try:
        test_app.get("/foo", {"_token": token})
        assert False
    except AppError:
        assert True

    group_id = app.auth.add_group("admin", "admin of the app")
    app.auth.add_membership(group_id, user_id)

    token = app.auth.login(username, password)

    assert test_app.get("/foo", {"_token": token}).status == "200 OK"
    assert test_app.get("/foo", {"_token": token}).text == "foo"


def test_auth_requires_permission(app):
    test_app = TestApp(app.app)

    username = "foo"
    password = "bar"

    user_id = app.auth.register(username, password)

    group_id = app.auth.add_group("developer", "developer of the app")
    app.auth.add_membership(group_id, user_id)

    token = app.auth.login(username, password)

    try:
        test_app.get("/bar", {"_token": token})
        assert False
    except AppError:
        assert True

    app.auth.add_permission(group_id, "read", "bar")
    token = app.auth.login(username, password)

    assert test_app.get("/bar", {"_token": token}).status == "200 OK"
    assert test_app.get("/bar", {"_token": token}).text == "bar"
