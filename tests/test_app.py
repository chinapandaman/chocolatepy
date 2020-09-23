# -*- coding: utf-8 -*-

import pytest
from chocolatepy import ChocolateApp, InvalidPyDALParameterError
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


def test_app_db_settings():
    try:
        ChocolateApp("test_db", db_settings="not a dict")
    except InvalidPyDALParameterError:
        assert True

    try:
        ChocolateApp("test_db", db_settings={"random_setting": True})
    except InvalidPyDALParameterError:
        assert True

    app = ChocolateApp("test_db", db_settings={"pool_size": 10, "debug": True})

    assert app.db._uri == "sqlite:memory"
    assert app.db._pool_size == 10
    assert not app.db._folder
    assert app.db._db_codec == "UTF-8"
    assert not app.db._check_reserved
    assert app.db._migrate
    assert not app.db._fake_migrate
    assert app.db._migrate_enabled
    assert not app.db._fake_migrate_all
    assert not app.db._decode_credentials
    assert not app.db._driver_args
    assert not app.db._adapter_args
    assert app.db._attempts == 5
    assert not app.db._bigint_id
    assert app.db._debug
    assert not app.db._lazy_tables
    assert not app.db._db_uid
    assert len(app.db._tables) == 4
    assert app.db._ignore_field_case
