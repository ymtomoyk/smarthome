import RPi.GPIO as GPIO
import time
import os
LOCKFILE = '.lock'
GP_SERVO = 4

class ServoController:
  def __exclude (self):
    ret = False
    if (os.path.exists (LOCKFILE) == False):
      f = open (LOCKFILE, 'w')
      f.close ()
      ret = True
    return ret

  def __release (self):
    if (os.path.exists (LOCKFILE) == True):
      os.remove (LOCKFILE)

  def execute (self, dc):
    if (self.__exclude ()):
      servo = GPIO.PWM (GP_SERVO, 50)
      servo.start (0.0)
      servo.ChangeDutyCycle (dc)
      time.sleep (0.5)
      servo.stop ()
      self.__release ()

  def __init__ (self):
    GPIO.setup (GP_SERVO, GPIO.OUT)
    self.__release ()

  def __del__ (self):
    self.__release ()
