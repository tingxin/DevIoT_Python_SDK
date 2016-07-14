

import time
from grovepi import grovepi
from DevIoTGateway.gateway import Gateway

# connect the Grove Light Sensor to analog port A2
# SIG,NC,VCC,GND
light_sensor = 2

# connect the LED to digital port D3
# SIG,NC,VCC,GND
led = 3

grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(led, "OUTPUT")


# turn on/off the led when receive action from DevIot
# action name will be 'on' or 'off'
def trigger_grove_led(sensor_id, action):
    print('led get action:' + action.name)
    if action.name == 'on':
        grovepi.digitalWrite(led, 1)
    else:
        grovepi.digitalWrite(led, 0)


# create a gateway service instance
# the parameters are: app name, deviot address, mq server address, deviot account
app = Gateway("grovepi_test", "10.140.92.25:9000", "10.140.92.25:1883", "tingxxu@cisco.com")

# register input sensors
# the parameters are: sensor kind, sensor id, sensor display name
app.register("light", "grovelight", "GroveLight")

# register output sensors
# the parameters are: sensor kind, sensor id, sensor display name, action call back function
app.register_action("led", "groveled", "GroveLed", trigger_grove_led)

# run service
app.run()
    
while True:
    try:
        # get sensor value
        sensor_value = grovepi.analogRead(light_sensor)

        # update the sensor value, the parameters are: sensor id, new sensor value
        app.set_value("grovelight", sensor_value)
        time.sleep(.5)

    except IOError:
        print ("Error")
