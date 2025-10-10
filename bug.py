import RPi.GPIO as GPIO
import time 
from shifter import Shifter
import random
import threading
GPIO.setmode(GPIO.BCM)
s1, s2, s3,= 2,3,4 
GPIO.setup(s1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
class Bug:
	def __init__(self,timestep=.1, x=3,isWrapOn=False):
		self.timestep=timestep
		self.x=x
		self.isWrapOn=isWrapOn
		self.__shifter=Shifter(23,24,25)
		self.active=False
	def _move(self): # i had to add this method because the code was getting stuck executing the start code and wasn't taking in the inputs so weh had to make start a seperate thread it can be a thread because we only need to have the 2 threads running for this purpose 
		while self.active:

			on=1<<self.x
			self.__shifter.shiftByte(on)
			self.x+=random.choice([-1,1])
			if self.isWrapOn==True:
				if self.x>7:
					self.x =0
				elif self.x<0:
					self.x=7
			elif self.isWrapOn==False:
				if self.x<0:
					self.x=0
				elif self.x>7:
					self.x=7
			time.sleep(self.timestep)
	def start(self):
		if self.active==False:
			self.active=True
			self._thread=threading.Thread(target=self._move,daemon=True)
			self._thread.start()

	def stop(self):
		self.active=False
		on=0
		self.__shifter.shiftByte(on)

bug=Bug()
def fn():
	bug.isWrapOn= not bug.isWrapOn
#GPIO.add_event_detect(s2, GPIO.BOTH, callback=fn, bouncetime=100) since i added another thread this doesedn work so gonna execute it in my main code 
try:
	while True:
		if GPIO.input(s1)==True and bug.active==False:
			bug.start()
		elif GPIO.input(s1)==False:
			bug.stop()
		
		if GPIO.input(s3)==True:
			bug.timestep=bug.timestep/3
		else:
			bug.timestep=.1
		s2in1=False
		s2in2=GPIO.input(s2)
		if  s2in1!=s2in2:
			bug.isWrapOn= not bug.isWrapOn
		s2in1=s2in2


except KeyboardInterrupt:
	GPIO.cleanup()
