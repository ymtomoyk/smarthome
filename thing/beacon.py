import os

ADVDATA_FILE = 'advdata.txt'

class BeaconController:
  def start (self, advData):
    os.system ('hcitool -i hci0 cmd 0x08 0x0008 ' + advData)
    os.system ('hciconfig hci0 leadv 3')

  def stop (self):
    os.system ('hciconfig hci0 noleadv')

  def __init__ (self):
    f = open (ADVDATA_FILE, 'r')
    self.start (f.read ())
    f.close ()

  def __del__ (self):
    self.stop ()
