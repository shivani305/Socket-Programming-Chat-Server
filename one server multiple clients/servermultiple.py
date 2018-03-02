import socket
import sys
from tkinter import *
import _thread
def clientHandler(connection, client_address):
    print ('connected by',client_address)
    while True:
      data = connection.recv(1024)
      print ("received", repr(data))
      reply = input("Reply:")
      connection.sendall(reply.encode())
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host= socket.gethostname()
port=12345
s.bind(('10.250.95.97',port))
s.listen(10)
print("server is running")
while True:
      connection, client_address=s.accept()
      _thread.start_new_thread(clientHandler, (connection, client_address))
s.close()