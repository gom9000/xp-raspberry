# serial-midi.py
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
# Version....: 1.0 2022/03/31
# Description: module for read MIDI messages from serial port at 31250Hz
# URL........: https://github.com/gom9000/xp-raspberry
# License....: MIT License


import serial

s = serial.Serial('/dev/ttyAMA0', baudrate=38400)    

message = [0, 0, 0]
print ('midi-in serial test')
while True:
  i = 0
  while i < 3:
    data = ord(s.read(1))
    if data >> 7 != 0:  # status byte
      i = 0
    message[i] = data
    i += 1
    if i == 2 and message[0] >> 4 == 12:  # program change (only 2 bytes)
      message[2] = 0
      i = 3

  messagetype = message[0] >> 4
  messagechannel = (message[0] & 15) + 1
  note = message[1] if len(message) > 1 else None
  velocity = message[2] if len(message) > 2 else None

  if messagetype == 9:    # Note on
    print ('Note on')
  elif messagetype == 8:  # Note off
    print ('Note off')            
  elif messagetype == 12: # Program change
    print ('Program change')
