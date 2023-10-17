from rehbr.imgprocessing import *
from rehbr.config import *
import numpy as np

class Queue() :

    def __init__(self,length) :
        self.queue=[]
        self.length=length
    
    def initialize(self) :
        self.queue=[]

    def check_length(self) :
        return len(self.queue) == self.length

    def enqueue(self,value) :
        if self.check_length() :
            self.queue.pop(0)
        self.queue.append(value)

    def get_mean(self) :
        return np.mean(self.queue)

def confirm_circleinfo(img,param,circleinfo) :
    if len(circleinfo)==0 :
        circles = detect_circle_areas(img,param)
        if len(circles)==1 :
            print("Found Circle Area")
            circleinfo = circles[0]
    return circleinfo
        
def get_current_r_value(img, circleinfo,area_size) :
    area = get_target_area(img,circleinfo,area_size)
    return get_mean_r(area)



            
