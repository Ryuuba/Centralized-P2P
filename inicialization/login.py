import sys
import naming
from socket   import *
import socket
import os
import getpass

def setInfoUsuario(puertito):
    try:
        print("Nombre del usuario: ")
        naming.usuario.usuario = input()
        print("ingresa la contraseña: ")
        naming.usuario.password = input()
        naming.usuario.direccion_ip =  socket.gethostbyname(socket.gethostname())
        naming.usuario.puerto = puertito
        info = naming.usuario.usuario + naming.usuario.password + naming.usuario.direccion_ip + str(naming.usuario.puerto)
        
        return str(info)

    except ValueError as ve:
        return str(ve)

def InfoUsuario_base(puertito):
    try:
        print("Nombre del usuario: ")
        naming.usuario.usuario = input()
        print("ingresa la contraseña: ")
        naming.usuario.password = input()
        naming.usuario.direccion_ip =  socket.gethostbyname(socket.gethostname())
        naming.usuario.puerto = puertito
        info = naming.usuario.usuario + " " + naming.usuario.password + " " + "20041" + " " + getpass.getuser()       
        return str(info)

    except ValueError as ve:
        return str(ve)

def InicioSesion(ip: tuple):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conectSucces = False

    while conectSucces == False:
        
        info = InfoUsuario_base(ip[1])
        print("mensaje es:" + info + "\n")
        t = len(info)
        mensaje = '00' + str(t) +"0002"+ info
        print(mensaje)
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

def key_mensaje(ip: tuple):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mensaje = "00000010"

    mensaje_encoded = mensaje.encode(encoding = 'ascii')
    #no se puede pasar la ip, se le debe de pasar el socket
    sock.connect(ip)
    try:
        sock.sendall(mensaje_encoded)
        response = sock.recv(1024)
    finally:
            key = response.decode('ascii')
            if os.path.isfile('./key/public_napster.pem'):
                print("Ya se tiene la llave publica")
            else:
                f = open('./key/public_napster.pem','w')
                pub_key = key.split(sep="\n")
                f.write("-----BEGIN RSA PUBLIC KEY-----\n")
                f.write(pub_key[1]+"\n")
                f.write(pub_key[2]+"\n")
                f.write(pub_key[3])
                f.write("\n-----END RSA PUBLIC KEY-----\n")
                f.close()