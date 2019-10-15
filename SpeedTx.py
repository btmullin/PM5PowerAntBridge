import sys
from ant.core import message
from ant.core.constants import *
from ant.core.exceptions import ChannelError
import datetime

from constants import *

CHANNEL_PERIOD = 8182


# Transmitter for Bicycle Speed ANT+ sensor
class SpeedTx(object):
    class SpeedData:
        def __init__(self):
            self.eventCount = 0
            self.eventTime = 0
            self.cumulativeDistance = 0
            self.instPace = 0;
            self.startTime = datetime.datetime.now()

    def __init__(self, antnode, sensor_id):
        self.antnode = antnode

        # Get the channel
        self.channel = antnode.getFreeChannel()
        try:
            self.channel.name = 'C:SPEED'
            self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_TRANSMIT)
            self.channel.setID(SPEED_DEVICE_TYPE, sensor_id, 0)
            self.channel.setPeriod(8182)
            self.channel.setFrequency(57)
        except ChannelError as e:
            print "Channel config error: "+e.message
        self.speedData = SpeedTx.SpeedData()

    def open(self):
        self.channel.open()

    def close(self):
        self.channel.close()

    def unassign(self):
        self.channel.unassign()

    # A stroke was completed update the speed
    # TODO - Update shit here
    def update(self, distance, pace):
        self.speedData.eventCount = (self.speedData.eventCount + 1) & 0xff
        self.speedData.cumulativeDistance = int(distance) & 0xffff
        self.speedData.instPace = int(pace)
        
        # calculate the total time since we instantiated, then convert to 1/1024ths of a second
        # then truncate to 2 bytes
        n = datetime.datetime.now()
        timeDelta = n - self.speedData.startTime
        fSec = int(timeDelta.total_seconds() * 1024) & 0xffff

        payload = chr(0x00)  # data page 0x00
        payload += chr(0xFF) # reserved
        payload += chr(0xFF) # reserved
        payload += chr(0xFF) # reserved
        # event time 1/1024 second, LSB then MSB
        payload += chr(fSec & 0xff)
        payload += chr(fSec >> 8)
        
        # cumulative revolution count, LSB then MSB
        payload += chr(self.speedData.cumulativeDistance & 0xff)
        payload += chr(self.speedData.cumulativeDistance >> 8)
        
        print payload.encode("hex")
        
        ant_msg = message.ChannelBroadcastDataMessage(self.channel.number, data=payload)
        self.antnode.driver.write(ant_msg.encode())