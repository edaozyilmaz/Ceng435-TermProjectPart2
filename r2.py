from time import sleep
import sys
import signal
from socket import *
from threading import Thread

sPort = 29614
port = 29612
dPort = 29610

def sum(data):
    res=0
    for x in data:
        res+=ord(x)
    return res


def r2():
	#receive from s
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('10.10.2.1',port)) #from r2 to s
	#send to d
    i = 0
	while True:
        i+=1
        msg, addr = server.recvfrom(2048)
        #print msg
		clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(msg,('10.10.5.2', dPort)) #from r2 to d
		clientSocket.close()

def r2d():
	#send to d
	R2_d = socket(AF_INET, SOCK_DGRAM)
	R2_d.bind(('10.10.5.1', port)) #ip of d
    i = 0
	while True:
        i+=1
		#receive message Ack from d
		msgAck, add = R2_d.recvfrom(2048)
		#send message Ack to s
		clientSocketAck = socket(AF_INET, SOCK_DGRAM)
		clientSocketAck.sendto(msgAck,('10.10.2.2',sPort))
		clientSocketAck.close()

sender2 = Thread(target = r2,args=())
sender2d = Thread(target = r2d,args=())
sender2.start()
sender2d.start()
sender2.join()
sender2d.join()
