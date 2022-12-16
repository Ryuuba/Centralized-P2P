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

#doesn't use provided port number...
def mountServer(port,directory):
    hostname='localhost' #this might change, need to check
    dir = abspath(directory)
    print(directory)
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=dir)
    httpd = http.server.HTTPServer((hostname, 0), Handler, False)
    print("server about to bind to port %d on hostname '%s'" % (port, hostname))
    httpd.server_bind()
    address="http://%s:%d" % (httpd.server_name, httpd.server_port)
    print("server about to listen on:", address)
    httpd.server_activate()
    httpd.serve_forever()

#mountServer(49999, '/run/media/cardcathouse/Main/Música/')