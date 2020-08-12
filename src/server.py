# -*- coding: utf-8 -*-

from bottle.bottle import Bottle, run


class ChocolateServer(object):
    def __init__(self):
        self.server = Bottle()

    def register_app(self, chocolate_app):
        self.server.merge(chocolate_app.app)

    def run(self):
        run(self.server, host="localhost", port=8080)
