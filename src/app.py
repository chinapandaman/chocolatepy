# -*- coding: utf-8 -*-

from bottle.bottle import Bottle


class ChocolateApp(object):
    def __init__(self, app_name):
        self.app = Bottle()
        self.route = self.app.route
        self.app.mount("/{}".format(app_name), self.app)
