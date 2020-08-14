# -*- coding: utf-8 -*-

from bottle import Bottle, run

from app import ChocolateApp


class NonChocolateAppError(Exception):
    """Raised when attempting to register a non-chocolate app"""

    def __init__(self, message=""):
        super().__init__(message)
        self.message = message


class ChocolateServer(object):
    def __init__(self):
        self.server = Bottle()

    def register_apps(self, *args, **kwargs):
        default_app = None

        for k, v in kwargs.items():
            if k == "default_app":
                if not isinstance(v, ChocolateApp):
                    raise NonChocolateAppError(
                        "Attempt to register: {}".format(type(v))
                    )
                default_app = v

        for each in reversed(args):
            if not isinstance(each, ChocolateApp):
                raise NonChocolateAppError("Attempt to register: {}".format(type(each)))

            if each == default_app:
                continue

            self.server.merge(each.app)

        if default_app:
            self.server.merge(default_app.app)

    def run(self):
        run(self.server, host="localhost", port=8080)
