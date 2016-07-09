__author__ = 'tingxxu'
from sproperty import SProperty
from saction import SAction
from ssetting import SSetting

class Sensor:

    def __init__(self, sensor_kind, sensor_id, sensor_name):
        self.kind = sensor_kind
        self.id = sensor_id
        self.name = sensor_name
        self.__properties__ = []
        self.__settings__ = []
        self.__actions__ = []

    def add_property(self, sensor_property):
        if isinstance(sensor_property, SProperty):
            self.__properties__.append(sensor_property)
        else:
            raise ValueError("sensor_property should be type of SProperty")

    def add_action(self, sensor_action):
        if isinstance(sensor_action, SAction):
            self.__actions__.append(sensor_action)
        else:
            raise ValueError("sensor_action should be type of SAction")

    def add_setting(self, sensor_setting):
        if isinstance(sensor_setting, SSetting):
            self.__settings__.append(sensor_setting)
        else:
            raise ValueError("sensor_setting should be type of SSetting")