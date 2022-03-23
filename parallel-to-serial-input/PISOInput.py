# PISOInput.py
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
# Description: module for input serial data from parallel-to-serial shift registers
# URL........: https://github.com/gom9000/xp-raspberry
# License....: MIT License


from RPi import GPIO
from time import sleep
import math


class PISOInput:
    DELAY = 0.001

    # ------------------------------------------------------------------------
    # Init the module and set GPIO pins
    # ------------------------------------------------------------------------
    def __init__(self, data_pin, clock_pin, latch_pin):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.latch_pin = latch_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.clock_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.latch_pin, GPIO.OUT, initial=GPIO.HIGH)


    # ------------------------------------------------------------------------
    # Send pulse to registers
    # ------------------------------------------------------------------------
    def __pulse(self, pin, value=GPIO.HIGH):
        GPIO.output(pin, value)
        sleep(self.DELAY)
        GPIO.output(pin, not value)


    # ------------------------------------------------------------------------
    # Read data from registers
    # ------------------------------------------------------------------------
    def read(self):
	    data = 0
	    GPIO.output(self.latch_pin, GPIO.LOW)
        for ii in range(16):
		    databit = GPIO.input(self.data_pin)
            data += databit&int(math.pow(2, ii))
            self.__pulse(self.clock_pin)

		GPIO.output(self.latch_pin, GPIO.HIGH)

		return data




# ----------------------------------------------------------------------------
# Test
# ----------------------------------------------------------------------------
try:
    module = PISOInput(17, 18, 22)
    while True:
        print ("PISO Input: %d"% (module.read()))
        sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
