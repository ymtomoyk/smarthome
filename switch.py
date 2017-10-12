import RPi.GPIO as GPIO
import time

GP_PW_LOCK   = 5
GP_PW_UNLOCK = 10
GP_SW_LOCK   = 8
GP_SW_UNLOCK = 9
INTERVAL     = 0.5

class SwitchHandler:
  def __switchEventHandler (self, pin):
    now = time.time()
    if (now - self.lastExec) > INTERVAL: #avoid chattering
      self.lastExec = now
      if pin == GP_SW_UNLOCK:
        self.lockCtrl.unlock()
      else:
        self.lockCtrl.lock()

  def __observe (self, pin):
    GPIO.setup (pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect (pin, GPIO.FALLING)
    GPIO.add_event_callback (pin, self.__switchEventHandler)

  def __init__ (self, lockCtrl):
    GPIO.setup  (GP_PW_LOCK,   GPIO.OUT)
    GPIO.setup  (GP_PW_UNLOCK, GPIO.OUT)
    GPIO.output (GP_PW_LOCK,   GPIO.HIGH)
    GPIO.output (GP_PW_UNLOCK, GPIO.HIGH)
    self.lockCtrl = lockCtrl
    self.lastExec = 0
    self.__observe (GP_SW_LOCK)
    self.__observe (GP_SW_UNLOCK)

  def __del__ (self):
    GPIO.output (GP_PW_LOCK,   GPIO.LOW)
    GPIO.output (GP_PW_UNLOCK, GPIO.LOW)
    self.lockCtrl = None
