import sys
import os
import subprocess
import socket
import SocketServer as ss
import threading
import json

HOST = '127.0.0.1'
PORT = int(sys.argv[1])

def SuccessMessage():
    return dict({'data': 'ok'})
def FailMessage():
    return dict({'data': 'gg'})

class MyHandler(ss.StreamRequestHandler):
    def handle(self):
        #print self.request
        while True:
            self.data = self.rfile.readline()[0:-1]
            self.data = json.loads(self.data)
            #self.wfile.write(json.dumps(test))
class ThreadedTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    pass
#def client(ip, port, message):
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), MyHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    server_thread.start()
