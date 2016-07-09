__author__ = 'tingxxu'
import time
import random
from DevIoTGateway.gateway import Gateway


# action name will be 'on' or 'off'
def trigger_pollution_shanghai(action):
    print("shanghai " + action.name)


# action name will be 'on' or 'off'
def trigger_pollution_suzhou(action):
    print("suzhou " + action.name)


# action name will be 'on' or 'off'
def trigger_pollution_beijing(action):
    print("beijing " + action.name)

if __name__ == '__main__':
    # create a gateway service instance
    # the parameters are: app name, deviot address, mq server address, deviot account
    app = Gateway("tingxin_test", "10.140.92.25:9000", "10.140.92.25:1883", "tingxxu@cisco.com")

    # register input sensors
    # the parameters are: sensor kind, sensor id, sensor display name
    app.register("PM25", "PM25Shanghai", "PM25Shanghai")
    app.register("Noise", "NoiseShanghai", "NoiseShanghai")

    # register output sensors
    # the parameters are: sensor kind, sensor id, sensor display name, action call back function
    app.register_action("Alert", "PollutionShanghai", "PollutionInShanghai", trigger_pollution_shanghai)
    app.register_action("Alert", "PollutionSuzhou", "PollutionSuzhou", trigger_pollution_suzhou)
    app.register_action("Alert", "PollutionBeijing", "PollutionBeijing", trigger_pollution_beijing)

    # run service
    app.run()

    while True:
        # use random value to update the sensor
        # the parameters are: sensor id, new sensor value
        app.set_value("PM25Shanghai", random.randint(50, 200))
        app.set_value("NoiseShanghai", random.randint(50, 200))

        time.sleep(0.5)