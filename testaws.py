#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import datetime
from time import sleep

camera = PiCamera()
#camera.rotation=180
camera.hflip = True
camera.vflip = True

import boto3
import json

#
# See http://www.wrightfully.com/garagepi-my-raspberry-pi-playground
#

GPIO.setmode(GPIO.BCM)


SPEED_OF_SOUND = 34000 #cm/s
NOTIFY = 70 #cm  - is actually about 60 but get readings up to 68 sometimes
SAMPLE_SPEED = 5 #seconds

# GPIO pin numbers
TRIG = 23
ECHO = 24
LED_OPEN = 12
LED_RUN = 25

class SonicController:
  def readDistance(self):

    print "Distance Measurement In Progress " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    roundtrip_duration = pulse_duration * SPEED_OF_SOUND
    one_way_distance = roundtrip_duration/2
    print "    Distance: %.2f cm" %one_way_distance
    return one_way_distance

  def init(self):

    print "Initializing Ultrasonic Range Finder"

    #GPIO.setup(TRIG, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(TRIG, GPIO.OUT)
    #GPIO.setup(ECHO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    time.sleep(2)

  def teardown(self):
    print "Tearing down Ultrasonic Range Finder"
    GPIO.output(TRIG, False)

class LedController:
  def init(self):
    print "initializing led"
    GPIO.setup(LED_OPEN, GPIO.OUT)
    GPIO.setup(LED_RUN, GPIO.OUT)
    GPIO.output(LED_RUN, True)

  def turnOnDoorLed(self):
    print " turning led on"
    GPIO.output(LED_OPEN, True)

  def turnOffDoorLed(self):
    print "turning led off"
    GPIO.output(LED_OPEN, False)

  def teardown(self):
    print "tearing down led"
    self.turnOffDoorLed()
    GPIO.output(LED_RUN, False)

led = LedController()
led.init()

sensor = SonicController()
sensor.init()



try:
  print "loop start"
  while True:
    sleep(10)
    print "scanning"
    distance = sensor.readDistance()
    if distance < NOTIFY:
      print "    Take picture"

      #find current date and time
      str1 = datetime.datetime.now()
      str1 = str1.strftime('%m_%d_%Y_%H_%M_%S')
      str2 = "/home/pi/Desktop/pics/"
      str3 = ".jpg"
      str4 = str1 + str3
      str1 = str2 + str1
      str1 = str1 + str3

      #using set jpg name for now
      #filename = str1 + str3
      #filename = "newPhoto.jpg"

      #take picture
      camera.start_preview()
      sleep(5)
      camera.capture(str1)
      camera.stop_preview()

      ############################AWS########################################


      s3 = boto3.resource('s3')



      #s3 = boto3.client('s3',aws_access_key_id='ACCESS_KEY',aws_secret_access_key='SECRET_KEY')
      #response=s3.get_object(Bucket='BUCKET',Key='KEY')

      #Bucket Name
      bucketName = 'scuiot'

      #Upload Photo
      photo = open(str1, 'rb')
      s3.Bucket(bucketName).put_object(Key=str4,Body=photo )

      #simple recognition
      #'''

      #fileName='newPhoto.jpg'
      client=boto3.client('rekognition','us-west-2')

      response = client.detect_faces(Image={'S3Object':{'Bucket':bucketName,'Name':str4}},Attributes=['ALL'])

      print('Detected faces for ' + str1)
      for faceDetail in response['FaceDetails']:
          print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
          print('Here are the other attributes:')
          print(json.dumps(faceDetail, indent=4, sort_keys=True))
      #'''

      ########################################################################

      #led.turnOnDoorLed()
    else:
      print "    Nothing too close"
      #led.turnOffDoorLed()

    time.sleep(SAMPLE_SPEED)
except KeyboardInterrupt:
    print "keyboard interrupt caught"
finally:
  sensor.teardown()
  led.teardown()
  # Finally, we clean our GPIO pins to ensure that all inputs/outputs are reset
  GPIO.cleanup()
  print "exiting"
