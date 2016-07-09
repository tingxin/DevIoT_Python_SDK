#DevIoT Gateway Python SDK
This is [DevIoT](https://developer.cisco.com/site/devnetlabs/deviot/) gateway service SDK and sample codes. You can use this SDK to register sensors to DevIoT, and sync up data and actions between the sensors and DevIoT. 

## Table of contents

* [What in this code](#what-in-this-code)
* [Prerequisite](#prerequisite)
* [Usage](#Usage)
* [SDK API](#sdk-api)
* [Getting help](#getting-help)

## What in this code
1. DevIotGateway folder: The SDK python source code

2. Sample_Code_for_GrovePi_Sensor.py : A simple sample to show how to use this SDK, which sync up grove light sensor data to DevIot, it also let DevIo trigger grove Led sensor

3. Sample_Code_for_Simulated_Sensor.py: A simple sample to show how to use this SDK, which sync up some virtual sensor data to DevIot, it also let DevIot can trigger some virtual action sensor

##Prerequisite
1.[Python2.7](https://www.python.org/downloads/):This SDK base on the Python 2.7.10

2.[paho-mqtt](https://eclipse.org/paho/clients/python/): this SDK use this to build a simple MQTT client

##Usage:
1. You can use sample code to register GrovePi sensors and simulated sensors to DevIoT.

2. You can also use SDK to register other sensors and systems to DevIoT.


##SDK API
###Gateway
This class allow your instance a Gateway app, hepe you register sensors to DevIot, sync up data and action to DevIot.
####Constructor
* app name: the gateway name, DevIot use it differentiates gateways 
* deviot address: the address of DevIot, should include the port
* mq server: gateway use mqtt protocol to communicate with DevIot, you can ask the your DevIot administrator to get it, it also should include the port
* DevIot account: you DevIot account, you also can use empty string, it will let all account get the data of your gateway

        # the parameters are: app name, deviot address, mq server address, deviot account
        app = Gateway("grovepi_test", "10.140.92.25:9000", "10.140.92.25:1883", "tingxxu@cisco.com")

####Register Data Sensors
* sensor kind: the kind of sensor, it describes your sensor's function
* sensor id: the unique id of sensor
* sensor name: the display name in DevIot of the sensor

        # the parameters are: sensor kind, sensor id, sensor display name, action call back function
        app.register_action("led", "groveled", "GroveLed", trigger_grove_led)
        
####Register Action Sensors
* sensor kind: the kind of sensor, it describes your sensor's function
* sensor id: the unique id of sensor
* sensor name: the display name in DevIot of the sensor
* action callback function: when DevIot trigger this action sensor, this function will be call

        # the parameters are: sensor kind, sensor id, sensor display name
        app.register("light", "grovelight", "GroveLight")
        
        # turn on/off the led when receive action from DevIot
        # action name will be 'on' or 'off'
        def trigger_grove_led(action):
            print('led get action:' + action.name)
            if action.name == 'on':
                grovepi.digitalWrite(led, 1)
            else:
                grovepi.digitalWrite(led, 0)
                
####Start the Gateway

        # run service
        app.run()
        
The run method will let gateway start a background thread to register sensors and sync up data and action
     
####Update the Sensor Data
* sensor id: the unique id of sensor
* sensor value: the new value of data sensor

        app.set_value("grovelight", 50.0f)
        
##How to run Sample_Code_for_GrovePi_Sensor.py
###Build the hardware###

1.Prepare your RaspberryPi os environment in your SD card

* Download the OS for RaspberryPi form here[RASPBIAN JESSIE](https://www.raspberrypi.org/downloads/raspbian/)

* Format you SD card

* Use window install the OS image to the SD card. you can use [Win32 Disk Manager](https://sourceforge.net/projects/win32diskimager/) do this 
    I strongly recommend you do this use windows, i have met many issues when i installed it by mac os

* Attach the SD card to the RaspberryPi

You also can do this follow [here](https://www.raspberrypi.org/documentation/installation/noobs.md)

2.Join the GrovePi with RaspberryPi. if you correct, it should be like this


3.Connect RaspberryPi with the power and network.

4.Connect RaspberryPi with Display use the HDMI cables.

###Build the software environment###
5.Install the Python 2.7. Check the python version of RaspberryPi os. this sample code base on python2.7.3 or later. in most time, the RaspberryPi os have installed the python2.7.3 or later, if not, you can 
install the python follow [here](https://www.raspberrypi.org/documentation/linux/software/python.md)

6.Install GrovePi SDK.

* Make sure your Raspberry Pi is connected to the internet. 
 
* Type follow command in terminal window
    
        sudo apt-get update
        sudo apt-get install rpi.gpio
    
* [Follow this tutorial for setting up the GrovePi](http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/).

* Restart the Raspberry Pi.
    
Your SD card now has what it needs to start using the GrovePi!
[Here is info more about install GrovePi SDK](http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/)

###Run Grove Pi sample
* Cd to your work space in terminal window
* Type follow command:
    
        python Sample_Code_for_GrovePi_Sensor.py
        
## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker

## Getting involved

For general instructions on _how_ to contribute, please visit [CONTRIBUTING](CONTRIBUTING.md)

## Open source licensing info

1. [LICENSE](LICENSE)

## Credits and references

None
        
 