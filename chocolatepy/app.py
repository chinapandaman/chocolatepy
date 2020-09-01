# -*- coding: utf-8 -*-

from auth import Auth
from config import ChocolateConfig
from pydal import DAL

from bottle import Bottle


class ChocolateApp(object):
    def __init__(self, app_name):
        self.name = app_name
        self.app = Bottle()
        self.route = self.app.route
        self.app.mount("/{}".format(app_name), self.app)

        self.db = DAL("sqlite:memory")
        self.auth = Auth(db=self.db)

        self.config = ChocolateConfig(self.name)
        self.config.set_config(section="auth", key="jwt_secret", value="secret")
        self.config.set_config(section="auth", key="jwt_exp", value="3600")
        self.config.set_config(section="auth", key="jwt_alg", value="HS256")
