import os
import socket
import getpass
import time
import hashlib
from dataclasses import dataclass, field
import requests
import urllib.request
import hashlib
import http.server
import functools
from sys import stderr
from functools import partial
from os.path import abspath
from tabulate import tabulate
import pandas as pd
import socketserver
# to display a Web-based documents to users
import webbrowser
import shutil

def listaArchivos(path:str) -> list[str]:
        lista = []
        contenido = os.listdir(path)
        print("Entro a la lista de archivos")
        for fichero in contenido:
          if os.path.isfile(os.path.join(path, fichero)) and fichero.endswith('.iso'):
            lista.append(fichero)
            print(fichero)

        print("La lista es: "+str(lista))
        return lista

def buscarArchivoCompartido(sock: socket.socket, palabraClave: str)->list[str]:
        listaAuxliar = []
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # print("El mensaje codificado es: "+str(mensaje_encoded))
        #no se puede pasar la ip, se le debe de pasar el socket
        #sock.connect(ip)
        #print("\tLa IP es: "+str(ip))
        
        #enviarle el mensaje al servidor
        try: 
            lenght = "{:04d}".format(len(palabraClave))
            #Estructura del mensaje
            mensaje = str(lenght) + "00C8" + palabraClave
            #print("La estructura del mensaje es: "+mensaje)
            #encode(): El método devuelve una versión codificada de la cadena dada.
            mensaje_encoded = mensaje.encode(encoding = 'ascii')
            sock.sendall(mensaje_encoded)
            response = sock.recv(1024)
            resp_wk = response.decode('ascii')
            print(resp_wk)
            num = int(resp_wk[8])
            if num > 0:
                #
                    #print(i)
                partial_msg = sock.recv(2048)
                msg = partial_msg.decode('ascii')
                msg = msg.split()
                print(msg)
                i=0
                j=0
                auxiliar = ""
                for part in msg:
                    auxiliar += part + " "
                    i+=1
                    if i == 8:
                        listaAuxliar.insert(j,auxiliar)
                        auxiliar=""
                        j+=1
                        i=0
                return listaAuxliar
            else:
                #print("No se hizo la busqueda")
                print("\nLa palabra "+str(palabraClave)+ " no se encontro ")
                #return False
        finally:
            print("---------busqueda terminada-----------")
            # tabla = tabulate(palabra, headers=["Distribucion", "Version", "Arch", "Size", "Target", "Name"])
            # print(tabla)

def enviarArchivoServidor(sock: socket.socket, directorio: str):
        print("Enviando Archivos")
        
        #Pasamos el contenido de lista distribuciones a la carpeta distribuciones
        
        listaDistribuciones = listaArchivos(directorio)

        # Pasar lo de la lista a un archivo txt
        with open('distribuciones.txt', 'w') as temp_file:
            for item in listaDistribuciones:
                temp_file.write("%s\n" % item)
        
        # Leer el txt y pasar la estructura del mensaje
        with open('distribuciones.txt', 'rb') as file:
            for line in file:
                #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #sock.connect(self.ip)
                archivo = line.split()
                distro = archivo[0].decode()
                sha256 = hashlib.sha256(line.rstrip()).hexdigest()
                print("El sha256 es: "+sha256)
                size = archivo[1].decode()
                version = archivo[2].decode()
                arch = archivo[3].decode()
                target = archivo[4].decode()
                file_name = archivo[5].decode()
                mensaje = distro + " " + sha256 + " " + size + " " + \
                    version + " " + arch + " " + target + " " + file_name
                print("La info de la iso es: " + mensaje)
                mensaje_lenght = "{:04d}".format(len(mensaje))
                mensaje_insertar = mensaje_lenght + '0064' + mensaje
                print("Esto se envia al server: " + mensaje_insertar)
                mensaje_encoded = mensaje_insertar.encode(encoding = 'ascii')
                try: 
                    sock.sendall(mensaje_encoded)
                    print("------------------Notificacion enviada al server------------------")
                    response = sock.recv(1024)
                finally:
                    print("-----------------Respuesta del server------------------")
                    resp = response.decode('ascii')
                    print(resp)
                    #return mensaje_insertar
            
            #file.close()
    
def descargarArchivo(user_path: str,raiz: list[str]):
        # crear el http request
        # Las funciones parciales nos permiten fijar un cierto número de
        # argumentos de una función y generar una nueva función.
        #Handler = functools.partial(http.server.SimpleHTTPRequestHandler, user_path)
        #print("Handler: "+ str(Handler))

        #elemento = raiz.split()
        nombre_cont = ""
        ip_cont = raiz[6]
        port_cont = raiz[7]
        cont = 0
        #print(ip_cont)
        #print(port_cont)
        for i in raiz:
            #print("\tCICLO: " + str(cont) + " \n")
            if cont <= 5:
                nombre_cont += " " + i
            cont += 1
        nombre_cont = nombre_cont[1:]

        #Pedir datos para enviarlo
        print("Direccion IP del archivo proveniente: ")
        print(ip_cont)
        print("Puerto de origen del archivo: ")
        print(port_cont)
        print("Nombre del archivo: ")
        print(nombre_cont)
        print(user_path)
        #print()
        

        complet_path ='http://' +ip_cont + ':' + port_cont + user_path + '/' + nombre_cont
        print("el path completo es: ")
        print(complet_path)
        #direccionHTTP  = abspath(complet_path)

        response = requests.get(complet_path,stream=True)
        with open(nombre_cont,'wb') as out_file :
            shutil.copyfileobj(response.raw,out_file)
        del response

def compartirCarpeta(sock: socket.socket,directorio:str):
    # assigning the appropriate port value
    PORT = 20041
    #20041
    # this finds the name of the computer user
    #os.environ['HOME']

    IP = socket.gethostbyname(socket.gethostname())
    # changing the directory to access the files desktop
    # with the help of os module
    direccion = abspath(directorio)
    #print(directorio)
    #                    '/home/uriel/Documentos/Distribuciones')
    #os.chdir(desktop)

    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=direccion)
    # creating a http request
    # returns, host name of the system under
    # which Python interpreter is executed
    httpd = http.server.HTTPServer((IP,PORT), Handler, False)
    httpd.server_bind()
    address="http://%s:%d" % (httpd.server_name, httpd.server_port)
    print(httpd)

    httpd.server_activate()
    webbrowser.open(address)
    httpd.serve_forever()