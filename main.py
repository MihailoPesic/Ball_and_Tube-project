import cv2
import numpy as np
import os
import sys
import time

import serial

arduino = serial.Serial(port='COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=.1)


cam=cv2.VideoCapture(0)
lower_limit = np.array([0, 0, 220])
upper_limit = np.array([50, 50, 255])
real_height=1.97
pixel_height=0

point_low = [0, 0]
point_high = [0, 0]

mid_x = 0
mid_y = 0
height_ratio=0

want_height = 1.5
height_before = 0
V0 = 17
Vmax = 29
Vmin = 13

kd = 10
kv = 2

serial.Serial

def main():
    running=True
    
    detected_pixels_sum_x = 0    
    detected_pixels_sum_y = 0
    n_detected_pixels = 0
    

    input()
    result,img= cam.read()
    img=img[350:380, 100:650]

    detected_pixels_sum_x, detected_pixels_sum_y, n_detected_pixels, img = maskColor(img, lower_limit, upper_limit, 0, 0, 0)
    point_low = [int(detected_pixels_sum_x / n_detected_pixels), int(detected_pixels_sum_y / n_detected_pixels)]

    arduino.write(bytes(str(255), 'utf-8'))
     

    # serial.Serial.close
    
    input()
    result,img= cam.read()
    img=img[350:380, 100:650]


    detected_pixels_sum_x, detected_pixels_sum_y, n_detected_pixels, img = maskColor(img, lower_limit, upper_limit, 0, 0, 0)
    point_high = [int(detected_pixels_sum_x / n_detected_pixels), int(detected_pixels_sum_y / n_detected_pixels)]
    
    
    pixel_height=point_low[0]-point_high[0]
    
    


    global height_ratio
    #height_ratio=real_height/pixel_height
    height_ratio=real_height/pixel_height

    
    
    print(point_low, point_high)
    print(height_ratio)
    global height_before
    running=True
    while running==True:
        result, img = cam.read()
        img=img[350:380, 100:650]

        #if result:
            

        a, b, c, img = maskColor(img, lower_limit, upper_limit, 0, 0, 0)
        real_point = [int(a / c), int(b / c)]
        height = real_height-((real_point[0] - point_high[0])*(height_ratio))-0.08

        #cv2.imshow('image', img)
        #cv2.waitKey(1)
        
        delta_height = want_height - height

        voltage = V0 + delta_height * kd + (height - height_before) * kv

        height_before = height

        if(voltage>Vmax):
            voltage=Vmax
        if(voltage<Vmin):
            voltage=Vmin

        calcVolt = str(int((voltage / Vmax) * 255))
        print(calcVolt)
        arduino.write(bytes('50', 'utf-8'))
        arduino.readline()
        serial.Serial.close

        #arduino.write(bytes(str(120), 'utf-8')) 
        
        time.sleep(0.01)
    
    # cam = cv2.VideoCapture(0)
    # result, img = cam.read()


def update():
    arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

    global height_before
    running=True
    while running==True:
        result, img = cam.read()
        img=img[350:380, 100:650]

        if result:
            

            a, b, c, img = maskColor(img, lower_limit, upper_limit, 0, 0, 0)
            real_point = [int(a / c), int(b / c)]
            height = real_height-((real_point[0] - point_high[0])*(height_ratio))-0.08



            cv2.imshow('image', img)
            cv2.waitKey(1)
        
        delta_height = want_height - height

        voltage = V0 + delta_height * kd + (height - height_before) * kv

        height_before = height

        if(voltage>Vmax):
            voltage=Vmax
        if(voltage<Vmin):
            voltage=Vmin

        calcVolt = str(int((voltage / Vmax) * 255))
        print(calcVolt)
        serial.close()
        time.sleep(1)








import matplotlib.pyplot as plt

def maskColor(img, lower_limit, upper_limit, a, b, c):

    for i in range (0, len(img)):
        for j in range(0, len(img[0])):
            if img[i][j][0] < lower_limit[0] or img[i][j][0] > upper_limit[0] or img[i][j][1] < lower_limit[1] or img[i][j][1] > upper_limit[1] or img[i][j][2] < lower_limit[2] or img[i][j][2] > upper_limit[2]:
              img[i][j] = [0, 0, 0]
            else:
                a += j
                b += i
                c += 1
    if c==0:
        c=1

    return a, b, c, img
       



if __name__ == '__main__':
    main()