# -*- coding: utf-8 -*-
from bottle.bottle import Bottle


class ChocolateServer(object):
    def __init__(self):
        self.server = Bottle()
