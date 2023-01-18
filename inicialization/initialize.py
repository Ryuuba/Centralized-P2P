#se debe mandar el puerto la ip el usuario y la contraseña
import login 
import socket
import sys
from pubkeyreq import NapsterKeyManager
from create_keys import createKeys

print(" ======= INICIO DE SERVANT =======")
#codigo del libro

puerto = "6699"
direccionServidor = ('localhost', int(puerto))
print('Iniciando en {} port {}'.format(*direccionServidor))
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print('Escuchando en ', sock.getsockname())
#inicio de sesion
#establecer el envio de la lleva publica si ya existe envia los datos para inicio de sesion 
# si no existe lo envia antes de iniciar sesion

# pedir llave publica 
login.key_mensaje(direccionServidor)

#Crear la llave publica
#crearKeys = createKeys()
#crearKeys.generarKey()
#Devuelve la llave publica
#manager = NapsterKeyManager()
#print(manager)

login.InicioSesion(direccionServidor)


