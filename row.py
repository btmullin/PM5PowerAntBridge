#!/usr/bin/python
#
# This script will NOT work alone, it needs a few library installed
# Please refers to the full image to flash a working environment on a Raspberry
#
from constants import *
import hashlib

import time
import datetime
from random import randint

import pyrow
from ant.core import driver
from ant.core import node

from PowerMeterTx import PowerMeterTx
from SpeedTx import SpeedTx

###########################################################################################################

def dummy_workout(power_meter, myLog):

    zwiftRpm = 1
    zwiftWatts = 1

    #power_meter.update(zwiftWatts, zwiftRpm)
    power_meter.update(zwiftWatts)
    speed_sensor.update(0, 0)
    myNow = datetime.datetime.now() 
    myLog.write(str(myNow) + " DUMMY " + str(zwiftRpm) + " --- " + str(zwiftWatts) + "\n")
    myLog.flush()
    return()

###########################################################################################################

def workout(power_meter, myWorkout, myLog):

    forceplot = erg.get_force_plot()

    #Loop while waiting for drive
    while forceplot['strokestate'] != 2 and myWorkout['state'] == 1:
          time.sleep(.1)
          forceplot = erg.get_force_plot()
          myWorkout = erg.get_workout()

    #get monitor data for END of stroke
    monitor = erg.get_monitor()
    mySpm=monitor['spm']
    myWatts=monitor['power']
    zwiftWatts=int(round(myWatts * POWER_ADJUST))
    zwiftRpm=int(round(mySpm * RPM_ADJUST))
    print("W= "+str(myWatts)+" RPM= "+str(mySpm)+"\n")

    power_meter.update(zwiftWatts, zwiftRpm)
    
    zwiftDist=monitor['distance']
    zwiftPace=monitor['pace']
    speed_sensor.update(zwiftDist, zwiftPace)
    print("D= "+str(zwiftDist)+" "+"P= "+str(zwiftPace)+"\n")
    
    myNow = datetime.datetime.now() 
    myLog.write(str(myNow) + " ... " + str(zwiftRpm) + " --- " + str(zwiftWatts) + "\n")
    myLog.flush()
    return()


###########################################################################################################
######################     MAIN                                                        ####################
###########################################################################################################

# ANT+ ID of the virtual power sensor
# The expression below will choose a fixed ID based on the CPU's serial number
POWER_SENSOR_ID = int(int(hashlib.md5(getserial()).hexdigest(), 16) & 0xfffe) + 1
# The expression below will choose a fixed ID based on the CPU's serial number
SPEED_SENSOR_ID = int(int(hashlib.md5(getserial()).hexdigest(), 16) & 0xfffe) + 1
# ANT+ network key
NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

POWER_ADJUST = 1.0
RPM_ADJUST = 1.0
DEBUG = False
PRINT = False
LOG = ''
myNow = datetime.datetime.now().strftime("%Y%m%d%H%M")
myLogName = "/home/pi/C2Power/app/log/" + myNow + ".log"
myLog = open(myLogName,"w")

# initialize ANT dongle

stick = driver.USB2Driver(None, log=LOG, debug=DEBUG)
antnode = node.Node(stick)

antnode.start()
key = node.NetworkKey('N:ANT+', NETKEY)
antnode.setNetworkKey(0, key)

power_meter = PowerMeterTx(antnode, POWER_SENSOR_ID)
power_meter.open()
myLog.write("STARTED power meter with ANT+ ID " + repr(POWER_SENSOR_ID) + "\n")
myLog.flush()


speed_sensor = SpeedTx(antnode, SPEED_SENSOR_ID)
speed_sensor.open()
myLog.write("STARTED speed sensor with ANT+ ID " + repr(SPEED_SENSOR_ID) + "\n")
myLog.flush()

while True:
      try:
          # loop for C2 usb
          ergs = list(pyrow.find())
          while len(ergs) == 0:
                dummy_workout(power_meter, myLog)
                time.sleep(5)
                ergs = list(pyrow.find())

          while True:
             # Waiting for workout start
             myLog.write("Waiting for workout start\n")
             myLog.flush()
             erg = pyrow.pyrow(ergs[0])
             myWorkout = erg.get_workout()
             while myWorkout['state'] == 0:
                dummy_workout(power_meter, myLog)
                time.sleep(1)
                myWorkout = erg.get_workout()

             #     ROW on !!
             while myWorkout['state'] == 1:
                workout(power_meter, myWorkout, myLog)
                myWorkout = erg.get_workout()

      except:
         myLog.write("Starting new ???\n")
         myLog.flush()

