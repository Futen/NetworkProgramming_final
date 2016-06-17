import socket
import sys
import json
import Parameter as Pm

def IsOk(data):
    if data['data'] == 'ok':
        return True
    else:
        return False

if __name__ == '__main__':
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    while True:
        command = raw_input('your command: ')
        #test_data = dict({'command':'show', 'data':'ggwp'})
        if command == Pm.CREATEACCOUNT:
            account = raw_input('your account: ')
            password = raw_input('your password: ')
            nickname = raw_input('your nickname: ')
            sendData = dict({'command':command, 'account':account, 'password':password, 'nickname':nickname})
            sock.sendall(json.dumps(sendData) + '\n')
            recvData = json.loads(sock.recv(1200))
            if IsOk(recvData):
                print 'Create Success'
            else:
                print 'Create Fail'
        elif command == Pm.USERLOGIN:
            account = raw_input('your account: ')
            password = raw_input('your password: ')
            sendData = dict({'command':command, 'account':account, 'password':password})
            sock.sendall(json.dumps(sendData) + '\n')
            recvData = json.loads(sock.recv(1200))
            if IsOk(recvData):
                print 'Login Success'
            else:
                print 'Login Fail'
        elif command == Pm.USERLOGOUT:
            sendData = dict({'command':command, 'account':account})
            print sendData
            sock.sendall(json.dumps(sendData) + '\n')
            recvData = json.loads(sock.recv(1200))
            if IsOk(recvData):
                print 'Logout Success'
                break
            else:
                print 'Logout Fail'
        else:
            print 'Unknown Command'
        #sock.sendall(a + '\n')
        #print sock.recv(1024)
        #data = json.loads(sock.recv(1024))
        #print data['data']
        #print 'one loop'
        #break
    sock.close()
