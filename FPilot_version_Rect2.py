import numpy as np, cv2, datetime, time
import socket, binascii, serial, os, sys, tty, termios, math
import imutils
from imutils.video import VideoStream
import argparse
from collections import deque

DEVICE = '/dev/ttyACM1'
BAUD = 9600
ser = serial.Serial(DEVICE, BAUD)

ap=argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-v", "--video", help="path to video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args=vars(ap.parse_args())

red_lower = (1, 1, 1)
red_upper = (255, 240, 240)
green_lower = (40, 50, 25)
green_upper = (80, 255, 150)
pts = deque(maxlen=args["buffer"])

camera = VideoStream(usePiCamera=args["picamera"] > 0).start()
#go to target
theta_total="1/011/2/020/3/155/4/080"
print theta_total
print 'going to target'
ser.write(theta_total)
#time.sleep(2)
ser.write(theta_total)
#time.sleep(8)

time.sleep(2.0)
while(1):
        (frame)=camera.read()        
        frame=imutils.resize(frame, width=400)
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv, green_lower, green_upper)
        cv2.imshow('OrigFrame',frame)
        #cv2.imshow('Original Mask',mask)
        mask=cv2.erode(mask, None, iterations=3)
        #cv2.imshow('Erode Mask',mask)
        mask=cv2.dilate(mask, None, iterations=3)
        cv2.imshow('Dilate Mask',mask)
        #contours
        cnts=cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        #time.sleep(10)
        center=None
        if len(cnts)>0:
                cnt=cnts[0]
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box=np.int0(box)
                x1=(box[3][0]-(box[0][0]))
                y1=(box[3][1]-(box[0][1]))
                print 'x1', x1
                print 'y1', y1
                
                if ((abs(x1)>70)or (abs(y1)>70)):
                        #time.sleep(5)
                        cv2.imshow('OrigFrame',frame)
                        execfile("InvKin_Control.py")
                        print "picking up"
                cv2.drawContours(frame,[box],0,(0,0,255),2)                
        
        key=cv2.waitKey(1)& 0xFF
        if key==ord("q"):
               break


camera.stop()
cv2.destroyAllWindows()
          
