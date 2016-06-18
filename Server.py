import sys
import os
import subprocess
import socket
import SocketServer as ss
import threading
import json
import Parameter as Pm
import DataBase as DB

#HOST = '127.0.0.1'
HOST = '192.168.1.105'
PORT = int(sys.argv[1])

def SuccessMessage(command):
    return json.dumps(dict({'command':command, 'data': 'ok'}))
def FailMessage(command):
    return json.dumps(dict({'command':command, 'data': 'gg'}))

class MyHandler(ss.StreamRequestHandler):
    def handle(self):
        print 'GGWP'
        while True:
            try:
                recvData = json.loads(self.rfile.readline()[0:-1])
                print recvData
            except ValueError:
                break
            command = recvData['command']
            if command == Pm.CREATEACCOUNT:
                print command
                result = DB.CreateAccount(recvData)
                if result:
                    DB.SaveUserData()
                    self.wfile.write(SuccessMessage(command))
                else:
                    self.wfile.write(FailMessage(command))
            elif command == Pm.USERLOGIN:
                print command
                result = DB.UserLogin(recvData)
                if result:
                    DB.SaveUserData()
                    self.wfile.write(SuccessMessage(command))
                else:
                    self.wfile.write(FailMessage(command))
            elif command == Pm.USERLOGOUT:
                print command
                result = DB.UserLogout(recvData)
                if result:
                    DB.SaveUserData()
                    self.wfile.write(SuccessMessage(command))
                else:
                    self.wfile.write(FailMessage(command))

            #print DB.UserData
            #self.data = json.loads(self.data)
            #self.wfile.write(self.data)
class ThreadedTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    pass
#def client(ip, port, message):
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), MyHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    server_thread.start()
