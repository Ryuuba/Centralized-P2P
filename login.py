import sys
import naming
from socket   import *
import socket



def setInfoUsuario(puertito):
    try:
        print("Nombre del usuario: ")
        naming.usuario.usuario = input()
        print("ingresa la contraseña: ")
        naming.usuario.password = input()
        naming.usuario.direccion_ip =  socket.gethostbyname(socket.gethostname())
        naming.usuario.puerto = puertito
        info = naming.usuario.usuario + naming.usuario.password + naming.usuario.direccion_ip + str(naming.usuario.puerto)
        #print("info es:" + info + "\n")
        return str(info)

    except ValueError as ve:
        return str(ve)

def InicioSesion(ip: tuple):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conectSucces = False

    while conectSucces == False:
        
        mensaje = setInfoUsuario(ip[1])
        mensaje_encoded = mensaje.encode(encoding = 'ascii')
        #no se puede pasar la ip, se le debe de pasar el socket
        sock.connect(ip)
        try:
            sock.sendall(mensaje_encoded)
            response = sock.recv(1024)
        finally:
            if response.decode('ascii') == 'ACK':
                conectSucces = True
            else:
                print('No se puedo iniciar sesión. Ingresa tus datos de nuevo')
