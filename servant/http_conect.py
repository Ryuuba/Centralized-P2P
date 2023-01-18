#Tener un código que nos permita hacer transferencias http 

# for implementing the HTTP Web servers
import http.server
import functools
import getpass
import urllib.request

# provides access to the BSD socket interface
import socket

# a framework for network servers
import socketserver

import requests
import os

def show_content():
    PORT = 16200
    hostname = 'localhost'
    user_path = "/home/" + getpass.getuser() + "/Documentos"

    # cambiar el directorio para acceder al escritorio de archivos
    # con la ayuda del módulo os
    desktop = os.path.join(os.path.join(os.environ['HOME']),
                        user_path)
    print("Mi desktop: "+desktop) 
    os.chdir(desktop)

    # crear el http request
    #Las funciones parciales nos permiten fijar un cierto número de 
    # argumentos de una función y generar una nueva función.
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, desktop)
    print("Handler: "+str(Handler))


    httpd = http.server.HTTPServer((hostname,PORT),Handler,False)
    httpd.server_bind()
    #print(httpd)

    print("-----------------")
    contents = urllib.request.urlopen("http://" + hostname + ":" + str(PORT) + user_path).read()
    print(contents)

    httpd.server_activate()
    httpd.serve_forever()
    