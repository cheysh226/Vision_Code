import argparse
import cv2
from rehbr.system import DigitalOutput, Camera
from rehbr.config import Params
from rehbr.mainfunctions import Queue,confirm_circleinfo, get_current_bgr_value
import time
import logging
import smbus
import datetime

bus = smbus.SMBus(1)
device_address = 0x63
color_value = 0x00
par = Params()

# 로거 설정
logging.basicConfig(
    filename='RGB_LOG.txt',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def run_process(camera_address, area_size) :
    cam = Camera(camera_address)
    ret = True
    circleinfo = []
    try :
        while ret :
            ret, img = cam.read()
            img = cv2.resize(img,(600,337))
            # cv2.imshow("CCTV_TEST",img)
            # cv2.waitKey(1)
            circleinfo = confirm_circleinfo(
                img,
                par.hough_circles,
                circleinfo
                )
            # if circleinfo exists, 
            if len(circleinfo)!= 0 :
                B, G, R = get_current_bgr_value(img,circleinfo,area_size)
                color_value = int(R * 4056 / 255)
                regis_pos = int(color_value / 255)
                bus.write_byte_data(device_address, regis_pos, color_value % 255)

                r_str = f"{R:4}"
                g_str = f"{G:4}"
                b_str = f"{B:4}"
                
                # 로그 메시지 작성
                message = f"R: {r_str} G: {g_str} B: {b_str}"
                logging.info(message)
                                    
            time.sleep(1)
    except Exception as e:
        logging.error(f"Error: {str(e)}")




def run_logging_loop(max_attempts=10):
    attempt = 0
    while True:
        try:
            attempt += 1
            if attempt > max_attempts:
                logging.error("최대 시도 횟수 초과")
                break

            run_process(
                par.camera_address(**par.camera_info, test = True),
                area_size=30
            )
            # 성공 시 시도 횟수 리셋
            attempt = 0
            # 1초 대기
            time.sleep(1)
        
        except Exception as e:
            logging.error(f"루프 실패, 다시 시도합니다: {str(e)}")
            # 1초 대기 후 다시 시도
            time.sleep(1)

# 로그 루프 실행
run_logging_loop()