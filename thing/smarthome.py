import time
import argparse
import json
import RPi.GPIO as GPIO
from awsiot import MyAWSIoTClient
from lockctrl import LockController

GPIO.setmode (GPIO.BCM)
parser = argparse.ArgumentParser ()
parser.add_argument ('-e', '--endpoint', action='store', required=True, dest='host', help='Your AWS IoT custom endpoint')
parser.add_argument ('-r', '--rootCA', action='store', required=True, dest='rootCAPath', help='Root CA file path')
parser.add_argument ('-c', '--cert', action='store', required=True, dest='certificatePath', help='Certificate file path')
parser.add_argument ('-k', '--key', action='store', required=True, dest='privateKeyPath', help='Private key file path')
parser.add_argument ('-id', '--clientId', action='store', required=True, dest='clientId', default='basicPubSub',
                      help='Targeted client id')
parser.add_argument ('-tq', '--topic_req', action='store', required=True, dest='topicReq', default='sdk/test/Python', help='topic for request')
parser.add_argument ('-ts', '--topic_res', action='store', required=True, dest='topicRes', default='sdk/test/Python', help='topic for response')
args = parser.parse_args()

awsiotClient = MyAWSIoTClient (args)
lockCtrl     = LockController ()

def requestHandler (data):
  jsonData = json.loads(data)
  cmd = jsonData['cmd']

  if cmd == 'lock':
    jsonData.update (lockCtrl.lock ())
  elif cmd == 'unlock':
    jsonData.update (lockCtrl.unlock ())
  elif cmd == 'isLocked':
    jsonData.update (lockCtrl.isLocked ())

  if jsonData['type'] == 'line':
    awsiotClient.publish (json.dumps (jsonData))

awsiotClient.subscribe (requestHandler)

try:
  while True:
    time.sleep (3600)
finally:
  print '\n'
  print '------------------------------------------'
  print ' Interruption occurred, perform clean up. '
  print '------------------------------------------'
  awsiotClient.delete ()
  lockCtrl.delete ()
  GPIO.cleanup ()
  time.sleep (5) # give time to finish clean up
