# -*- coding: utf-8 -*-

from bottle import Bottle
from pydal import DAL

from auth import Auth
from config import ChocolateConfig


class BaseAppException(Exception):
    """Base Exception for ChocolateServer"""

    pass


class InvalidPyDALParameterError(BaseAppException):
    """Raised when constructing app's pydal with invalid parameters"""

    pass


class ChocolateApp(object):
    def __init__(self, app_name, db_settings=None):
        self.name = app_name
        self.app = Bottle()
        self.route = self.app.route
        self.app.mount("/{}".format(app_name), self.app)

        if db_settings and self.validate_pydal_parameters(db_settings):
            self.db = DAL(
                uri=db_settings.get("uri", "sqlite:memory"),
                pool_size=db_settings.get("pool_size", 0),
                folder=db_settings.get("folder"),
                db_codec=db_settings.get("db_codec", "UTF-8"),
                check_reserved=db_settings.get("check_reserved"),
                migrate=db_settings.get("migrate", True),
                fake_migrate=db_settings.get("fake_migrate", False),
                migrate_enabled=db_settings.get("migrate_enabled", True),
                fake_migrate_all=db_settings.get("fake_migrate_all", False),
                decode_credentials=db_settings.get("decode_credentials", False),
                driver_args=db_settings.get("driver_args"),
                adapter_args=db_settings.get("adapter_args"),
                attempts=db_settings.get("attempts", 5),
                auto_import=db_settings.get("auto_import", False),
                bigint_id=db_settings.get("bigint_id", False),
                debug=db_settings.get("debug", False),
                lazy_tables=db_settings.get("lazy_tables", False),
                db_uid=db_settings.get("db_uid"),
                do_connect=db_settings.get("do_connect", True),
                after_connection=db_settings.get("after_connection"),
                tables=db_settings.get("tables"),
                ignore_field_case=db_settings.get("ignore_field_case", True),
                entity_quoting=db_settings.get("entity_quoting", False),
                table_hash=db_settings.get("table_hash"),
            )
        else:
            self.db = DAL("sqlite:memory")

        self.auth = Auth(db=self.db)

        self.config = ChocolateConfig(self.name)
        self.config.set_config(section="auth", key="jwt_secret", value="secret")
        self.config.set_config(section="auth", key="jwt_exp", value="3600")
        self.config.set_config(section="auth", key="jwt_alg", value="HS256")
        self.config.set_config(section="auth", key="password_salt", value="salt")

    @staticmethod
    def validate_pydal_parameters(pydal_params):
        acceptable_params = [
            "uri",
            "pool_size",
            "folder",
            "db_codec",
            "check_reserved",
            "migrate",
            "fake_migrate",
            "migrate_enabled",
            "fake_migrate_all",
            "decode_credentials",
            "driver_args",
            "adapter_args",
            "attempts",
            "auto_import",
            "bigint_id",
            "debug",
            "lazy_tables",
            "db_uid",
            "do_connect",
            "after_connection",
            "tables",
            "ignore_field_case",
            "entity_quoting",
            "table_hash",
        ]

        for each in pydal_params:
            if not each in acceptable_params:
                raise InvalidPyDALParameterError

        return True
