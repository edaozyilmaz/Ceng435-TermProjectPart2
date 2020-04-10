import time
from time import sleep
import sys
import signal
from socket import *
from threading import Thread
#from netifaces import interfaces

window=50 #This is a indicator that indicates the end of the window
currentWindow=0 #This is a indicator that indicates the beginning of the window
i=0 #This is a variable for sending packets
flag1=0 #to check if senderR3 should stop

currentWindow2=0 #This is a indicator that indicates the beginning of the window
i2=0 #This is a variable for sending packets
flag2=0 #to check if senderR1 should stop
flag3=0 #to check if senderR2 should stop
i1=0 #This is a variable for sending packets

file=open('input.txt','r')
inp=file.read()

file=open('input2.txt','r')
inp2=file.read()

buffer=[] #Split file to buffer
buffer2=[] #Split file to buffer

serverSocketR3 = socket(AF_INET,SOCK_DGRAM)
serverSocketR3.bind(('10.10.3.1',29614))   #ip of r3 - port of s

serverSocketR1 = socket(AF_INET,SOCK_DGRAM)
serverSocketR1.bind(('10.10.1.1',29614))   #ip of r3 - port of s

serverSocketR2 = socket(AF_INET,SOCK_DGRAM)
serverSocketR2.bind(('10.10.2.2',29614))   #ip of r3 - port of s

#Divide file into packets then store in buffer array
while inp2:
	buffer2.append(inp2[0:900])
	inp2 = inp2[900:]

while inp:
	buffer.append(inp[0:900])
	inp = inp[900:]

DataSended= [0]*5556 #For selective repeat, this shows the successfuly sent packets
DataSended2= [0]*5556

def chksum(data):
	res=0
	for x in data:
		res+=ord(x)
	return ~res

# To send packets to r3
def senderR3():
	global i
	global currentWindow
	global flag1
	while True:
		if flag1==1:
			break
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		if(i-currentWindow)<51:
			if i<5556 and DataSended[i]==0: # send if not exceed window, array and not sended before
				message= buffer[i] + '^*_*^' + str(chksum(buffer[i])) +'^*_*^' + str(i)
				clientSocket.sendto(message,('10.10.3.2',29613))
			i+=1
		clientSocket.close()

# To send packets r1
def senderR1():
	global i1
	global currentWindow2
	global flag2
	while True:
		if flag2==1 or flag3==1:
			break
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		if(i1-currentWindow2)<51:
			if i1<5556 and DataSended2[i1]==0: # send if not exceed window, array and not sended before
				message= buffer2[i1] + '^*_*^' + str(chksum(buffer2[i1])) +'^*_*^' + str(i1)
				if(i1%2 == 1):
					clientSocket.sendto(message,('10.10.1.2',29611))	#if odd send to r1
			i1+=1
		clientSocket.close()

# To send packets r2
def senderR2():
	global i2
	global currentWindow2
	global flag3
	while True:
		if flag3==1 or flag2==1:
			break
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		if(i2-currentWindow2)<51:
			if i2<5556 and DataSended2[i2]==0: # send if not exceed window, array and not sended before
				message= buffer2[i2] + '^*_*^' + str(chksum(buffer2[i2])) +'^*_*^' + str(i2)
				if(i2%2 == 0):
					clientSocket.sendto(message,('10.10.2.1',29612))	#if even send to r2
			i2+=1
		clientSocket.close()


# For selective repeat and go back n
def nextWindow():
	global i
	global currentWindow
	while True:
		sleep(1.5)
		i=currentWindow
		window=i+50
		if 0 not in DataSended:
			break

# For selective repeat and go back n
def nextWindow2():
	global i2
	global i1
	global currentWindow2
	while True:
		sleep(1.5)
		i2=currentWindow2
		i1=currentWindow2
		window2=i2+50
		if 0 not in DataSended:
			break


#Function that count successfuly sent packet via receiving ACKs from d through r3
def ackReceiverR3():
	global currentWindow
	global flag1
	while True:
		message, addr = serverSocketR3.recvfrom(2048)
		if message=="": #if message is empty then continue
			continue
		first=DataSended.index(0) #find first not successfuly sent packet number
		index=int(message)
		DataSended[index]=1
		if 0 not in DataSended:
			flag1=1
			break
		second=DataSended.index(0) #find first not successfuly sent packet number after received one more ACK
		if index== first: #if last received ack goes into beginning of actual window then update cwnd locaton
			currentWindow=second


#Function that count successfuly sent packet via receiving ACKs from d through r1
def ackReceiverR1():
	global currentWindow2
	global flag2
	while True:
			message, addr = serverSocketR1.recvfrom(2048)
			if message=="": #if message is empty then continue
				continue
			first=DataSended2.index(0) or DataSended2.count(0)==1 #find first not successfuly sent packet number
			index=int(message)
			DataSended2[index]=1
			second=DataSended2.index(0) #find first not successfuly sent packet number after received one more ACK
			if index== first: #if last received ack goes into beginning of actual window then update cwnd locaton
				currentWindow2=second
			if 0 not in DataSended2 or DataSended2.count(0)==1:
				flag2=1
				break


#Function that count successfuly sent packet via receiving ACKs from d through r2
def ackReceiverR2():
	global currentWindow2
	global flag3
	while True:
			message, addr = serverSocketR2.recvfrom(2048)
			if message=="": #if message is empty then continue
				continue
			first=DataSended2.index(0) #find first not successfuly sent packet number
			index=int(message)
			DataSended2[index]=1
			second=DataSended2.index(0) #find first not successfuly sent packet number after received one more ACK
			if index== first: #if last received ack goes into beginning of actual window then update cwnd locaton
				currentWindow2=second
			if 0 not in DataSended2 or DataSended2.count(0)==1:
				flag3=1
				break

# If all packets sent successfuly then halt
def end():
	while True:
		if 0 not in DataSended:
			sys.exit(0)
			break


sender3 = Thread(target = senderR3,args=())
sender1 = Thread(target = senderR1,args=())
sender2 = Thread(target = senderR2,args=())
nextWindow = Thread(target = nextWindow,args=())
nextWindow2 = Thread(target= nextWindow2,args=())
ackReceiver3 = Thread(target = ackReceiverR3,args=())
ackReceiver1 = Thread(target = ackReceiverR1,args=())
ackReceiver2 = Thread(target = ackReceiverR2,args=())
end = Thread(target = end,args=())

if sys.argv[1]=="1":
	sender3.start()
	nextWindow.start()
	ackReceiver3.start()
	end.start()
	sender3.join()
	nextWindow.join()
	ackReceiver3.join()
	end.join()

if sys.argv[1]=="2":
	sender1.start()
	sender2.start()
	nextWindow2.start()
	ackReceiver1.start()
	ackReceiver2.start()
	end.start()
	sender1.join()
	sender2.join()
	nextWindow2.join()
	ackReceiver1.join()
	ackReceiver2.join()
	end.join()
