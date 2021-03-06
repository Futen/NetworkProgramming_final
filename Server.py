import sys
import os
import subprocess
import socket
import SocketServer as ss
import threading
import json
import Parameter as Pm
import DataBase as DB
import ChatRoom as CR

#HOST = '127.0.0.1'
HOST = '192.168.1.105'
PORT = int(sys.argv[1])

SocketLst = {}
AddrLst = {}
def SuccessMessage(command):
    return json.dumps(dict({'command':command, 'data': 'ok'}))
def FailMessage(command):
    return json.dumps(dict({'command':command, 'data': 'gg'}))
def RequestIP(dataIn):
    data = {}
    who = dataIn['who']
    data['command'] = dataIn['command']
    if who in SocketLst and who in AddrLst:
        #data['ip'] = list(AddrLst[who][0].client_address)
        data['ip'] = [AddrLst[who][2], AddrLst[who][1]]
        data['ip'][1] = AddrLst[who][1]
        data['port'] = AddrLst[who][1]
    return json.dumps(data)
def PikaRequest(dataIn):
    data = {'command':dataIn['command']}
    if dataIn['to'] in SocketLst and dataIn['to'] in AddrLst:
        data['from'] = dataIn['account']
    return json.dumps(data)
def PikaAccept(dataIn):
    data = {'command':dataIn['command']}
    data['ip'] = AddrLst[dataIn['account']][2]
    return json.dumps(data)
def PikaReject(dataIn):
    data = {'command':dataIn['command']}
    data['from'] = dataIn['account']
    return json.dumps(data)
class MyHandler(ss.StreamRequestHandler):
    def handle(self):
        print (self.client_address)
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
                    account = self.recvData['account']
                    result = DB.UserLogin(self.recvData)
                    #print SocketLst
                    if result:
                        print self.recvData
                        SocketLst[self.recvData['account']] = self.request
                        AddrLst[self.recvData['account']] = []
                        AddrLst[self.recvData['account']].append(self)
                        AddrLst[self.recvData['account']].append(self.recvData['port'])
                        AddrLst[self.recvData['account']].append(self.recvData['localip'])
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
                elif command == Pm.GETPROFILE:
                    print command
                    sendData = DB.GetProfile(self.recvData)
                    self.wfile.write(sendData)
                elif command == Pm.GETFRIENDPROFILE:
                    print command
                    sendData = DB.GetFriendProfile(self.recvData)
                    self.wfile.write(sendData)
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
                    print self.recvData
                    result = DB.FriendRequest(self.recvData)
                    print result
                    if result:
                        DB.SaveUserData()
                        if self.recvData['to'] in SocketLst:
                            sendData = DB.FriendRequestPacket(self.recvData)
                            print sendData
                            SocketLst[self.recvData['to']].sendall(sendData)
                        #self.wfile.write(SuccessMessage(command))
                    else:
                        pass
                        #self.wfile.write(FailMessage(command))
                elif command == Pm.SHOWFRIENDREQUEST:
                    print command
                    data = DB.GetAllFriendRequest(self.recvData)
                    print data
                    self.wfile.write(data)
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
                elif command == Pm.ASKINGINFO:
                    print command
                    data = CR.AskingUpdate(self.recvData)
                    #print data
                    self.wfile.write(data)
                elif command == Pm.ACCEPTINVITE:
                    print command
                    result = DB.AcceptFriendRequest(self.recvData)
                    if not result:
                        print 'accept gg'
                elif command == Pm.REJECTINVITE:
                    print command
                    result = DB.RejectFriendRequest(self.recvData)
                    if not result:
                        print 'reject gg'
                elif command == Pm.CHATTOONE:
                    print command
                    sendData = CR.CreateMessage(self.recvData)
                    if self.recvData['to'] in SocketLst:
                        SocketLst[self.recvData['to']].sendall(sendData)
                elif command == Pm.SOUNDREQUEST:
                    print command
                    sendData = CR.SoundRequest(self.recvData)
                    if self.recvData['to'] in SocketLst:
                        SocketLst[self.recvData['to']].sendall(sendData) 
                elif command == Pm.SENDSOUND:
                    print command
                    sendData = CR.CreateSoundMessage(self.recvData)
                    if self.recvData['to'] in SocketLst:
                        SocketLst[self.recvData['to']].sendall(sendData)
                elif command == Pm.CREATEGROUP:
                    print command
                    result = CR.CreateGroup(self.recvData)
                    CR.SaveGroupData()
                elif command == Pm.ADDMEMBER:
                    print command
                    result = CR.AddMemberToGroup(self.recvData) 
                    #print result
                    #print self.recvData
                    if result:
                        CR.SaveGroupData()
                        #print CR.GroupTable
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                elif command == Pm.REMOVEMEMBER:
                    print command
                    result = CR.RemoveMemberFromGroup(self.recvData)
                    if result:
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                elif command == Pm.CHATTOGROUP:
                    print command
                    sendData = CR.CreateGroupMessageDict(self.recvData)
                    sendStr = json.dumps(sendData)
                    for member in sendData['member']:
                        if member in SocketLst and not member == self.recvData['account']:
                            SocketLst[member].sendall(sendStr)
                elif command == Pm.REQUESTIP:
                    print command
                    sendData = RequestIP(self.recvData)
                    self.wfile.write(sendData)
                elif command == Pm.PIKAREQUEST:
                    print command
                    sendData = PikaRequest(self.recvData)
                    SocketLst[self.recvData['to']].sendall(sendData)
                elif command == Pm.ACCEPTPIKA:
                    print command
                    sendData = PikaAccept(self.recvData)
                    SocketLst[self.recvData['to']].sendall(sendData)
                elif command == Pm.REJECTPIKA:
                    print command
                    sendData = PikaReject(self.recvData)
                    SocketLst[self.recvData['to']].sendall(sendData)
                elif command == Pm.REMOVEFRIEND:
                    print command
                    result = DB.RemoveFriend(self.recvData)
                    if result:
                        self.wfile.write(SuccessMessage(command))
                    else:
                        self.wfile.write(FailMessage(command))
                #print DB.UserData
                #self.data = json.loads(self.data)
                #self.wfile.write(self.data)
        except socket.error:
            try:
                a = account
                print 'account leave:'%account
                if a in DB.OnlineLst:
                    DB.OnlineLst.remove(a)
                if a in DB.BusyLst:
                    DB.BusyLst.remove(a)
                if a in DB.OfflineLst:
                    DB.OfflineLst.remove(a)
                if a in DB.LoginLst:
                    DB.LoginLst.remove(a)
            except:
                pass

        try:
            for one in SocketLst:
                if SocketLst[one] is self.request:
                    key = one
                    a = key
                    break
            SocketLst.pop(key, None)
            if a in DB.OnlineLst:
                DB.OnlineLst.remove(a)
            if a in DB.BusyLst:
                DB.BusyLst.remove(a)
            if a in DB.OfflineLst:
                DB.OfflineLst.remove(a)
            if a in DB.LoginLst:
                DB.LoginLst.remove(a)

        except KeyError:
            pass

        print SocketLst
        print DB.LoginLst
class ThreadedTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    pass
#def client(ip, port, message):
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), MyHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    server_thread.start()
