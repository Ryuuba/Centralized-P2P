import sys
import naming
from socket   import *
import socket



def puertoDisponible(ip,port):
    disponible = False
    while disponible == False:
        try: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            disponible = True
        except:
                print("No se puede establecer coneccion...")
    
''' 
    ## Yo tengo una sugerencia
    puerto = 1
    while puerto <= 65535: ##Buscamos en cada puerto,disponible.
        try:
            try: 
                s = socket(AF_INET, SOCK_STREAM, 0)
            except:
                print("Socket error")
                break
            s.connect(host ,puerto)
            disponible = True
        except Exception: ##
            disponible = False
        finally:
            if disponible and puerto != s.getsockname() [1]:
                print('El puerto {} esta activo'.format(puerto)) ## MENSAJE DE CONFIRMACION.
            puerto +=1 ## INCREMENTAMOS
            s.close() ## CERRAMOS EL SOCKET.
    return 

'''

def setInfoUsuario():
    try:
        print("Nombre del usuario: ")
        naming.usuario.usuario = input()
        print("ingresa la contraseña: ")
        naming.usuario.password = input()
        ip = socket.gethostbyname(socket.gethostname())
        puerto
        
        puertoDisponible(ip, puerto)
        naming.usuario.direccion_ip = 
        naming.usuario.puerto = socket.

    except ValueError as ve:
        return str(ve)

def InicioSesion(socket: socket, ip: tuple, port):
    conectSucces = False
    while connectionAck == False:

        naming.main
        
        #concatenamos 

        loginSock = socket
        loginSock.connect(server_address)
        try:
            loginSock.sendall(bytes(loginInfoMsg, 'utf-8'))
            response = loginSock.recv(16)
        finally:
            if response.decode('utf-8') == 'ACK':
                connectionAck = True
            else:
                print('No se puedo iniciar sesión. Ingresa tus datos de nuevo')

flag