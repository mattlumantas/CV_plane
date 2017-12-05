import time
import picamera
import cv2
import numpy as np
import pigpio as io
X_PIN = 2
Y_PIN = 3

pi = io.pi()
pi.set_mode(X_PIN,io.OUTPUT)
pi.set_mode(Y_PIN,io.OUTPUT)
lower_red = np.array([200,0,0])
upper_red = np.array([255,150,150])
prev_error = np.empty((2,), dtype=np.uint8)
with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        camera.framerate = 24
        time.sleep(2)
        image = np.empty((480 * 640 * 3,), dtype=np.uint8)
	pi.set_servo_pulsewidth(Y_PIN,1900)
	time.sleep(1)
	pi.set_servo_pulsewidth(Y_PIN,800)
	time.sleep(1)
	while True:
		image = image.reshape ((480*640*3))
	        camera.capture(image, 'rgb')
		print ('Image taken!')
	        image = image.reshape((480,640,3))
	        mask = cv2.inRange(image,lower_red,upper_red)
	        points = cv2.findNonZero(mask)
		if np.any(points):
			print ('Point found!')
		        location = np.average(points,axis=0)
		        error = np.subtract(location,[320,240])
			delta = error - prev_error
			print ('Error = %d',error)
			print ('Delta = %d',delta)
			pi.set_servo_pulsewidth(X_PIN,1750 - (2*error[0][0]) + delta[0][0])
			pi.set_servo_pulsewidth(Y_PIN,1350 + (3*error[0][1]) - delta[0][1])
			prev_error = error
		else:
			print('No point found!')
