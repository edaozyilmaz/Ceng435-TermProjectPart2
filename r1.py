from time import sleep
import sys
import signal
from socket import *
from threading import Thread

sPort = 29614
port = 29611
dPort = 29610

def sum(data):
    res=0
    for x in data:
        res+=ord(x)
    return res


def r1():
	#receive from s
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('10.10.1.2',port)) #from r1 to s
    i = 0
	while True:
        i+=1
        msg, addr = server.recvfrom(2048)
        print i
        #print msg
		clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(msg,('10.10.4.2', dPort)) #from r1 to d
		clientSocket.close()

def r1d():
	#send to d
	R1_d = socket(AF_INET, SOCK_DGRAM)
	R1_d.bind(('10.10.4.1', port)) #ip of d
    i = 0
	while True:
        i+=1
		#receive message Ack from d
		msgAck, add = R1_d.recvfrom(2048)
		#send message Ack to s
		clientSocketAck = socket(AF_INET, SOCK_DGRAM)
		clientSocketAck.sendto(msgAck,('10.10.1.1',sPort))
		clientSocketAck.close()


sender1 = Thread(target = r1,args=())
sender1d = Thread(target = r1d,args=())

sender1.start()
sender1d.start()
sender1.join()
sender1d.join()
