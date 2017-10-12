import RPi.GPIO as GPIO
import time

GP_LIGHT_G = 15
GP_LIGHT_Y = 14

class LedController:
  def __gp_set (self, pin, enable):
    if enable:
      GPIO.output (pin, GPIO.HIGH)
    else:
      GPIO.output (pin, GPIO.LOW)

  def green (self, enable):
    self.__gp_set (GP_LIGHT_G, enable)

  def yellow (self, enable):
    self.__gp_set (GP_LIGHT_Y, enable)

  def __init__ (self):
    GPIO.setup (GP_LIGHT_G, GPIO.OUT)
    GPIO.setup (GP_LIGHT_Y, GPIO.OUT)
    self.green (False)
    self.yellow (False)

  def __del__ (self):
    self.green (False)
    self.yellow (False)
