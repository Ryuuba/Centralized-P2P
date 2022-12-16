#se debe almacenar en un diccionario las respuestas que se han solicitado

import socket
import sys

from dataclasses import dataclass
@dataclass

class cache_usuario:
    puerto: int #ejemplo de pueto: 1356
    direccion_ip: str #ejemplo de direccion 192.168.30.25
    usuario: str #ejemplo de usuario: gatitabellaka 
    password: str #pasword

    
    def __init__(self, puerto, direccion_ip, usuario, password):  # (self, puerto, self.direccion_ip}, {self.usuario}, {self.password):
        self.puerto = puerto
        self.direccion_ip =  direccion_ip
        self.usuario = usuario
        self.password = password

    def __str__(self) -> str:
        return f'{self.puerto}: {self.direccion_ip}, {self.usuario}, {self.password}'


    # def setData(self):
    #     print("Nombre del usuario: ")
    #     self.usuario = input()
    #     print("ingresa la contraseña: ")
    #     self.password = input()
    #     ip_address = socket.gethostbyname(socket.gethostname())
    #     mensaje = self.usuario + self.password
    #     # 
    #     # 
    #     #
    #     #     




def main():
    try:
        print("Nombre del usuario: ")
        usuario = input()
        print("ingresa la contraseña: ")
        contra = input()

        cache = cache_usuario(3512,'192.168.30.2',usuario,contra)
        print(cache)
    except ValueError as ve:
        return str(ve)
    


if __name__=='__main__': #if __name__=='__main__' LE PEGUÉ ESTA MAMADA HDTPM :)
    sys.exit(main())