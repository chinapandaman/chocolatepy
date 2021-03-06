# -*- coding: utf-8 -*-

from auth import Auth
from config import ChocolateConfig
from pydal import DAL

from bottle import Bottle


class BaseAppException(Exception):
    """Base Exception for ChocolateApp"""

    pass


class InvalidPyDALParameterError(BaseAppException):
    """Raised when constructing app's DAL with invalid parameters"""

    pass


class InvalidAuthSettingsError(BaseAppException):
    """Raised when setting app's auth config with invalid parameters"""

    pass


class DatabaseNotEnabledError(BaseAppException):
    """Raised when enabling other properties of app that need db without enabling db"""

    pass


class ChocolateApp(object):
    def __init__(
        self,
        app_name,
        db_enabled=True,
        db_settings=None,
        auth_enabled=True,
        auth_settings=None,
    ):
        self.name = app_name
        self.app = Bottle()
        self.route = self.app.route
        self.app.mount("/{}".format(app_name), self.app)

        self.config = ChocolateConfig(self.name)

        if not db_enabled:
            if any([db_settings, auth_enabled, auth_settings]):
                raise DatabaseNotEnabledError

        self.db = None
        if db_enabled:
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
                    after_connection=db_settings.get("after_connection"),
                    tables=db_settings.get("tables"),
                    ignore_field_case=db_settings.get("ignore_field_case", True),
                    entity_quoting=db_settings.get("entity_quoting", False),
                    table_hash=db_settings.get("table_hash"),
                )
            else:
                self.db = DAL("sqlite:memory")

        self.auth = None
        if auth_enabled:
            self.auth = Auth(db=self.db)

            auth_config = {}
            if auth_settings and self.validate_auth_settings(auth_settings):
                auth_config = auth_settings

            self.config.set_config(
                section="auth",
                key="jwt_secret",
                value=auth_config.get("jwt_secret", "secret"),
            )
            self.config.set_config(
                section="auth",
                key="jwt_exp",
                value=str(auth_config.get("jwt_exp", 3600)),
            )
            self.config.set_config(
                section="auth", key="jwt_alg", value=auth_config.get("jwt_alg", "HS256")
            )
            self.config.set_config(
                section="auth",
                key="password_salt",
                value=auth_config.get("password_salt", "salt"),
            )

    @staticmethod
    def validate_auth_settings(auth_settings):
        if not isinstance(auth_settings, dict):
            raise InvalidAuthSettingsError

        acceptable_params = ["jwt_secret", "jwt_exp", "jwt_alg", "password_salt"]

        for each in auth_settings:
            if each not in acceptable_params:
                raise InvalidAuthSettingsError
            if each == "jwt_exp":
                if not isinstance(auth_settings[each], int):
                    raise InvalidAuthSettingsError
            elif not isinstance(auth_settings[each], str):
                raise InvalidAuthSettingsError

        return True

    @staticmethod
    def validate_pydal_parameters(pydal_params):
        if not isinstance(pydal_params, dict):
            raise InvalidPyDALParameterError

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
            "after_connection",
            "tables",
            "ignore_field_case",
            "entity_quoting",
            "table_hash",
        ]

        for each in pydal_params:
            if each not in acceptable_params:
                raise InvalidPyDALParameterError

        return True
