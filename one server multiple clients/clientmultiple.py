import socket
import sys
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host= socket.gethostname()
port=12345
s.connect(('10.250.95.97',port))
i=1
while i is 1:
      message = input("your message:")
      s.send(message.encode())
      print("Awaiting reply")
      reply = s.recv(1024)
      print("Received",repr(reply))
s.close()