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

SocketLst = {}
def SuccessMessage(command):
    return json.dumps(dict({'command':command, 'data': 'ok'}))
def FailMessage(command):
    return json.dumps(dict({'command':command, 'data': 'gg'}))

class MyHandler(ss.StreamRequestHandler):
    def handle(self):
        print 'GGWP'
        try:
            while True:
                try:
                    self.recvData = json.loads(self.rfile.readline()[0:-1])
                    #print self.recvData
                except ValueError:
                    break
                command = self.recvData['command']
                if command == Pm.CREATEACCOUNT:
                    print command
                    result = DB.CreateAccount(self.recvData)
                    if result:
                        DB.SaveUserData()
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                elif command == Pm.USERLOGIN:
                    print command
                    result = DB.UserLogin(self.recvData)
                    SocketLst[self.recvData['account']] = self.request
                    #print SocketLst
                    if result:
                        DB.SaveUserData()
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                elif command == Pm.USERLOGOUT:
                    print command
                    result = DB.UserLogout(self.recvData)
                    if result:
                        DB.SaveUserData()
                        #SocketLst.pop(self.recvData['account'], None)
                        #print SocketLst
                        break
                        #self.wfile.write(SuccessMessage(command))
                    else:
                        pass
                        #self.wfile.write(FailMessage(command))

                elif command == Pm.MODIFYACCOUNT:
                    print command
                    result = DB.ModifyAccount(self.recvData)
                    if result:
                        DB.SaveUserData()
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                    print DB.UserData
                elif command == Pm.DELETEACCOUNT:
                    print command
                    result = DB.DeleteAccount(self.recvData)
                    if result:
                        DB.SaveUserData()
                        #self.wfile.write(SuccessMessage(command))
                    else:
                        pass
                        #self.wfile.write(FailMessage(command))
                elif command == Pm.SEARCHACCOUNT:
                    print command
                    result = DB.SearchUser(self.recvData)
                    if result:
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                elif command == Pm.FRIENDREQUEST:
                    print command
                    result = DB.FriendRequest(self.recvData)
                    if result:
                        if self.recvData['to'] in SocketLst:
                            sendData = DB.FriendRequestPacket(self.recvData)
                            SocketLst[self.recvData['to']].sendall(sendData)
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                elif command == Pm.CHANGESTATE:
                    print command
                    result = DB.ChangeState(self.recvData)
                    if result:
                        self.wfile.write(SuccessMessage(command))
                        print DB.OnlineLst
                        print DB.BusyLst
                        print DB.OfflineLst
                    else:
                        self.wfile.write(FailMessage(command))
                #print DB.UserData
                #self.data = json.loads(self.data)
                #self.wfile.write(self.data)
        except socket.error:
            pass
        try:
            for one in SocketLst:
                if SocketLst[one] is self.request:
                    key = one
                    break
            SocketLst.pop(key, None)
        except KeyError:
            pass
        print SocketLst
class ThreadedTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    pass
#def client(ip, port, message):
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), MyHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    server_thread.start()
