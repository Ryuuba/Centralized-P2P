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
        #no se puede pasar la ip, se le debe de pasar el socket
        sock.connect(ip)
        try:
            socket.sendall(bytes(mensaje, 'utf-8'))
            response = sock.recv(16)
        finally:
            if response.decode('utf-8') == 'ACK':
                conectSucces = True
            else:
                print('No se puedo iniciar sesión. Ingresa tus datos de nuevo')
