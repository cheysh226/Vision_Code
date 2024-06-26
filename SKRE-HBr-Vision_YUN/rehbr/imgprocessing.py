import numpy as np
import cv2

def detect_circle_areas(img,params: dict ,blurparam=25) :
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray,blurparam)
    circles = cv2.HoughCircles(blur,**params)
    if circles is not None :
        circles = np.uint16(np.around(circles))
        result = circles[0,:]
    else :
        result = []
    return result

def get_target_area(img,circle,r=30) :
    assert len(circle) == 3 , f"Circle Info length should be 3, current input has length of {len(circle)}"
    x,y,r0 = circle
    if r is None :
        r = r0
    roi = img[y-r:y+r, x-r:x+r]
    return roi

def get_mean_bgr(img) :
    # ver. 0.0.1. (2023.03.20)
    b,g,r = np.mean(img,axis=(0,1))
    return b,g,r
