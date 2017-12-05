import time
import picamera
import numpy as np

with picamera.PiCamera() as camera:
        camera.resolution = (320,240)
        camera.framerate = 24
        time.sleep(2)
        image = np.empty((240 * 320 * 3,), dtype=np.uint8)
        camera.capture(image, 'rgb')
        with open('out0','wb',) as d:
            d.write(image.tostring())
        x = 0
        t = time.time();
        for x in range (0,(240*320*3)-3,3):
            if(image[x] > 200 and image[x+1] < 150 and image[x+2] < 150):
                image[x] = image[x+1] = image[x+2] = 255
            else:
                image[x] = image[x+1] = image[x+2] = 0
        image = image.reshape((240,320,3))
        print (time.time() - t)
        with open('out','wb') as f:
            f.write(image.tostring())
        print (time.time() - t)
