# -*- coding: utf-8 -*-

import jwt

from bottle import request


class ChocolateHelper(object):
    @staticmethod
    def current_app_name():
        return request.route.app.routes[0].config.mountpoint.prefix.split("/")[1]

    @staticmethod
    def decode_token(token, secret, alg):
        try:
            payload = jwt.decode(token, secret, algorithms=alg,)
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Token expired."
        except jwt.InvalidTokenError:
            return "Invalid token."
