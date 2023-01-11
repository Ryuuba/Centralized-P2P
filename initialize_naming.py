import pwinput
import socket
import sys

"""
Este módulo se encarga de pedir al usuario su usuario y contraseña.
El módulo obtiene la dirección IP y el número de socket del servidor 
HTTP del servent. Esta información se junta en un sólo mensaje que se pasa
como una cadena de texto al módulo initialize_login. Este último invoca a este módulo
para obtener el mensaje. Puede que sea necesario ejecutar pip install pwinput para
instalar el módulo pwinput localmente.

Formato del mensaje de inicio de sesión:

[LP][CM][nick][password][PuertoHTTP][VersionCliente]

LP = Longitud de la carga útil (4 bytes)
CM = código del mensaje (4 bytes hexadecimales escritos en ASCII)
nick = nombre de usuario
password = contraseña
PuertoHTTP = número de puerto por el cual el servidor HTTP escucha peticiones

Ejemplo: 00260002alex alex0000 20041 netcat
"""
def getUserInfo(port_number):
    print("Inserta tu nombre de usuario:")
    function = '0002'
    nick = input();
    password = pwinput.pwinput(prompt='Inserta tu contraseña: ')
    client_info = "Servent_Equipo2"
    port = str(port_number)
    login_msg = " ".join([nick,password,port,client_info])
    #Obtaining payload size in bytes
    length = len(login_msg)
    #Header + payload 
    final_login_msg = '00' + str(length) + function + login_msg
    print(final_login_msg)
    return(final_login_msg.rstrip())