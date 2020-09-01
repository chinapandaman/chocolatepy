# -*- coding: utf-8 -*-

from bottle import request


class ChocolateHelper(object):
    @staticmethod
    def current_app_name():
        return request.app.routes[0].config.mountpoint.prefix.split("/")[1]
