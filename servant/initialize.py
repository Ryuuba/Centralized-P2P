#se debe mandar el puerto la ip el usuario y la contraseña

import socket
import sys
sys.path.append('./servant')
import login as login 
from dataclasses import dataclass, field
#from serviceAdv 
import serviceAdv as serviceAdv
from pubkeyreq import NapsterKeyManager
from create_keys import createKeys
import http_conect as http_conect
import getpass
import pandas as pd
import threading
import time

# from server import 

# from server.napster_db import DBNapsterConnector

sys.path.append('../server')
from napster_db import DBNapsterConnector

@dataclass
class P2PClient:
    direccionServidor: tuple
    miDirectorio: str
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Abrimos un socket
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print('Escuchando en ', sock.getsockname())
    def start_connection(self):
        #self.__listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect(self.direccionServidor)
        # max length of pending connections is automatically computed
        #self.__listener.listen(max)
        print(f'--------Socket creado:  {self.direccionServidor} --------')
        #print(f'Listen on {self.ip}, {self.port}')

    # pedir la llave publica al servidor
    def keyRequest(self):
        login.key_mensaje(self.sock)

    def sessionRequests(self):
        if login.InicioSesion(self.sock):
            #Hilo secundario
            serviceAdv.enviarArchivoServidor(self.sock,self.miDirectorio)
            t2 = threading.Thread(target=serviceAdv.compartirCarpeta, args=(self.sock, self.miDirectorio))
            t2.start()
            #Subimos la lista de los archivos a la base de datos
            
            

            
            #########serviceAdv.compartirCarpeta(self.sock, self.miDirectorio)
            #Compartimos la carpeta de los archivos
            #time.sleep(1)
            #time.sleep(1000/1000000.0)
            exito = False
            indice = False
            while(exito==False):
                print("\n===========================\n")
                print("\tDesplegando menu:")
                print("\tDescargar archivo(1)")
                print("\tSalir(2)")
                print("\n===========================\n")
                seleccion = int(input("Ingrese la opcion deseada:"))
                #serviceAdv(self.miDirectorio,self.sock)
                if seleccion == 1:

                    # llamar funcion busqueda
                    palabra = input("Ingrese el contenido a buscar: ")
 
                    if len(palabra) < 1:
                        print("ningun elemento de busqueda, vuelve a intentar")
                        #print("No se encontraron contenidos que coincidan con " + palabra)
                    else:
                        
                        # BUSQUEDA DE LA IMAGEN COMPARTIDA
                        busquedaPalabra = serviceAdv.buscarArchivoCompartido(self.sock, palabra)
                        listaAuxliar = []

                        for i in range(len(busquedaPalabra)):
                            textoUnido = busquedaPalabra[i]
                            textoSE = textoUnido[8:]
                            listaAuxliar.append(textoSE.split())

                        print(listaAuxliar)

                        print("\nLos archivos con la palabra " + palabra + " son: ")
                        print(pd.DataFrame(listaAuxliar, columns=['Distro', 'Version', 'Arch', 'Size', 'Target', 'Name', 'IP', 'Puerto']))
                        max = len(busquedaPalabra)
                        #print(max)
                        while(indice==False):
                            i = int(input("Que elemento deseas descargar?: "))
                            if i < max:
                                print("Hay algo que busc")
                                #print(palabra)
                                #print(listaAuxliar)
                                seleccion = listaAuxliar[i]   
                                #print(seleccion)                           
                                serviceAdv.descargarArchivo(self.miDirectorio,seleccion)
                                indice=True
                            else:
                                print("el indice indicado no es valido")
                elif seleccion == 2:
                    print("Saliendo...")
                    exito = True
                    DBNapsterConnector.close()

                else:
                    print("error la opcion " + seleccion + " no es la correcta")    

        # espere hasta que el subproceso 1 se ejecute por completo
        t2.join()


