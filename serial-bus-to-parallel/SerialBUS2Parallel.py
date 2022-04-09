 # SerialBUS2Parallel.py
#            ___              _
#  __ ___ __| _ \__ _ ____ __| |__  ___ _ _ _ _ _  _
#  \ \ / '_ \   / _` (_-< '_ \ '_ \/ -_) '_| '_| || |
#  /_\_\ .__/_|_\__,_/__/ .__/_.__/\___|_| |_|  \_, |
#      |_|              |_|                     |__/
#
# This file is part of the RaspberryPi eXPerience:
#     https://github.com/gom9000/xp-repository
#
# Author.....: Alessandro Fraschetti (mail: gos95@gommagomma.net)
# Target.....: RaspberryPI
# Version....: 1.0 2022/04/02
# Description: module for input/output serial data from/to parallel bus throught shift registers
# URL........: https://github.com/gom9000/xp-raspberry
# License....: MIT License


from RPi import GPIO
from time import sleep
import math


class SerialBUS2Parallel:
    DELAY = 0.001

    # ------------------------------------------------------------------------
    # Init the module and set GPIO pins
    # ------------------------------------------------------------------------
    def __init__(self, data_pin, clock_pin, latch_pin, rw_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.latch_pin = latch_pin
        self.rw_pin = rw_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clock_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.latch_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.rw_pin, GPIO.OUT, initial=GPIO.LOW)


    # ------------------------------------------------------------------------
    # Send pulse
    # ------------------------------------------------------------------------
    def __pulse(self, pin, value=GPIO.HIGH):
        GPIO.output(pin, value)
        sleep(self.DELAY)
        GPIO.output(pin, not value)


    # ------------------------------------------------------------------------
    # Write data on BUS
    # ------------------------------------------------------------------------
    def write(self, data):
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.output(self.rw_pin, GPIO.HIGH)
        for ii in range(8):
            databit = bool(data&int(math.pow(2, ii)))
            GPIO.output(self.data_pin, databit)
            self.__pulse(self.clock_pin)
        self.__pulse(self.latch_pin)


    # ------------------------------------------------------------------------
    # Read data from BUS
    # ------------------------------------------------------------------------
    def read(self):
        data = 0
        GPIO.setup(self.data_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(self.rw_pin, GPIO.LOW)
        self.__pulse(self.latch_pin)
        for ii in range(8):
            databit = GPIO.input(self.data_pin)
            #print ("PISO Input: i%d %d"% (ii, databit))
            data += databit*int(math.pow(2, ii))
            self.__pulse(self.clock_pin)

        return data





# ----------------------------------------------------------------------------
# Test
# ----------------------------------------------------------------------------
try:
    module = SerialBUS2Parallel(13, 6, 19, 26)

    # read from bus
    #while (True):
    #    data = module.read()
    #    print ("read: %d"% data)
    #    sleep(0.5)

    # write on bus
    #for ii in range(0, 256, 1):
    #    print ("write: %d"% ii)
    #    module.write(ii)
    #    sleep(0.02)

    # read & write on bus
    while (True):
        data = module.read()
        print ("read: %d"% data)
        module.write(~data)
        sleep(0.05)
except KeyboardInterrupt:
    GPIO.cleanup()