import sys
sys.path.append('./servant')
import naming as naming
from socket   import *
import socket
import os
import getpass

def key_mensaje(sock:socket.socket):
    mensaje = "00000010"
    mensaje_encoded = mensaje.encode(encoding = 'ascii')
    #no se puede pasar la ip, se le debe de pasar el socket
    #sock.connect()
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

def InfoUsuario_base(sock:socket.socket):
    try:
        print("Nombre del usuario: ")
        naming.usuario.usuario = input()
        print("ingresa la contraseña: ")
        naming.usuario.password = input()
        naming.usuario.direccion_ip =  sock.getsockname()[0]
        naming.usuario.puerto = sock.getsockname()[1]
        info = naming.usuario.usuario + " " + naming.usuario.password + " " + "20041" + " " + getpass.getuser()       
        return str(info)
    except ValueError as ve:
        return str(ve)

def InicioSesion(sock: socket.socket)-> bool:
    #esto tiene el mismo puerto del servidor para enviarselo
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conectSucces = False
    while conectSucces == False:
        #Pide los datos del usuario
        info = InfoUsuario_base(sock)
        print("mensaje es:" + info + "\n")
        t = len(info)
        print("len: "+str(t))
        #Estructura del mensaje
        mensaje = '00' + str(t) +"0002"+ info
        #print("La estructura del mensaje es: "+mensaje)
        #encode(): El método devuelve una versión codificada de la cadena dada.
        mensaje_encoded = mensaje.encode(encoding = 'ascii')
        print("El mensaje codificado es: "+str(mensaje_encoded))
        #no se puede pasar la ip, se le debe de pasar el socket
        #sock.connect(ip)
        #Si no puede haber una conexion con el socket se intenta de nuevo con try
        try:
            #debemos de enviar el mensaje codificado al socket
            sock.sendall(mensaje_encoded)
            response = sock.recv(1024)
            #Entraria si la pos 7 es un 3 ya que la solicitud tiene un 
            
        finally:
            resp = response.decode('ascii')
            print("resp: "+resp)
            if resp[7] == "3":
                print("Inicio de sesion valido")
                print(resp[8:]) #devuelve la 
                conectSucces = True
                return True
            else:
                print(resp)
                print('No se puedo iniciar sesión. Ingresa tus datos de nuevo')

