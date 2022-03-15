# SIPOOutput.py
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
# Version....: 1.0 2022/03/0813
# Description: module for output serial data to serial-to-parallel shift registers
# URL........: https://github.com/gom9000/xp-raspberry
# License....: MIT License


from RPi import GPIO
from time import sleep
import math


class SIPOOutput:
    DELAY = 0.001

    # ------------------------------------------------------------------------
    # Init the module and set GPIO pins
    # ------------------------------------------------------------------------
    def __init__(self, data_pin, clock_pin, latch_pin, reset_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.latch_pin = latch_pin
        self.reset_pin = reset_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.latch_pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.reset_pin, GPIO.OUT, initial=GPIO.HIGH)

        self.__pulse(self.reset_pin, GPIO.LOW)


    # ------------------------------------------------------------------------
    # Send pulse to registers
    # ------------------------------------------------------------------------
    def __pulse(self, pin, value=GPIO.HIGH):
        GPIO.output(pin, value)
        sleep(self.DELAY)
        GPIO.output(pin, not value)


    # ------------------------------------------------------------------------
    # Send data to registers
    # ------------------------------------------------------------------------
    def write(self, data):
        for ii in range(16):
            databit = bool(data&int(math.pow(2, ii)))
            GPIO.output(self.data_pin, databit)
            self.__pulse(self.clock_pin)
        self.__pulse(self.latch_pin, GPIO.LOW)




# ----------------------------------------------------------------------------
# Test
# ----------------------------------------------------------------------------
try:
    module = SIPOOutput(17, 18, 22, 23)
    for ii in range(256):
        module.write(ii + ii*256)
        sleep(0.05)
except KeyboardInterrupt:
    GPIO.cleanup()
