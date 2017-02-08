import random
import socket   
import sys  
import time
from Crypto.Cipher import AES
from Crypto import Random


numsensors = 0
validuser = 0
sensor_1 = '10.124.7.78'  
sensor_2 = '10.124.7.79'  



#KEY GENERATION
##########################################################################################################
def keygen():
	alpha = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")
	newiv = ''.join([random.choice(alpha) for _ in range(32)])
	return newiv

##########################################################################################################




#AUTHENTICATION
##########################################################################################################
while numsensors<2:
	#SENSOR 1 AUTHENTICATION - Port 50010
	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s1.bind(('10.124.7.69', 50010))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit() 

	#force the socket to listen for a remote connection
	s1.listen(1)
	print 'Socket is listening'

	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s1.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		 
		data = conn.recv(1024)
		
		if not data: 
			break 
		print('Received: ' +(data))
		user, passw = data.split('||')
		
		print user
		print passw
		
		user1 = str(user)
		passw1 = str(passw)
		
		print user1
		print passw1
		
		time.sleep(5)

		if user1 == 'test' and passw1 == 'test':
			numsensors=1
			validuser=1
			
			authmsg = 'Username and password correct. Access granted.'
			sauth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sauth.connect(('10.124.7.78', 50011))
			sauth.sendall(authmsg)
			sauth.close()
		else:
			numsensors = 1
			
			authmsg = 'Invalid username and/or password. Access denied.'
			sauth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sauth.connect(('10.124.7.78', 50011))
			sauth.sendall(authmsg)
			sauth.close()
		print "numsensors is .. " + str(numsensors)
		break
	conn.close()
	s1.close()
	
	
	
	
	
	#SENSOR 2 AUTHENTICATION - Port 50012
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s2.bind(('10.124.7.69', 50012))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit() 

	#force the socket to listen for a remote connection
	s2.listen(1)
	print 'Socket is listening'

	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s2.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		 
		data2 = conn.recv(1024)
		
		if not data2: 
			break 
		print('Received: ' +(data2))
		user2, passw2 = data2.split('||')
		
		print user2
		print passw2
		
		user22 = str(user2)
		passw22 = str(passw2)
		
		print user2
		print passw2
		
		time.sleep(5)

		if user2 == 'test' and passw2 == 'test':
			numsensors=2
			validuser=2
			
			authmsg = 'Username and password correct. Access granted.'
			sauth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sauth.connect(('10.124.7.79', 50013))
			sauth.sendall(authmsg)
			sauth.close()
		else:
			numsensors = 2
			
			authmsg = 'Invalid username and/or password. Access denied.'
			sauth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sauth.connect(('10.124.7.79', 50013))
			sauth.sendall(authmsg)
			sauth.close()
		print "numsensors is .. " + str(numsensors)
		break
	conn.close()
	s1.close()
	
	break	
##########################################################################################################





#ENCRYPTION
##########################################################################################################

#INITIAL SENSOR KEY
key = b'Sixteen byte key'
iv1 = 'a8a567890dfc14d2915af82adc065311'
iv=iv1.decode('hex')
cipher = AES.new(key, AES.MODE_CFB, iv)

#SENSOR 1 KEY GEN
key2 = b'Sixteen byte key'
iv1next1 = keygen() #call function to generate new key
iv1next = iv1next1.decode('hex')
cipher2 = AES.new(key2, AES.MODE_CFB, iv1next)

#SENSOR 2 KEY GEN	
key3 = b'Sixteen byte key'
iv31 = keygen() #call function to generate new random key
iv3 = iv31.decode('hex')
cipher3 = AES.new(key3, AES.MODE_CFB, iv3)

message = iv + cipher.encrypt('sensor: report @ time 1!||' + iv1next1)
ivmsg = iv1next + cipher2.encrypt('sensor 1: report @ time 2!')
iv3msg = iv3 + cipher3.encrypt('sensor 2: report @ time 2!')

print message
print ivmsg
print iv3msg
##########################################################################################################
	

	
	
	
#MESSAGE PASSING
##########################################################################################################

