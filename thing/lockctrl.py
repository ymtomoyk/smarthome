import time
import threading
from led import LedController
from servo import ServoController
from lockcheck import LockStatusChecker
from switch import SwitchHandler
from beacon import BeaconController

MAX_THREAD_NUM = 8
AUTOLOCK_DELAY = 60 #sec
DC_LOCK = 9.4
DC_UNLOCK = 5.2

class LockController:
  def __init__ (self):
    self.ledCtrl    = LedController ()
    self.servoCtrl  = ServoController ()
    self.statCheck  = LockStatusChecker ()
    self.switchHndl = SwitchHandler (self)
    self.beaconCtrl = BeaconController ()
    self.lastUnlock = 0

  def __checkAndExecute (self, dc, targetState, blinker):
    result = {}
    result['wasLocked'] = self.statCheck.isLocked ()
    if result['wasLocked'] != targetState:
      blinker (True)
      self.servoCtrl.execute (dc);
      blinker (False)
      result['isLocked'] = self.statCheck.isLocked ()
    else:
      result['isLocked'] = result['wasLocked']
    return result

  def lock (self):
    return self.__checkAndExecute (DC_LOCK, True, self.ledCtrl.green)

  def __autoLock (self, delay):
    time.sleep (delay)
    elapsed = time.time () - self.lastUnlock
    if elapsed >= AUTOLOCK_DELAY:
      print str (elapsed) + ' seconds elapsed, perform lock'
      self.lock ()
    else:
      print 'unlock happened just ' + str (elapsed) + ' seconds ago, do not lock for now'

  def __createAutoLockTask (self):
    if threading.active_count () < MAX_THREAD_NUM:
      try:
        th = threading.Thread (target=self.__autoLock, name='delay', args=(AUTOLOCK_DELAY,))
        th.start ()
      finally:
        print 'current number of thread: ' + str (threading.active_count ())

  def unlock (self):
    targetState = False
    result = self.__checkAndExecute (DC_UNLOCK, False, self.ledCtrl.yellow)
    if result['wasLocked'] == True and result['isLocked'] == False:
      self.lastUnlock = time.time ()
      self.__createAutoLockTask ()
    return result

  def isLocked (self):
    return {'isLocked': self.statCheck.isLocked ()}

  def __del__ (self):
    del self.ledCtrl
    del self.servoCtrl
    del self.statCheck
    del self.switchHndl
    del self.beaconCtrl

  def delete (self):
    # to ensure stopping beacon
    self.beaconCtrl.stop ()
    self.__del__()
    del self
