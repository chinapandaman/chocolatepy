# -*- coding: utf-8 -*-

import pytest
from chocolatepy import ChocolateApp, ChocolateServer, NonChocolateAppError
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


@pytest.fixture
def app_four():
    app = ChocolateApp("four")

    @app.route("/<value>")
    def index(value):
        return value

    return app


def test_register_apps(app_one, app_two, app_three, app_four):
    server = ChocolateServer()

    server.register_apps(app_one, app_two, app_three, app_four)

    app = TestApp(server.server)

    assert app.get("/one").status == "200 OK"
    assert app.get("/one").text == "one"

    assert app.get("/two").status == "200 OK"
    assert app.get("/two").text == "two"

    assert app.get("/three").status == "200 OK"
    assert app.get("/three").text == "three"

    assert app.get("/four/foo").status == "200 OK"
    assert app.get("/four/foo").text == "foo"

    assert app.get("/one").text == app.get("/").text


def test_register_apps_with_default_app(app_one, app_two, app_three, app_four):
    server = ChocolateServer()

    server.register_apps(app_one, app_three, app_four, default_app=app_two)

    app = TestApp(server.server)

    assert app.get("/two").text == app.get("/").text


def test_register_non_chocolate_app(app_one, app_two, app_three, app_four):
    server = ChocolateServer()

    bad_app = "app_five"

    try:
        server.register_apps(app_one, app_two, app_three, app_four, bad_app)
        assert False
    except NonChocolateAppError:
        assert True


def test_register_non_chocolate_app_as_default(app_one, app_two, app_three, app_four):
    server = ChocolateServer()

    bad_app = 5

    try:
        server.register_apps(app_one, app_two, app_three, app_four, default_app=bad_app)
        assert False
    except NonChocolateAppError:
        assert True
