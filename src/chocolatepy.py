# -*- coding: utf-8 -*-

from bottle.bottle import run
from server import ChocolateServer

if __name__ == "__main__":
    server = ChocolateServer()
    run(server.server, host="localhost", port=8080)