#if  user is validated
if validuser==2:
	time.sleep(5)
	#SENSOR 1 - Port 50014
	try:
		#create a socket with AF_INET (IPv4) and SOCK_STREAM (TCP based)
		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
		sys.exit();
	 
	print 'Socket Created'

	s1.connect((sensor_1, 50014))

	print 'Connected to ' + sensor_1

	try :
		#Set the whole string
		s1.sendall(message)
	except socket.error:
		#Send failed
		print 'Send failed'
		sys.exit()
	 
	print 'Message 1 sent successfully'
	
	time.sleep(5)


	try :
		#Set the whole string
		s1.sendall(ivmsg)
	except socket.error:
		#Send failed
		print 'Send failed'
		sys.exit()
	 
	print 'Message 2 sent successfully'
	# while True:
		# data = s.recv(1024)
		# print("Recieved: "+(data))
		# response = raw_input("Reply: ")
		# if response == "exit":
			# break
		# s.sendall(response)
		

	s1.close()
	
	
	
	#SENSOR 2 - Port 50015
	try:
		#create a socket with AF_INET (IPv4) and SOCK_STREAM (TCP based)
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
		sys.exit();
	 
	print 'Socket Created'

	s2.connect((sensor_2, 50015))

	print 'Connected to ' + sensor_2

	try :
		#Set the whole string
		s2.sendall(message)
	except socket.error:
		#Send failed
		print 'Send failed'
		sys.exit()
	 
	print 'Message 1 sent successfully'

                    ###wait for temperature
	
	time.sleep(5)


	try :
		#Set the whole string
		s2.sendall(iv3msg)
	except socket.error:
		#Send failed
		print 'Send failed'
		sys.exit()
	 
	print 'Message 2 sent successfully'
	# while True:
		# data = s.recv(1024)
		# print("Recieved: "+(data))
		# response = raw_input("Reply: ")
		# if response == "exit":
			# break
		# s.sendall(response)
		

	s2.close()
	
	
	
	#SENSOR 1 - Port 50016
	sard = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sard.bind(('10.124.7.69', 50016))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit() 

	#force the socket to listen for a remote connection
	sard.listen(1)
	
	print 'Socket is listening'
	
	while 1:
		#wait to accept a connection - blocking call
		connard, addrard = sard.accept()
		print 'Connected with ' + addrard[0] + ':' + str(addrard[1])
		 
		dataard = connard.recv(1024)
		
		if not dataard: 
			break 
		print('Sensor 1 @ time 1: ' +(dataard)+ ' degrees C')
		
		
		break
	connard.close()
	sard.close()

	#SENSOR 2 - Port 50017
	sard2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sard2.bind(('10.124.7.69', 50017))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit() 

	#force the socket to listen for a remote connection
	sard2.listen(1)
	
	print 'Socket is listening'
	
	while 1:
		#wait to accept a connection - blocking call
		connard2, addrard2 = sard2.accept()
		print 'Connected with ' + addrard2[0] + ':' + str(addrard2[1])
		 
		dataard2 = connard2.recv(1024)
		
		if not dataard2: 
			break 
		print('Sensor 2 @ time 1: ' +(dataard2)+ ' degrees C')
		
		
		break
	connard2.close()
	sard2.close()
	
	
	###################################### 2nd Round of Temps

	#SENSOR 1 - Port 50018
	sard3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sard3.bind(('10.124.7.69', 50018))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit() 

	#force the socket to listen for a remote connection
	sard3.listen(1)
	
	print 'Socket is listening'
	
	while 1:
		#wait to accept a connection - blocking call
		connard3, addrard3 = sard3.accept()
		print 'Connected with ' + addrard3[0] + ':' + str(addrard3[1])
		 
		dataard3 = connard3.recv(1024)
		
		if not dataard3: 
			break 
		print('Sensor 1 @ time 2: ' +(dataard3)+ ' degrees C')
		
		
		break
	connard3.close()
	sard3.close()

	#SENSOR 2 - Port 50019
	sard4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sard4.bind(('10.124.7.69', 50019))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit() 

	#force the socket to listen for a remote connection
	sard4.listen(1)
	
	print 'Socket is listening'
	
	while 1:
		#wait to accept a connection - blocking call
		connard4, addrard4 = sard4.accept()
		print 'Connected with ' + addrard4[0] + ':' + str(addrard4[1])
		 
		dataard4 = connard4.recv(1024)
		
		if not dataard4: 
			break 
		print('Sensor 2 @ time 2: ' +(dataard4)+ ' degrees C')
		
		
		break
	connard4.close()
	sard4.close()
	######################################
	
	# try:
		# #create a socket with AF_INET (IPv4) and SOCK_STREAM (TCP based)
		# s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# except socket.error, msg:
		# print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
		# sys.exit();
	 
	# print 'Socket Created'

	# sensor_2 = '10.124.7.79'                 
	# port = 50008

	# s2.connect((sensor_2, port))

	# print 'Connected to ' + sensor_2

	# #message = "yo"

	# try :
		# #Set the whole string
		# s2.sendall(message2)
	# except socket.error:
		# #Send failed
		# print 'Send failed'
		# sys.exit()
	 
	# print 'Message sent successfully'

	# # while True:
		# # data = s.recv(1024)
		# # print("Recieved: "+(data))
		# # response = raw_input("Reply: ")
		# # if response == "exit":
			# # break
		# # s.sendall(response)
	# s.close()
	######################################

