import socket

def clientHandler(connection, client_address):
    print ('connected by',client_address)
    while True :
        data = (connection.recv(1024)).decode()
        print ("received", repr(data))
        reply = input("Reply:")
        connection.sendall(reply.encode())
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host= socket.gethostname()
port=12347
s.bind(('10.250.14.157',port))
s.listen(10)
print("server is running")
while True:
    connection, client_address=s.accept()
    clientHandler(connection, client_address)
s.close()