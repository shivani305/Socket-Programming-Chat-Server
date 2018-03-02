import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port=12347
s.connect(('10.250.14.157',port))
while True :
	message = input("your message:")
	s.send(message.encode())
	print("Awaiting reply")
	reply = s.recv(1024)
	print("Received",repr(reply))
s.close()