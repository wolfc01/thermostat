import subprocess
import time
import sys

processes = {}

def startWebserver():
  return subprocess.Popen(["python","webserver.py"], shell=False)
def startController():
  return subprocess.Popen(["python", "controller.py"], shell=False)
def startSimulator():
  return subprocess.Popen(["python", "simulator.py"], shell=False)

processes[startWebserver] = False
processes[startController] = False
processes[startSimulator] = False

try:
  while True:
    time.sleep(0.1)
    for process in processes:
      if processes[process] == False:
        processes[process] = process()
      if processes[process].poll() is not None: #this process is terminated
        processes[process] = False
except KeyboardInterrupt:
  for process in processes:
    try: 
      processes[process].terminate()
      processes[process].wait()
    except:
      pass
  sys.exit(0)
