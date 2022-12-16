#se debe almacenar en un diccionario las respuestas que se han solicitado

import socket
import sys

from dataclasses import dataclass

#reglas de inicializacion 
@dataclass
class usuario:
    puerto: int #ejemplo de pueto: 1356
    direccion_ip: str #ejemplo de direccion 192.168.30.25
    usuario: str #ejemplo de usuario: gatitabellaka 
    password: str #password

if __name__=='__main__': 
    sys.exit()

#no andes de tenton que no es pito HDTPM c:

#aqui HDTPM

'''
def getUserInfo(port_number):
    print("Inserta tu nombre de usuario:")
    function = '0x02'
    nick = input();
    password = pwinput.pwinput(prompt='Inserta tu contraseña: ')
    client_info = "Servant_Equipo2"
    ip_address = socket.gethostbyname(socket.gethostname())
    port = port_number
    login_msg = " ".join([nick,password,client_info,ip_address,port])
    #Obtaining payload size in bytes
    length = sys.getsizeof(login_msg)
    #Header + payload 
    login_msg = " ".join([function,str(length),nick,password,client_info,ip_address,port])
    return(login_msg)

'''