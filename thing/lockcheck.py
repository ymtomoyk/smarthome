import Adafruit_MCP3008

GP_CLK  = 18
GP_MISO = 23
GP_MOSI = 24
GP_CS   = 25
SAMPLING_NUM = 4
BASE_VALUE = 512
THRESHOLD = 100

class LockStatusChecker:
  def __init__ (self):
    self.mcp = Adafruit_MCP3008.MCP3008 (clk=GP_CLK, cs=GP_CS, miso=GP_MISO, mosi=GP_MOSI)

  def isLocked (self):
    ret = False
    total = 0
    for i in range (SAMPLING_NUM): 
      total += self.mcp.read_adc (0)
    average = total / SAMPLING_NUM;
    if abs (BASE_VALUE - average) > THRESHOLD:
      ret = True
    return ret

  def __del__ (self):
    del self.mcp
