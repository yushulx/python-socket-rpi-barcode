# Thanks to https://github.com/sabjorn/NumpySocket
import socket
import numpy as np
import sys
import json

if sys.version_info.major == 2:
    from cStringIO import StringIO
else:
    from io import StringIO


class NumpySocket():
    def __init__(self):
        self.address = 0
        self.port = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def startClient(self, address, port):
        self.address = address
        self.port = port
        try:
            self.socket.connect((self.address, self.port))
            print('Connected to %s on port %s' % (self.address, self.port)) 
        except:
            print('Connection to %s on port %s failed.' % (self.address, self.port))
            exit()

    def startServer(self, port):
        self.address = ''
        self.port = port

        self.socket.bind((self.address, self.port))
        self.socket.listen(1)
        print('waiting for a connection...')
        self.connection, self.address = self.socket.accept()
        print('connected to %s' % self.address[0])

    def endClient(self):
        self.socket.shutdown(1)
        self.socket.close()

    def endServer(self):
        self.connection.shutdown(1)
        self.connection.close()

    def sendNumpy(self, image):
        if not isinstance(image, np.ndarray):
            print('not a valid numpy image') 
            return
        f = StringIO()
        np.savez_compressed(f, frame=image)
        f.seek(0)
        out = f.read()
        val = "{0}:".format(len(f.getvalue()))  # prepend length of array
        out = val + out
        try:
            self.socket.sendall(out)
        except Exception:
            exit()

    def sendJSON(self, data):
        out = json.dumps(data)

        try:
            self.connection.sendall(out)
        except Exception:
            exit()

    def receiveJSON(self):
        try:
            chunk = self.socket.recv(1024)    
        except Exception:
            exit()
                
        return json.loads(chunk)

    def recieveNumpy(self):
        length = None
        ultimate_buffer = ""
        while True:
            data = self.connection.recv(1024)
            ultimate_buffer += data
            if len(ultimate_buffer) == length:
                break
            while True:
                if length is None:
                    if ':' not in ultimate_buffer:
                        break
                    # remove the length bytes from the front of ultimate_buffer
                    # leave any remaining bytes in the ultimate_buffer!
                    length_str, ignored, ultimate_buffer = ultimate_buffer.partition(':')
                    length = int(length_str)
                if len(ultimate_buffer) < length:
                    break
                # split off the full message from the remaining bytes
                # leave any remaining bytes in the ultimate_buffer!
                ultimate_buffer = ultimate_buffer[length:]
                length = None
                break
        final_image = np.load(StringIO(ultimate_buffer))['frame']
        return final_image
