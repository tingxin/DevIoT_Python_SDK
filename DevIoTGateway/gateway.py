_author__ = 'tingxxu'

from mqclient import MQClient
from register import Register
from singleton import Singleton
from sensormanager import manager

__main_manager__ = []


class Gateway(Singleton):

    def __init__(self, app_name, iot_address, mqtt_address, deviot_account):

        self.app_name = app_name
        self.iot_address = iot_address

        self.is_virtual = False
        self.deviot_account = deviot_account
        self.mqtt_address = mqtt_address

    def run(self):
        try:
            mqtt_info = self.mqtt_address.split(":")
            server_host = mqtt_info[0]
            port = int(mqtt_info[1])
        except:
            print("the format of mqtt host should be: ip:port")
            return

        register = Register(self.app_name, manager, self.iot_address, server_host,
                            port, self.deviot_account, True, self.is_virtual)
        register.port = port
        register.start()

        mqtt_listener = MQClient(server_host, port, register.MQData_topic, register.MQAction_topic, manager)
        mqtt_listener.start()

    def register(self, sensor_kind, sensor_id, sensor_name):
        manager.add_read_sensor(sensor_kind, sensor_id, sensor_name)

    def register_action(self, sensor_kind, sensor_id, sensor_name, action_function):
        manager.add_action_sensor(sensor_kind, sensor_id, sensor_name, action_function)

    def set_value(self, sensor_id, new_value):
        manager.update_sensor(sensor_id, new_value)

    def set_custom_sensor(self, sensor_id, properties):
        manager.update_custom_sensor(sensor_id, properties)