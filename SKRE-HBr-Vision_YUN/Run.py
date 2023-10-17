import argparse
import cv2
from rehbr.system import DigitalOutput, Camera
from rehbr.config import Params
from rehbr.mainfunctions import Queue,confirm_circleinfo,get_current_r_value
import time
import logging
import smbus

bus = smbus.SMBus(1)
device_address = 0x63
color_value = 0x00

def run_process(camera_address, mean_thres, area_size) :
    cam = Camera(camera_address)
    ret = True
    ext_bool = False
    circleinfo = []
    i = 0
    j = 0
    RQ = Queue(5)
    try :
        while ret :
            if cam is None :
                if j > 100 :
                    img = cv2.imread("/home/pi/SKRE-HBr-Vision/masked_img.png")
                else :
                    img = cv2.imread("/home/pi/SKRE-HBr-Vision/img.png")
                j += 1
            else :
                ret,img = cam.read()
            img = cv2.resize(img,(600,337))
            cv2.imshow("CCTV_TEST",img)
            cv2.waitKey(1)
            # Needs Resizing due to memory constraint
            if i > 10 :
                # find circle if empty
                circleinfo = confirm_circleinfo(
                    img,
                    par.hough_circles,
                    circleinfo
                    )
                # if circleinfo exists, 
                if len(circleinfo)!= 0 :
                    R = get_current_r_value(img,circleinfo,area_size)
                    RQ.enqueue(R)
                    color_value = int(R* 4056 / 255)
                    regis_pos = int(color_value / 255)
                    bus.write_byte_data(device_address, regis_pos, color_value % 255)
                    print(int(R))
            i+=1
            time.sleep(1)
    except Exception as e:
        print(e)

par = Params()
run_process(
	par.camera_address(**par.camera_info, test = True),
    mean_thres=100,
    area_size=30
)
