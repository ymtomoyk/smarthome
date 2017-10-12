from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging

MQTT_PORT   = 8883

class MyAWSIoTClient:
  def __init__ (self, args):
    self.args = args
    self.client = AWSIoTMQTTClient (args.clientId)

    # Configure logging
    logger = logging.getLogger ('AWSIoTPythonSDK.core')
    logger.setLevel (logging.DEBUG)
    streamHandler = logging.StreamHandler ()
    formatter = logging.Formatter ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter (formatter)
    logger.addHandler (streamHandler)

    # Init AWSIoTMQTTClient
    self.client.configureEndpoint (self.args.host, MQTT_PORT)
    self.client.configureCredentials (self.args.rootCAPath, self.args.privateKeyPath, self.args.certificatePath)

    # AWSIoTMQTTClient connection configuration
    self.client.configureAutoReconnectBackoffTime (1, 32, 20)
    self.client.configureOfflinePublishQueueing (-1)  # Infinite offline Publish queueing
    self.client.configureDrainingFrequency (2)  # Draining: 2 Hz
    self.client.configureConnectDisconnectTimeout (100)  # 10 sec
    self.client.configureMQTTOperationTimeout (5)  # 5 sec

  def __message_handler (self, client, userdata, message):
    print ('Received a new message: ')
    print (message.payload)
    print ('from topic: ' + message.topic)
    try:
      self.callback (message.payload)
    finally:
      print ("--------------\n\n")

  def subscribe (self, callback):
    self.callback = callback
    self.client.connect ()
    self.client.subscribe (self.args.topicReq, 1, self.__message_handler)

  def publish (self, message):
    print message
    self.client.publishAsync (self.args.topicRes, message, 1)

  def __del__ (self):
    self.client.disconnect ()

  # to call __del__() explicitly
  def delete (self):
    self.__del__ ()
    del self
