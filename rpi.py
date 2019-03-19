from numpysocket import NumpySocket
import cv2
import time
import threading
import json
from multiprocessing import Queue
from scipy.misc import imresize

frame_queue = Queue(1)

# Sending frames and receiving results in the thread.
class SocketThread (threading.Thread):
    def __init__(self, name, npSocket):
        threading.Thread.__init__(self)
        self.name = name
        self.npSocket = npSocket
        self.isRunning = True

    def run(self):      
        while self.isRunning:
            frame = frame_queue.get(timeout=100)

            try:
                start_time = time.time()
                self.npSocket.sendNumpy(frame)
                obj = self.npSocket.receiveJSON()
                print("--- %.2f ms seconds ---" % ((time.time() - start_time) * 1000))
                data = obj['results']

                if (len(data) > 0):
                    for result in data:
                        print("Type: " + result[0])
                        print("Value: " + result[1] + "\n")
                else:
                    print('No barcode detected.')
            except:
                break
            
        self.npSocket.endClient()           

def read_barcode():
    vc = cv2.VideoCapture(0)
    vc.set(3, 640) #set width
    vc.set(4, 480) #set height

    if not vc.isOpened():
        print('Camera is not ready.')
        return

    host_ip = '192.168.8.84' 
    npSocket = NumpySocket()
    npSocket.startClient(host_ip, 9999)

    socket_thread = SocketThread('SocketThread', npSocket)
    socket_thread.start() 

    while vc.isOpened():
        
        ret, f = vc.read()
        cv2.imshow("RPi Reader", f)
        frame = imresize(f, .5)

        key = cv2.waitKey(20)
        if key == 27 or key == ord('q'):   
            socket_thread.isRunning = False
            socket_thread.join() 
            break

        if not socket_thread.is_alive():
            break
        
        try:
            frame_queue.put_nowait(frame)
        except:
            # Clear unused frames
            try:
                while True:
                    frame_queue.get_nowait()
            except:
                pass

    frame_queue.close()
    frame_queue.join_thread()
    vc.release()
    

if __name__ == '__main__':
    read_barcode()