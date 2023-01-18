"""
Este módulo monta un servidor HTTP que envía los archivos contenidos en
un directorio en específico. En el servant completo, este servidor se 
estará ejecutando en un su propio hilo. 
"""
from sys import stderr
from functools import partial
from os.path import abspath
import functools

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

#doesn't use provided port number...
def mountServer(port,directory):
    hostname='localhost' #this might change, need to check
    dir = abspath(directory)
    print(directory)
    Handler = functools.partial(SimpleHTTPRequestHandler, directory=dir)
    httpd = HTTPServer((hostname, 0), Handler, False)
    print("server about to bind to port %d on hostname '%s'" % (port, hostname))
    httpd.server_bind()
    address="http://%s:%d" % (httpd.server_name, httpd.server_port)
    print("server about to listen on:", address)
    httpd.server_activate()
    httpd.serve_forever()

mountServer(49999, '/home/alanbc/Documentos')







