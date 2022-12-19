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

#An available pórt is assigned to the server automatically.
#Client and server should use different ports. 
def mountServer(directory):
    hostname='localhost' #this might change, need to check
    dir = abspath(directory)
    print(directory)
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=dir)
    httpd = http.server.HTTPServer((hostname, 0), Handler, False)
    httpd.server_bind()
    address="http://%s:%d" % (httpd.server_name, httpd.server_port)
    print("Servidor escuchando en :", address)
    httpd.server_activate()
    httpd.serve_forever()