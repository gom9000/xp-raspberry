# QuadratureEncoder.py
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
# Version....: 1.0 2022/03/08
# Description: module for reading and counting quadrature encoded signals
#              from 3-pin incremental rotary encoder
# URL........: https://github.com/gom9000/xp-raspberry
# License....: MIT License


from RPi import GPIO
from time import sleep


class QuadratureEncoder:

    # ------------------------------------------------------------------------
    # Init the module and set GPIO pins
    # ------------------------------------------------------------------------
    def __init__(self, A_pin, B_pin):
        self.A_pin = A_pin
        self.B_pin = B_pin
        self.ALastState = GPIO.LOW
        self.BLastState = GPIO.LOW
        self.AState = GPIO.LOW
        self.BState = GPIO.LOW
        self.positionCounter = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.A_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.B_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    # ------------------------------------------------------------------------
    # Set the current incremental position counter
    # ------------------------------------------------------------------------
    def setPositionCounter(self, positionCounter):
        self.positionCounter = positionCounter


    # ------------------------------------------------------------------------
    # Return the current incremental position counter
    # ------------------------------------------------------------------------
    def getPositionCounter(self):
        self.__read()
        self.__decode2x()

        return self.positionCounter


    # ------------------------------------------------------------------------
    # Read encoder signals state
    # ------------------------------------------------------------------------
    def __read(self):
        self.AState = GPIO.input(self.A_pin)
        self.BState = GPIO.input(self.B_pin)


    # ------------------------------------------------------------------------
    # Decode and count the encoder signals state (double evaluation)
    # ------------------------------------------------------------------------
    def __decode2x(self):
        if self.AState != self.ALastState:
            if self.BState != self.AState:
                self.positionCounter += 1
            else:
                self.positionCounter -= 1
            self.ALastState = self.AState


    # ------------------------------------------------------------------------
    # Decode and count the encoder signals state (quadruple evaluation)
    # ------------------------------------------------------------------------
    def __decode4x(self):
        if self.AState != self.ALastState:
            if self.BState != self.AState:
                self.positionCounter += 1
            else:
                self.positionCounter -= 1
            self.ALastState = self.AState
        else:
            if self.BState != self.BLastState:
                if self.BState != self.AState:
                    self.positionCounter -= 1
                else:
                    self.positionCounter += 1
                self.BLastState = self.BState


# ----------------------------------------------------------------------------
# Test
# ----------------------------------------------------------------------------
try:
    module = QuadratureEncoder(23,24)
    module.setPositionCounter(0)
    while True:
        print ("Quadrature Encoder value: %d"% (module.getPositionCounter()))
        sleep(0.001)
except KeyboardInterrupt:
    GPIO.cleanup()
