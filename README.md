# apiToSmartDevice
## Intro
This project uses information from a webb api to control a smart device on a daily schedule.
This project is currently aimed at only one model of smartplug(tapo p110) from TP-link and is only tested with firmware 1.3.0
The code can be altered to function with a broader group of smart devices and from different api sources for different functionality.
For now it is focused on saving money by turning off devices when cost is to high.

## Electricity Price to P110(tapo smartplug) (EPtP110)
In EPtP110, the code reads electrical price for the day. 
This is used together with a limit value to decide when the device should be turned on/off.
A problem with this program is that the updated firmware off the smart-device might hinder functionality off the PyP100 package used for connection over wifi to the device. This means that turning off automatic updating for this device before using it in a setup like this is smart.

## Initial setup
Initialize the smart device on your network before using the program. This can be done f.e. in the tapo phone application. PyP100 library is not capable of initial setup of the smart device.

## Packages used:
time, schedule, requests, keyboard, https://github.com/almottier/TapoP100/blob/main/PyP100/PyP100.py.
All of these can be installed with pip(package installer for python)
Note that the PyP100 is not the official one, but a later build, this can be used in pip:
> pip install git+https://github.com/almottier/TapoP100.git@main
