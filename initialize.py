#se debe mandar el puerto la ip el usuario y la contraseña
import login
import socket
import sys

#codigo del libro

puerto = 36887
direccionServidor = ('localhost', puerto)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print('Escuchando en ', sock.getsockname())
#inicio de sesion
login.InicioSesion(direccionServidor)




