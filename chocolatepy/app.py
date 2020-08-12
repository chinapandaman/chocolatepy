# -*- coding: utf-8 -*-

from auth import Auth
from bottle.bottle import Bottle
from pydal.pydal import DAL


class ChocolateApp(object):
    def __init__(self, app_name):
        self.name = app_name
        self.app = Bottle()
        self.route = self.app.route
        self.app.mount("/{}".format(app_name), self.app)

        self.db = DAL("sqlite:memory")
        self.auth = Auth(db=self.db)
