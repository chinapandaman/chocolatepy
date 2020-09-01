# -*- coding: utf-8 -*-


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
