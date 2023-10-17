class Params :

    hough_circles = {
        'method' : 3,
        'dp' : 1,
        'minDist' : 100,
        'param1' : 30,
        'param2' : 50,
        'minRadius' : 0,
        'maxRadius' : 300
    }

    camera_info = {
        'ip' : '192.168.9.2',
        'port' : '554',
        'user_name' : 'admin',
        'password' : 'admin123!'
    }

    serial_info = {
        'port' : '/dev/serial1',
        'baudrate' : 9600,
        'parity' : 'N',
        'stopbits' : 1,
        'bytesize' : 8,
    }

    def camera_address(self,ip,port,user_name,password,test=False) :
        if test :
            return "http://192.168.43.1:4747/video"
        else :
            return f"rtsp://{user_name}:{password}@{ip}:{port}/profile5/media.smp"
