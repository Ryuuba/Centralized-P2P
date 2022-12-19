import pwinput
import socket
import sys

"""
Este módulo se encarga de pedir al usuario su usuario y contraseña.
El módulo obtiene la dirección IP y el número de socket del equipo que está
ejecutando el servant. Esta información se junta en un sólo mensaje que se pasa
como una cadena de texto al módulo initialize_login. Este último invoca a este módulo
para obtener el mensaje. Puede que sea necesario ejecutar pip install pwinput para
instalar el módulo pwinput localmente.
"""
#El puerto debe ser enviado como String...por ahora
def getUserInfo(port_number):
    print("Inserta tu nombre de usuario:")
    function = '0002'
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