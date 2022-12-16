import initialize_login
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = "49999"
server_address = ('localhost', int(port))
initialize_login.loginToSystem(sock, server_address,port)
print("Bienvenido al sistema de distribución de imagenes de Linux")
#One thread should be executing initialize_cacheman
#After successful login, should execute initialize_servicead
