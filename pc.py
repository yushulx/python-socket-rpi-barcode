from numpysocket import NumpySocket
import cv2
import time
import json
import dbr

def get_time():
    localtime = time.localtime()
    capturetime = time.strftime("%Y%m%d%H%M%S", localtime)
    return capturetime

# Get the license of Dynamsoft Barcode Reader from https://www.dynamsoft.com/CustomerPortal/Portal/Triallicense.aspx
dbr.initLicense('LICENSE KEY')

npSocket = NumpySocket()
npSocket.startServer(9999)

# Receive frames for barcode detection
while(True):
    try:
        frame = npSocket.recieveNumpy()
        # cv2.imshow('PC Reader', frame)
        results = dbr.decodeBuffer(frame, 0x3FF | 0x2000000 | 0x4000000 | 0x8000000 | 0x10000000)
        out = {}
        out['results'] = results

        # Send barcode results to Raspberry Pi
        npSocket.sendJSON({'results': results})
    except:
        break
    
    # Press ESC to exit
    key = cv2.waitKey(20)
    if key == 27 or key == ord('q'):
        break

npSocket.endServer()
print('Closed')