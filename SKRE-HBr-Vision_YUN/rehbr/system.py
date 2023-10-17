import cv2
import serial
import time
import RPi.GPIO as gpio 
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

class DCS() :
    def __init__(self,port) :
        self.ser = serial.Serial(port=port)
    
    def send(self,byte_string) :
        self.ser.write(byte_string)
    
    def read(self) :
        return self.ser.readline()
    
    def close(self) :
        self.ser.close()

class SlaveServer() :

    def __init__(self) :
        self.store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),  # Discrete Inputs
            co=ModbusSequentialDataBlock(0, [0] * 100),  # Coils
            hr=ModbusSequentialDataBlock(0, [0] * 100),  # Holding Registers
            ir=ModbusSequentialDataBlock(0, [0] * 100),  # Input Registers
        )
        self.context = ModbusServerContext(slaves=self.store, single=True)
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'Raspberry Pi'
        self.identity.ProductCode = 'RPi'
        self.identity.VendorUrl = 'https://www.raspberrypi.org/'
        self.identity.ProductName = 'Raspberry Pi Modbus Slave Server'
        self.identity.ModelName = 'Raspberry Pi 3'
        self.identity.MajorMinorRevision = '1.0'

    def update_register(self,val,address=0,function_code=3) :
        self.context[0].setValues(function_code,address,[val])

    def get_register_value(self,address,length=1,function_code=3) :
        return self.context[0].getValues(function_code,address,length)

        
        

    
class Camera() :

    def __init__(self,address) :
        self.cap = cv2.VideoCapture(address)

    def check(self) :
        return self.cap.isOpened()

    def close(self) :
        self.cap.release()

    def read(self) :
        return self.cap.read()

gpio.setmode(gpio.BOARD)       

class RPIOutput() :
    
    def __init__(self,pin_no) :
        gpio.setup(pin_no,gpio.OUT)

    def close(self) :
        gpio.cleanup()




class AnalogOutput(RPIOutput) :

    def __init__(self,pin_no,freq=1000,start=0) :
        super().__init__(pin_no)
        self.out = gpio.PWM(pin_no,freq)
        self.out.start(start)
    
    def update(self,n) :
        assert (n<=100)&(n>=0), "n should be an integer between 0 and 100."
        self.out.ChangeDutyCycle(n)

class DigitalOutput(RPIOutput) :

    def __init__(self,pin_no) :
        super().__init__(pin_no)
        self.pin_no = pin_no
        gpio.output(pin_no,0)
    
    def update(self,n) :
        assert n in [0,1], "n should be one of 0,1 for digital output."
        gpio.output(self.pin_no,n)

class ButtonInput() :
    def __init__(self,pin_no) :
        gpio.setmode(gpio.BOARD)
        gpio.setup(pin_no,gpio.IN)
        self.status = False
        self.pin_no = pin_no
    
    def get_input(self) :
        inp = gpio.input(self.pin_no)
        if not inp :
            time.sleep(0.5)
            self.status = not self.status
        return not inp
