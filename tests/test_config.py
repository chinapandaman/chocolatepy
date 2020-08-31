# -*- coding: utf-8 -*-

from chocolatepy.config import ChocolateConfig


def test_set_config():
    app_config = ChocolateConfig("app_one")

    assert app_config.set_config("s1", "k1", "v1")
    assert app_config.set_config("s2", "k2", "v2")

    assert app_config.env.environ["app_one.s1.k1"] == "v1"
    assert app_config.env.environ["app_one.s2.k2"] == "v2"


def test_get_config():
    app_config = ChocolateConfig("app_two")

    app_config.set_config("s1", "k1", "v1")
    app_config.set_config("s2", "k2", "v2")

    assert app_config.get_config("s1", "k1") == "v1"
    assert app_config.get_config("s2", "k2") == "v2"

    assert not app_config.get_config("s5", "k5")


def test_config_as_dict():
    app_config = ChocolateConfig("app_three")

    app_config.set_config("s1", "k1", "v1")
    app_config.set_config("s2", "k2", "v2")

    assert app_config.as_dict() == {"s1": {"k1": "v1"}, "s2": {"k2": "v2"}}
