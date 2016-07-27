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

    def property(self, property_name):

        for item in self.__properties__:
            if item.name == property_name:
                return item.value
        return None

    def setting(self, setting_name):

        for item in self.__settings__:
            if item.name == setting_name:
                return item.value

        return None

    def update_properties(self, updated_properties):
        if len(self.__properties__) > 0:
            for sensor_property in self.__properties__:
                if sensor_property.name in updated_properties:
                    sensor_property.value = updated_properties[sensor_property.name]

    def update_settings(self, updated_settings):
        if len(self.__settings__) > 0:
            for sensor_setting in self.__settings__:
                if sensor_setting.name in updated_settings:
                    sensor_setting.value = updated_settings[sensor_setting.name]

    def copy(self):
        new_sensor = self.copy_with_info(self.id, self.name)
        return new_sensor

    def copy_with_info(self, new_id, new_name):
        new_sensor = Sensor(self.kind, new_id, new_name)
        for property_item in self.__properties__:
            new_property = SProperty(property_item.name, property_item.type, property_item.range, property_item.value)
            new_sensor.add_property(new_property)

        for setting_item in self.__settings__:
            new_setting = SSetting(setting_item.name, setting_item.type, setting_item.range,
                                   setting_item.value, setting_item.required)
            new_sensor.add_setting(new_setting)

        for action_item in self.__actions__:
            new_action = SAction(action_item.name)

            for setting_item in action_item.parameters:
                new_setting = SSetting(setting_item.name, setting_item.type, setting_item.range,
                                       setting_item.value, setting_item.required)
                new_action.parameters.append(new_setting)

            new_sensor.add_action(new_action)

        return new_sensor

    def copy_with_key(self, key):
        new_sensor = self.copy_with_info(key, self.name)
        return new_sensor