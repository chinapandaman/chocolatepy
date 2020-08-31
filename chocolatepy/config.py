# -*- coding: utf-8 -*-

import nt


class ChocolateConfig(object):
    def __init__(self, app_name):
        self.app_name = app_name

    def set_config(self, section, key, value):
        nt.environ["{}.{}.{}".format(self.app_name, section, key)] = value

        return True

    def get_config(self, section, key):
        return nt.environ.get("{}.{}.{}".format(self.app_name, section, key))

    def as_dict(self):
        result = {}

        for k, v in nt.environ.items():
            if k.startswith("{}.".format(self.app_name)):
                config = k.split("{}.".format(self.app_name))[-1]
                section, key = config.split(".")

                if section not in result:
                    result[section] = {}

                result[section][key] = v

        return result
