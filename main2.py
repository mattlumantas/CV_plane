import time
import picamera
import cv2
import numpy as np
import pigpio as io
#from gpiozero import LEDBoard,LED
X_PIN = 25
Y_PIN = 26

pi = io.pi()
pi.set_mode(X_PIN,io.OUTPUT)
pi.set_mode(Y_PIN,io.OUTPUT)

with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        camera.framerate = 24
        time.sleep(2)
        image = np.empty((480 * 640 * 3,), dtype=np.uint8)
        t = time.time()
        camera.start_preview()
        time.sleep(2)
        camera.capture(image, 'bgr')
        camera.stop_preview()
        image = image.reshape((480,640,3))

        image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        """lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(image_hsv,lower_red,upper_red)
        
        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(image_hsv,lower_red,upper_red)

        mask = mask0+mask1"""
       
        lower_red_rgb = np.array([200,0,0])
        upper_red_rgb = np.array([255,150,150])
        mask = cv2.inRange(image_rgb,lower_red_rgb,upper_red_rgb)
        output = image_rgb.copy()
        output = cv2.bitwise_and(output,output,mask = mask)
        
        output_rgb = cv2.cvtColor(output,cv2.COLOR_HSV2RGB)
        points = cv2.findNonZero(mask)
        """with open('points','wb') as g:
            g.write(points.tostring())"""
        location = np.average(points,axis=0)
        error = np.subtract(location,[320,240])
        divarray = np.array([128,96])
	mapped = location / divarray
	np.round(mapped)
	mapped = mapped.astype(int)
        np.savetxt('points',points,fmt='%s')
        print (location)
        print (mapped)
        print (error)

	#ledy = LEDBoard(2,3,4,17,27)
	#ledx = LEDBoard(22,10,9,11,5)
	x = mapped[0]
	print(x)
	#y = mapped[1]
	#ledy[x[0]].on()
	#ledx[x[1]].on()
	#time.sleep(3)

        #print(time.time()-t)
        with open('out','wb') as d:
            d.write(image_rgb.tostring())

        with open('out0','wb') as f:
            f.write(output.tostring())
