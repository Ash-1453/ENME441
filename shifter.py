import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dataPin, latchPin, clockPin = 23, 24, 25
class Shifter:
  def __init__(self,dataPin,latchPin,clockPin):
      self.dataPin=dataPin
      self.latchPin=latchPin
      self.clockPin=clockPin
      GPIO.setup(self.dataPin, GPIO.OUT)
      GPIO.setup(self.latchPin, GPIO.OUT, initial=0)  # start latch & clock low
      GPIO.setup(self.clockPin, GPIO.OUT, initial=0)  

  def __ping (self,p):
      GPIO.output(p,1) 	    # ping the clock pin to shift register data
      time.sleep(0)
      GPIO.output(p,0)
  
  def shiftByte(self,pattern):
      for i in range(8):
        GPIO.output(self.dataPin, pattern & (1<<i))
        self.__ping(self.clockPin)
      self.__ping(self.latchPin)
