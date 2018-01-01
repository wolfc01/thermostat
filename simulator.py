import globals
import time

temp = 0.0
leak = 0.001
mass = 100.0
energy = 0.0

while True:
  command, value = globals.readfifo(globals.FIFO_CTRL).split(":")
  if command == globals.COMMAND_NEWCONTROLVALUE:
    energy = float(value)
  temp = temp + energy * (1.0 / mass) - leak
  if temp < 0.0:
    temp = 0.0
  globals.writefifo(globals.FIFO_ACTUAL, globals.COMMAND_NEWACTUAL, str(temp))
  globals.writefifo(globals.FIFO_ACTUALWEBSERVER, globals.COMMAND_NEWACTUAL, str(temp))
  time.sleep(1)
