# -*- coding: utf-8 -*-

import pytest
from chocolatepy import ChocolateApp
from webtest import TestApp


@pytest.fixture
def app():
    app = ChocolateApp("app")

    @app.route("/")
    def index():
        return "app"

    return app


def test_app_init(app):
    assert app.name == "app"

    test_app = TestApp(app.app)

    assert test_app.get("/app").status == "200 OK"
    assert test_app.get("/app").text == "app"

    assert test_app.get("/app").text == test_app.get("/").text
