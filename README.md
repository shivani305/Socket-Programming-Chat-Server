# Socket-Programming-Chat-server
Establishing communication between Clients and Server using Sockets

This is basic chat application, but it is important to know how it actually worked.
The Server will be running in the background, and when ever the client connects to the Server Ip address and port.

Sockets are created at the server end and also at the client end. Communication channel will be established with these sockets.

When another client2 connects to the same server, a parallel communication channel is created between server socket and client2 socket.
