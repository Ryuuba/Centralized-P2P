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
