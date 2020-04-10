from time import *
import sys
import signal
from socket import *
from threading import Thread

r3Port = 29613
r2Port = 29612
r1Port = 29611
port = 29610
#start_time = time()
Ack = [0]*5556	#check ack to dcide whether the data is received
DataRec = [0]*5556

Ack2 = [0]*5556	#check ack to dcide whether the data is receiv
DataRec2 = [0]*5556

def sum(data):
    res=0
    for x in data:
        res+=ord(x)
    return res


def d_r3():
	#receive from s through r3
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('10.10.7.1',port)) #from r3 to d
    i = 0
	while True:
        i+=1
        msg, addr = server.recvfrom(2048
		#send ack to s through r3, message is received
		if msg=="":
            continue
		clientSocketAck = socket(AF_INET, SOCK_DGRAM)
		first = msg.find('^*_*^')
        second = msg.rfind('^*_*^')
    	data = msg[:first]
        check = int(msg[first+5:second])
        fake_i = int(msg[second+5:])
		if(sum(data)+check == -1) and Ack[fake_i]==0:
			DataRec[fake_i] = data
            Ack[fake_i] = 1
		if(sum(data)+check == -1) and Ack[fake_i]==1:
			clientSocketAck.sendto(str(fake_i),('10.10.7.2',r3Port))
		clientSocketAck.close()
        if i==5556:
            #end_time=time()
            #fin_time=end_time-start_time
            with open('output1.txt', 'w') as f:
                for data in DataRec:
                    f.write("%s" % data)
            break

def d_r1():
	#receive from s through r1
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('10.10.4.2',port)) #from r1 to d
    i = 0
	while True:
        msg, addr = server.recvfrom(2048)
		#send ack to s through r1, message is received
		if msg=="":
            continue
		clientSocketAck = socket(AF_INET, SOCK_DGRAM)
		first = msg.find('^*_*^')
        second = msg.rfind('^*_*^')
    	data = msg[:first]
        check = int(msg[first+5:second])
        fake_i = int(msg[second+5:])
		if(sum(data)+check == -1) and Ack2[fake_i]==0:
			DataRec2[fake_i] = data
            Ack2[fake_i] = 1
            i+=1
		if(sum(data)+check == -1) and Ack2[fake_i]==1:
			clientSocketAck.sendto(str(fake_i),('10.10.4.1',r1Port))
		clientSocketAck.close()
        if i==5556/2:
            break

def d_r2():
	#receive from s through r2
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('10.10.5.2',port)) #from r2 to d
    i = 0
	while True:
        msg, addr = server.recvfrom(2048)
		#send ack to s through r2, message is received
		if msg=="":
            continue
		clientSocketAck = socket(AF_INET, SOCK_DGRAM)
		first = msg.find('^*_*^')
        second = msg.rfind('^*_*^')
    	data = msg[:first]
        check = int(msg[first+5:second])
        fake_i = int(msg[second+5:])
		if(sum(data)+check == -1) and Ack2[fake_i]==0:
            i+=1
			DataRec2[fake_i] = data
            Ack2[fake_i] = 1
		if(sum(data)+check == -1) and Ack2[fake_i]==1:
			clientSocketAck.sendto(str(fake_i),('10.10.5.1',r2Port))
		clientSocketAck.close()
        if i==5556/2:
            break

senderd_r3 = Thread(target = d_r3,args=())
senderd_r1 = Thread(target = d_r1,args=())
senderd_r2 = Thread(target = d_r2,args=())

if sys.argv[1]=="1":
    senderd_r3.start()
    senderd_r3.join()

if sys.argv[1]=="2":
    senderd_r2.start()
    senderd_r1.start()
    senderd_r1.join()
    senderd_r2.join()
    with open('output2.txt', 'w') as f:
        for data in DataRec2:
            f.write("%s" % data)
        #end_time=time()
        #fin_time=end_time-start_time    
