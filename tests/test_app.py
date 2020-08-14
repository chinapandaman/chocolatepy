# -*- coding: utf-8 -*-

import pytest
from chocolatepy import ChocolateApp


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


def test_app_init(app_one, app_two, app_three):
    assert app_one.name == "one"
    assert app_two.name == "two"
    assert app_three.name == "three"
