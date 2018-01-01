import os

FIFO_SETPOINT = "SETPOINT"
FIFO_ACTUAL = "ACTUAL"
FIFO_CTRL = "CONTROL"
FIFO_ACTUALWEBSERVER = "ACTUALWEB"

COMMAND_NEWSETPOINT = "newsetpoint"
COMMAND_NEWCONTROLVALUE = "newcontrolvalue"
COMMAND_NEWACTUAL = "newactual"

writefifos = {}
readfifos = {}

def writefifo(name, command, value):
  if not name in writefifos:
    fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    if not os.path.exists(fullPath):
      os.mkfifo(fullPath)
    writefifos[name] = open(fullPath, "wb")
  writefifos[name].write("%s:%s\n" %(command, value))
  writefifos[name].flush() 

def readfifo(name):
  if not name in readfifos:
    fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    if not os.path.exists(fullPath):
      os.mkfifo(fullPath)
    readfifos[name] = os.open(fullPath, os.O_NONBLOCK)
  try:
    data = os.read(readfifos[name], 1)
  except OSError:
    data = ''
  if data:
    while not data.endswith("\n"):
      data += os.read(readfifos[name], 1)
    return data.strip()
  else:
    return ":"
  return data  
  
if __name__ == "__main__":
  import subprocess
  data = readfifo("testfifo")
  assert(data == ":")
  writefifo("testfifo","testcommand","testvalue")
  data = readfifo("testfifo")
  assert(data == "testcommand:testvalue")
  writefifo("testfifo","testcommand1","testvalue1")
  writefifo("testfifo","testcommand2","testvalue2")
  writefifo("testfifo","testcommand3","testvalue3")
  data = readfifo("testfifo")
  assert(data == "testcommand1:testvalue1")
  data = readfifo("testfifo")
  assert(data == "testcommand2:testvalue2")
  data = readfifo("testfifo")
  assert(data == "testcommand3:testvalue3")
  fullPath = fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfifo")
  p = subprocess.Popen("echo testcommand4:testvalue4 >%s" %fullPath, shell=True)
  p.wait()
  while True:
    data = readfifo("testfifo")
    if data == "testcommand4:testvalue4":
      break
  
  