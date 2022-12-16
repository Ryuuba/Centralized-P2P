#se debe mandar el puerto la ip el usuario y la contraseña

import socket
import sys

#codigo del libro
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((interface, port))
sock.listen(1)

print('Listening at', sock.getsockname())
sc, sockname = sock.accept()
print('We have accepted a connection from', sockname)



print(' Socket name:', sc.getsockname())
print(' Socket peer:', sc.getpeername())
message = recvall(sc, 16)
print(' Incoming sixteen-octet message:', repr(message))
sc.sendall(b'Farewell, client')
sc.close()
print(' Reply sent, socket closed')