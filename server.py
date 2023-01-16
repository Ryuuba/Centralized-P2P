"""
Este módulo monta un servidor HTTP que envía los archivos contenidos en
un directorio en específico. En el servant completo, este servidor se 
estará ejecutando en un su propio hilo. 
"""

import http.server
from sys import stderr
from functools import partial
from os.path import abspath
import functools


def mountServer(directory):
    hostname='172.30.5.33' #this might change, need to check
    dir = abspath(directory)
    print("Montando servidor en directorio: ", directory)
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=dir)
    #Server will always use port 49999
    httpd = http.server.HTTPServer((hostname, 49999), Handler, False)
    httpd.server_bind()
    address="http://%s:%d" % (httpd.server_name, httpd.server_port)
    print(httpd.server_address[0])
    print("Servidor escuchando en :", address)
    httpd.server_activate()
    httpd.serve_forever()
