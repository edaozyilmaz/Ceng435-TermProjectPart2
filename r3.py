from time import sleep
import sys
import signal
from socket import *
from threading import Thread

sPort = 29614
port = 29613
dPort = 29610

Ack = [0]*5556	#check ack to dcide whether the data is received
DataRec = [0]*5556

def sum(data):
    res=0
    for x in data:
        res+=ord(x)
    return res


def r3():
	#receive from s
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('10.10.3.2',port)) #from r3 to s
    i = 0
	while True:
        i+=1
        msg, addr = server.recvfrom(2048)
		clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(msg,('10.10.7.1', dPort)) #from r3 to d
		clientSocket.close()


def r3d():
	#send to d
	R3_d = socket(AF_INET, SOCK_DGRAM)
	R3_d.bind(('10.10.7.2', port)) #ip of d
    i = 0
	while True:
        i+=1
		#receive message Ack from d
		msgAck, add = R3_d.recvfrom(2048)
		#send message Ack to s
		clientSocketAck = socket(AF_INET, SOCK_DGRAM)
		clientSocketAck.sendto(msgAck,('10.10.3.1',29614))
		clientSocketAck.close()

sender3 = Thread(target = r3,args=())
sender3d = Thread(target = r3d,args=())
sender3.start()
sender3d.start()
sender3.join()
sender3d.join()
