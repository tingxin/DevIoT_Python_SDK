__author__ = 'tingxxu'
from ssetting import SSetting


class SAction:

    def __init__(self, s_name):
        self.name = s_name
        self.parameters = []

    def add_setting(self, setting):
        if isinstance(setting, SSetting):
            self.parameters.append(setting)
        else:
            raise ValueError("setting should be type of SSetting")



