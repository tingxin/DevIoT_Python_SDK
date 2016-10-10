__author__ = 'tingxxu'
from singleton import Singleton
from sensor import Sensor, SProperty, SAction, SSetting
import sys
import json


class SensorManager(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.__sensors__ = {}
        self.__actions__ = {}
        self.__kind_action__ = {}

    def add_read_sensor(self, sensor_kind, sensor_id, sensor_name):
        if sensor_id in self.__sensors__:
            raise ValueError("{0} have been added".format(sensor_id))
            return
        new_sensor = Sensor(sensor_kind, sensor_id, sensor_name)
        value_property = SProperty("value", 0, None, 0)
        new_sensor.add_property(value_property)
        self.__sensors__[sensor_id] = new_sensor

    def add_action_sensor(self, sensor_kind, sensor_id, sensor_name, action_function=None):
        if sensor_id in self.__sensors__:
            raise ValueError("{0} have been added".format(sensor_id))
            return
        new_sensor = Sensor(sensor_kind, sensor_id, sensor_name)
        action_on = SAction("on")
        action_off = SAction("off")
        new_sensor.add_action(action_on)
        new_sensor.add_action(action_off)
        self.__sensors__[sensor_id] = new_sensor

        if action_function is not None:
            self.__actions__[sensor_id] = action_function

    def add_custom_sensor(self, sensor):
        self.add_custom_sensor_with_action(sensor, None)

    def add_custom_sensor_with_action(self, sensor, action):
        if sensor.id in self.__sensors__:
            raise ValueError("{0} have been added".format(sensor.id))
            return
        if isinstance(sensor, Sensor):
            self.__sensors__[sensor.id] = sensor
            if action is not None:
                self.__actions__[sensor.id] = action
        else:
            raise ValueError("argument should be the instance of Sensor")

    def register_callback_for_kind(self, kind, callback):
        if callback is not None:
            self.__kind_action__[kind] = callback

    def update_sensor(self, sensor_id, new_value):
        if sensor_id in self.__sensors__:
            sensor = self.__sensors__[sensor_id]
            properties = {"value": new_value}
            sensor.update_properties(properties)

    def update_custom_sensor(self, sensor_id, properties):
        if sensor_id in self.__sensors__:
            sensor = self.__sensors__[sensor_id]
            sensor.update_properties(properties)

    def get_sensor(self, sensor_id):
        return self.__sensors__[sensor_id]

    def has_sensor(self, sensor_id):
        return sensor_id in self.__sensors__

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

    def __on_message__(self, message):
        try:
            command_dictionary = json.loads(message)
            if "name" in command_dictionary:

                sensor_id = command_dictionary["name"]
                if sensor_id in self.__sensors__:
                    target_sensor = self.__sensors__[sensor_id]
                    if "action" in command_dictionary:
                        # trigger action
                        action = SAction(command_dictionary['action'])
                        for key in command_dictionary:
                            if key != "name" and key != "action":
                                setting = SSetting(key, 0, [0, 100], command_dictionary[key], True)
                                action.add_setting(setting)
                        try:
                            self.__trigger_action__(sensor_id, action)
                            self.__trigger_kind_action__(sensor_id, action)
                        except:
                            res = "{\"result\":\"%s\"}" % sys.exc_info()[1]
                            print(res)
                    else:
                        # update setting
                        target_sensor.update_settings(command_dictionary)
                else:
                    # create a new sensor
                    if "kind" in command_dictionary:
                        kind = command_dictionary["kind"]
                    else:
                        kind = None

                    founded = False
                    for key in self.__sensors__:
                        sensor = self.__sensors__[key]
                        if (kind is not None and sensor.kind == kind) or sensor.kind in sensor_id:
                            founded = True
                            new_sensor = sensor.copy_with_key(sensor_id)

                            new_sensor.update_settings(command_dictionary)
                            self.add_custom_sensor(new_sensor)
                            break
                    if founded is False:
                        raise ValueError("Does not support {0}".format(kind))
            else:
                print("Bad Command from DevIot: %s" % message)
        except:
            res = "command format error: %s" % message
            print(res)

    def __get_sensor_value_expression(self, sensor):
        expression = {}

        for property_item in sensor.__properties__:
            expression[property_item.name] = property_item.value
        return expression

    def __trigger_action__(self, sensor_id, action):
        if sensor_id in self.__actions__:
            self.__actions__[sensor_id](sensor_id, action)

    def __trigger_kind_action__(self, sensor_id, action):
        if sensor_id in self.__sensors__:
            sensor = self.__sensors__[sensor_id]

            if sensor.kind in self.__kind_action__:
                self.__kind_action__[sensor.kind](sensor.id, action)


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
                "unit": property_item.unit,
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
                    "unit": parameter_item.unit,
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
                "unit": setting_item.unit,
                "description": setting_item.description,
                "required": setting_item.required
            })

        return expression

# -------------------------------------------------------------------------------- #

manager = SensorManager()
