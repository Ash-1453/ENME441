import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BCM)
pin=[14,15,18,23,24,25,8,7,12,16]
pwm=[]
b=[]
y=0
phi=math.pi/11
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def switch(channel):
	global phi
	phi=phi*-1

for x in pin:
	GPIO.setup(x, GPIO.OUT, initial=0)
	pwm.append(GPIO.PWM(x,500))
	pwm[y].start(0)
	
	y+=1
GPIO.add_event_detect(17, GPIO.RISING, callback=switch,bouncetime=100)
try:
	while True:
		y=0
		for x in pin:
			z=time.time()
			brightness=(100*(math.sin(math.pi*.2*2*z-phi*y))**2)
			pwm[y].ChangeDutyCycle(brightness)
			y+=1
except KeyboardInterrupt: # if user hits ctrl-C
	print('\nExiting')
except Exception as e:
	print('/ne')
y=0
for x in pin:	
	pwm[y].stop()
	y+=1
GPIO.cleanup()
