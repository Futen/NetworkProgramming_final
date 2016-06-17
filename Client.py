import socket
import sys
import json

HOST, PORT = sys.argv[1], int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
while True:
    test_data = dict({'command':'show', 'data':'ggwp'})
    sock.sendall(json.dumps(test_data) + '\n')
    data = json.loads(sock.recv(1024))
    print data['data']
    print 'one loop'
    break
