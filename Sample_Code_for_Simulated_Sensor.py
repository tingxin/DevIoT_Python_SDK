__author__ = 'tingxxu'
import time
import random
from DevIoTGateway.gateway import Gateway
from DevIoTGateway.sensor import Sensor,SSetting,SProperty,SAction
from DevIoTGateway.config import config

# action name will be 'on' or 'off'
def trigger_alert_shanghai(sensor_id, action):
    print("shanghai " + action.name)


# action name will be 'on' or 'off'
def pollution_callback(sensor_id, action):
    print("action %s occur at %s " % (action.name, sensor_id))

if __name__ == '__main__':
    app_name = config.get_string("appname", "test")
    print(app_name)
    # create a gateway service instance
    # the parameters are: app name, deviot address, mq server address, deviot account
    app = Gateway("tingxin_test", "www.ciscodeviot.com", "mqtt.ciscodeviot.com:1883", "")

    # register input sensors
    # the parameters are: sensor kind, sensor id, sensor display name
    app.register("PM25", "PM25Shanghai", "PM25Shanghai")
    app.register("Noise", "NoiseShanghai", "NoiseShanghai")

    # register output sensors
    # the parameters are: sensor kind, sensor id, sensor display name, action call back function
    app.register_action("Alert", "AlertToShanghai", "AlertToShanghai", trigger_alert_shanghai)

    # register some output sensors
    # don't set the  action call back function for those sensors
    app.register_action("Pollution", "PollutionSuzhou", "PollutionSuzhou")
    app.register_action("Pollution", "PollutionBeijing", "PollutionBeijing")

    # set callback for all sensors which kind is 'Pollution'
    app.register_callback_for_kind("Pollution", pollution_callback)

    # register a complex sensor
    weather = Sensor("weather", "weatherinsh", "WeatherInShangHai")

    temperature = SProperty("temperature", 0, [-10, 50], 20)
    temperature.unit = "Celsius"

    humid = SProperty("humid", 0, [0, 100], 35)
    humid.unit = "D"

    start = SAction("start")
    end = SAction("end")
    suspend = SAction("suspend")

    weather.add_property(temperature)
    weather.add_property(humid)

    weather.add_action(start)
    weather.add_action(end)
    weather.add_action(suspend)

    app.register_custom_sensor(weather)

    # run service
    app.run()

    while True:
        # use random value to update the sensor
        # the parameters are: sensor id, new sensor value
        app.set_value("PM25Shanghai", random.randint(50, 200))
        app.set_value("NoiseShanghai", random.randint(50, 200))

        time.sleep(0.5)