import getpass
import serial
import socket
import sys
import time
from Crypto.Cipher import AES
from Crypto import Random

#REGISTRATION WITH MASTER
######################################
print "Step 1. Registration ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
uname = raw_input('uname:')
passw = getpass.getpass('pass:')

#print uname
#print passw

message22 = uname + '||'+ passw
#print message22
print " "
print " "
print " "

stest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stest.connect(('10.124.7.69', 50010))
stest.sendall(message22)

######################################

#WAIT FOR AUTHENTICATION
######################################
print "Step 2. Authentication ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
sauth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sauth.bind(('10.124.7.78', 50011))
sauth.listen(1)
print 'Socket is listening'

while 1:
    conn, addr = sauth.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    data1 = conn.recv(1024)
    
    if not data1: 
        break 
    print('Received: ' +(data1))
    break
conn.close()
sauth.close()
print " "
print " "
print " "

######################################

#MESSAGE PASSING
######################################
print "Step 3. Receiving Messages ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
sensor_1 = '10.124.7.78'                 
port = 50014              

#create a socket with AF_INET (IPv4) and SOCK_STREAM (TCP based)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print 'Socket was created'


#bind the socket to the sensor_1 ip on the specified port number
try:
    s.bind((sensor_1, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit() 
#print 'Socket bind complete'


#force the socket to listen for up to 1 incoming remote connection
s.listen(1)
print 'Socket is listening'


#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    data = conn.recv(1024)
    
    #DECRYPTION
    ######################################

    key = b'Sixteen byte key'
    iv1 = 'a8a567890dfc14d2915af82adc065311'
    iv=iv1.decode('hex')
    cipher = AES.new(key,AES.MODE_CFB, iv)

    secretmsg = cipher.decrypt(data)
    secretmsg1 = secretmsg[16:]
    
	
	######################################
	
    message1, iv2 = secretmsg1.split('||')
	
    if not data: 
        break 
    print('Received: ' +(message1))
	
	#PASS TO ARDUINO
    ######################################
    if message1 == "sensor: report @ time 1!":
        ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port

    while True:
        temp1 = ser.readline()
        time.sleep(2)
        temp2 = ser.readline()
        #print temp1
        temp3 = int(temp2) * (-1)
        #print temp2
        temp_ac = temp3 + 530 #tare to 25 degrees C (room temp)
        print temp_ac
        break
    print " "
    print " "
    print " "

    print "Step 4. Group Key Reception ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	

    data2 = conn.recv(1024)

    #DECRYPTION2
    ######################################

    key2 = b'Sixteen byte key'
    iv22=iv2.decode('hex')
    cipher2 = AES.new(key2,AES.MODE_CFB, iv22)

    secretmsg2 = cipher2.decrypt(data2)
    secretmsg21 = secretmsg2[16:]
    
	
    ######################################
    time.sleep(3)
	
    print "New group key generated ..."
    
    time.sleep(3)
    print " "
    print " "
    print " "

	
    print "Step 5. Receiving Messages (c'td) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    if not data2: 
        break 
    print('Received: ' +(secretmsg21))
 
    #response = raw_input("Reply: ")
    #if response == "exit":
    #    break
    #conn.sendall(response)
	
	#PASS TO ARDUINO
    ######################################
    if secretmsg21 == "sensor 1: report @ time 2!":
        ser2 = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port

    while True:
        temp4 = ser2.readline()
        time.sleep(2)
        #print temp4
        temp5 = ser2.readline()
        #print temp5
        temp6 = int(temp5) * (-1)
        #print temp6
        temp_ac2 = temp6 + 530 #tare to 25 degrees C (room temp)
        print temp_ac2
        break
    print " "
    print " "
    print " "
	
    break
conn.close()
s.close()

time.sleep(3)
print " "
print " "
print " "

print "Step 6. Group Key Reception ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	
print "New group key generated ..."
    
time.sleep(3)

print " "
print " "
print " "

print "Step 7. Demo Completed ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "Steps 4 and 5 repeat n times..."

sard = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sard.connect(('10.124.7.69', 50016))
sard.sendall(str(temp_ac))

time.sleep(15)
sard2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sard2.connect(('10.124.7.69', 50018))
sard2.sendall(str(temp_ac2))
