# -*- coding: utf-8 -*-

import pytest
from chocolatepy import ChocolateApp, ChocolateServer
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


@pytest.fixture
def app_three():
    app = ChocolateApp("three")

    @app.route("/")
    def index():
        return "three"

    return app


def test_register_apps(app_one, app_two, app_three):
    server = ChocolateServer()

    server.register_apps(app_one, app_two, app_three)

    app = TestApp(server.server)

    assert app.get("/one").status == "200 OK"
    assert app.get("/one").text == "one"

    assert app.get("/two").status == "200 OK"
    assert app.get("/two").text == "two"

    assert app.get("/three").status == "200 OK"
    assert app.get("/three").text == "three"

    assert app.get("/one").text == app.get("/").text


def test_register_apps_with_default_app(app_one, app_two, app_three):
    server = ChocolateServer()

    server.register_apps(app_one, app_three, default_app=app_two)

    app = TestApp(server.server)

    assert app.get("/two").text == app.get("/").text


def test_register_non_chocolate_app(app_one, app_two, app_three):
    server = ChocolateServer()

    bad_app = "app_four"

    try:
        server.register_apps(app_one, app_two, app_three, bad_app)
    except Exception as e:
        assert e.message == "Attempt to register: {}".format(type(bad_app))


def test_register_non_chocolate_app_as_default(app_one, app_two, app_three):
    server = ChocolateServer()

    bad_app = 4

    try:
        server.register_apps(app_one, app_two, app_three, default_app=bad_app)
    except Exception as e:
        assert e.message == "Attempt to register: {}".format(type(bad_app))
