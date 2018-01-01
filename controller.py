import globals
import time
import sys
import time

class PID(object): #borrowed from code.activestate.com/recipes/577231-discrete-pid-controller/
  """
  Discrete PID control
  """

  def __init__(self, P=10.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=0):

    self.Kp=P
    self.Ki=I
    self.Kd=D
    self.Derivator=Derivator
    self.Integrator=Integrator
    self.Integrator_max=Integrator_max
    self.Integrator_min=Integrator_min

    self.set_point=0.0
    self.error=0.0

  def update(self,current_value):
    """
    Calculate PID output value for given reference input and feedback
    """

    self.error = self.set_point - current_value

    self.P_value = self.Kp * self.error
    self.D_value = self.Kd * ( self.error - self.Derivator)
    self.Derivator = self.error

    self.Integrator = self.Integrator + self.error

    if self.Integrator > self.Integrator_max:
      self.Integrator = self.Integrator_max
    elif self.Integrator < self.Integrator_min:
      self.Integrator = self.Integrator_min

    self.I_value = self.Integrator * self.Ki

    PID = self.P_value + self.I_value + self.D_value

    return PID

  def setPoint(self,set_point):
    """
    Initilize the setpoint of PID
    """
    self.set_point = set_point
    self.Integrator=0
    self.Derivator=0

  def alterSetpoint(self, set_point):
    self.set_point = set_point

  def setIntegrator(self, Integrator):
    self.Integrator = Integrator

  def setDerivator(self, Derivator):
    self.Derivator = Derivator

  def setKp(self, P):
    self.Kp=P

  def setKi(self, I):
    self.Ki=I
  
  def setKd(self, D):
    self.Kd=D

  def getPoint(self):
    return self.set_point

  def getError(self):
    return self.error

  def getIntegrator(self):
    return self.Integrator

  def getDerivator(self):
    return self.Derivator

pid = PID()
latestSetpoint = 0.0
actual = 0
try:
  while True:
    command, value = globals.readfifo(globals.FIFO_SETPOINT).split(":")
    if command == globals.COMMAND_NEWSETPOINT:
      latestSetpoint = float(value)
    pid.alterSetpoint(latestSetpoint)
    command, value = globals.readfifo(globals.FIFO_ACTUAL).split(":")
    if command == globals.COMMAND_NEWACTUAL:
      actual = float(value)
    ctrl = pid.update(actual)
    if ctrl < 0.0:
      ctrl = 0.0
    globals.writefifo(globals.FIFO_CTRL, globals.COMMAND_NEWCONTROLVALUE, str(ctrl))
    time.sleep(1)
except KeyboardInterrupt:
  sys.exit(0) 
