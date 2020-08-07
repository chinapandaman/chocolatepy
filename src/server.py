# -*- coding: utf-8 -*-

from bottle.bottle import Bottle


class ChocolateServer(object):
    def __init__(self):
        self.server = Bottle()

    def register_app(self, chocolate_app):
        self.server.merge(chocolate_app.app)
