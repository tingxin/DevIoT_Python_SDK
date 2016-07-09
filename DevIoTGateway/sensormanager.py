__author__ = 'tingxxu'
from singleton import Singleton
from sensor import Sensor, SProperty, SAction
import sys
import json


class SensorManager(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.__sensors__ = {}
        self.__actions__ = {}

    def add_read_sensor(self, sensor_kind, sensor_id, sensor_name):
        if sensor_id in self.__sensors__:
            raise ValueError("{0} have been added".format(sensor_id))
            return
        new_sensor = Sensor(sensor_kind, sensor_id, sensor_name)
        value_property = SProperty("value", 0, None, 0)
        new_sensor.add_property(value_property)
        self.__sensors__[sensor_id] = new_sensor

    def add_action_sensor(self, sensor_kind, sensor_id, sensor_name, action_function):
        if sensor_id in self.__sensors__:
            raise ValueError("{0} have been added".format(sensor_id))
            return
        new_sensor = Sensor(sensor_kind, sensor_id, sensor_name)
        action_on = SAction("on")
        action_off = SAction("off")
        new_sensor.add_action(action_on)
        new_sensor.add_action(action_off)
        self.__sensors__[sensor_id] = new_sensor
        self.__actions__[sensor_id] = action_function

    def add_custom_sensor(self, sensor):
        if sensor.id in self.__sensors__:
            raise ValueError("{0} have been added".format(sensor.id))
            return
        if isinstance(sensor, Sensor):
            self.__sensors__[sensor.id] = sensor
        else:
            raise ValueError("argument should be the instance of Sensor")

    def update_sensor(self, sensor_id, new_value):
        if sensor_id in self.__sensors__:
            sensor = self.__sensors__[sensor_id]
            if len(sensor.__properties__) > 0:
                for sensor_property in sensor.__properties__:
                    if sensor_property.name == "value":
                        sensor_property.value = new_value

    def update_custom_sensor(self, sensor_id, properties):
        if sensor_id in self.__sensors__:
            sensor = self.__sensors__[sensor_id]
            if len(sensor.__properties__) > 0:
                for sensor_property in sensor.__properties__:
                    if sensor_property.name in properties:
                        sensor_property.value = properties[sensor_property.name]

    def __trigger_action__(self, sensor_id, action):
        if sensor_id in self.__actions__:
            self.__actions__[sensor_id](action)

    def get_sensors_data(self):
        data = {}
        try:
            for sensor_id in self.__sensors__:
                sensor = self.__sensors__[sensor_id]
                if len(sensor.__properties__) > 0:
                    data[sensor_id] = self.__get_sensor_value_expression(sensor)
        except:
            print("sensor manager get_sensors_data ", sys.exc_info()[1])
        return json.dumps(data)

    def get_all_expression(self):
        result = []
        for sensor_id in self.__sensors__:
            sensor = self.__sensors__[sensor_id]
            expression = SensorManager.__get_sensor_expression(sensor)
            result.append(expression)
        return result

    def __get_sensor_value_expression(self, sensor):
        expression = {}

        for property_item in sensor.__properties__:
            expression[property_item.name] = property_item.value
        return expression

    @staticmethod
    def __get_sensor_expression(sensor):
        expression = {}
        expression["id"] = sensor.id
        expression["name"] = sensor.name
        expression["kind"] = sensor.kind
        expression["properties"] = []
        expression["actions"] = []
        expression["settings"] = []

        for property_item in sensor.__properties__:
            expression["properties"].append({
                "name": property_item.name,
                "type": property_item.type,
                "range": property_item.range,
                "value": property_item.value,
                "description": property_item.description
            })

        for action_item in sensor.__actions__:
            action = {}
            action["name"] = action_item.name
            action["parameters"] = []
            for parameter_item in action_item.parameters:
                parameter = {
                    "name": parameter_item.name,
                    "type": parameter_item.type,
                    "range": parameter_item.range,
                    "value": parameter_item.value,
                    "description": parameter_item.description,
                    "required": parameter_item.required
                }
                action["parameters"].append(parameter)

            expression["actions"].append(action)

        for setting_item in sensor.__settings__:
            expression["settings"].append({
                "name": setting_item.name,
                "type": setting_item.type,
                "range": setting_item.range,
                "value": setting_item.value,
                "description": setting_item.description,
                "required": setting_item.required
            })

        return expression

# -------------------------------------------------------------------------------- #

manager = SensorManager()
