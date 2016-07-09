__author__ = 'tingxxu'

import threading
import json
import time
import sys

import httplib


class Register(threading.Thread):

    def __init__(self, name, manager, iot_address, server_ip, server_port, owner, is_mqtt=True, is_virtual=True):
        threading.Thread.__init__(self)
        self.__api_address__ = iot_address
        self.__ip__ = server_ip
        self.__port__ = server_port
        self.__manager__ = manager
        self.__app_name__ = name
        self.__is_virtual__ = is_virtual
        self.is_mqtt = is_mqtt
        self.__owner = owner

        self.MQData_topic = ("%s-%s-data" % (self.__app_name__, self.__owner)).encode('utf8')
        self.MQAction_topic = ("%s-%s-action" % (self.__app_name__, self.__owner)).encode('utf8')

        self._register_model = {}
        self._register_model['name'] = self.__app_name__
        self._register_model['mode'] = 2
        self._register_model['virtual'] = self.__is_virtual__
        self._register_model['host'] = self.__ip__
        self._register_model['port'] = self.__port__
        self._register_model['owner'] = self.__owner

        self._register_model['data'] = self.MQData_topic
        self._register_model['action'] = self.MQAction_topic
        self._register_model['setting'] = '/api/modify'

    def run(self):
        api = "/api/v1/gateways"


        self._register_model['sensors'] = self.__manager__.get_all_expression()

        json_data = json.dumps(self._register_model)

        while True:
            try:
                conn = httplib.HTTPConnection(self.__api_address__)
                conn.request("POST", api, json_data, {'Content-Type': 'application/json'})
                response = conn.getresponse()
            except IOError as e:
                print(e)
            except:
                print("--RunRegisterThread error:", sys.exc_info()[1])
            time.sleep(60)

    @staticmethod
    def adapter(sensor_model):
        return sensor_model
