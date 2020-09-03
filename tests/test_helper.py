# -*- coding: utf-8 -*-


import time
from datetime import datetime, timedelta

import jwt
import pytest
from chocolatepy import ChocolateApp, ChocolateServer
from helper import ChocolateHelper
from webtest import TestApp


@pytest.fixture
def app_one():
    app = ChocolateApp("one")

    @app.route("/")
    def index():
        return "one"

    return app


@pytest.fixture
def app_two():
    app = ChocolateApp("two")

    @app.route("/")
    def index():
        return "two"

    return app


def test_current_app_name(app_one, app_two):
    server = ChocolateServer()

    server.register_apps(app_one, app_two, default_app=app_two)

    app = TestApp(server.server)

    assert app.get("/").status == "200 OK"

    assert ChocolateHelper().current_app_name() == app_two.name

    assert app.get("/one").status == "200 OK"

    assert ChocolateHelper().current_app_name() == app_one.name

    assert app.get("/two").status == "200 OK"

    assert ChocolateHelper().current_app_name() == app_two.name


def test_decode_token():
    token = ""

    assert (
        ChocolateHelper().decode_token(token, "secret", ["HS256"]) == "Invalid token."
    )

    payload = {
        "exp": datetime.utcnow() + timedelta(seconds=1),
        "iat": datetime.utcnow(),
        "sub": 4,
    }

    token = jwt.encode(payload, "secret", "HS256")

    time.sleep(5)

    assert (
        ChocolateHelper().decode_token(token, "secret", ["HS256"]) == "Token expired."
    )

    payload = {
        "exp": datetime.utcnow() + timedelta(seconds=3600),
        "iat": datetime.utcnow(),
        "sub": 5,
    }

    token = jwt.encode(payload, "secret", "HS256")

    assert ChocolateHelper().decode_token(token, "secret", ["HS256"]) == 5
