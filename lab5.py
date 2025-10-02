import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BCM)
pin=[14,15,18,23,24,25,8,7,12,16]
pwm=[]
b=[]
y=0

for x in pin:
	GPIO.setup(x, GPIO.OUT, initial=0)
	pwm[y]=GPIO.PWM(x,500)
	pwm[y].start(0)
	
	y+=1

try:
	while True:
		y=0
		for x in pin:
			z=time.time()
			b[y]=100*(math.sin(2*math.pi*.2*z-((math.pi*y)/11)))^2
			pwm[y].ChangeDutyCycle(b[y])
			y+=1
	except KeyboardInterrupt: # if user hits ctrl-C
	print('\nExiting')
for x in pin:	
	pwm[y].stop()
GPIO.cleanup()
