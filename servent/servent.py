import hashlib
import http.server
from sys import stderr
from functools import partial
from os.path import abspath
import functools
import requests
import os
from tabulate import tabulate
import cache_manager
import uuid
from random import randint
import time
import socket

# Inicializa la memoria cache
cache = cache_manager.start()

def login_msg(user:str, password:str)->str:
    # Login message
    port = '49999'
    implementation = 'Servent_Equipo2'
    msg_user = user + ' ' + password + ' ' + port + ' ' + implementation
    payload_lenght = "{:04d}".format(len(msg_user))
    msg_type = '0002'
    login_msg = 'printf "' + payload_lenght + msg_type + msg_user
    
    # Notification message
    #~ fetches files from the shared folder
    files = os.listdir('shared_content')
    #~ format of the name: distro#version#arch#target
    for file in files:
        file_split = file.split('#')
        #file_split.pop()
        distro = file_split[0]
        sha256 = hashlib.sha256(file.rstrip().encode()).hexdigest()
        size = os.stat('shared_content/'+file).st_size
        version = file_split[1]
        arch = file_split[2]
        target = file_split[3]
        anuncio = distro + " " + sha256 + " " + str(size) + " " + version + " " + arch + " " + target + " " + file
        anuncio_lenght = "{:04d}".format(len(anuncio))
        login_msg = login_msg + anuncio_lenght + '0064' + anuncio
            
    login_msg = login_msg + '" | ncat localhost 6699'
    
    return login_msg


def mountServer(directory):
    """
    Este módulo monta un servidor HTTP que envía los archivos contenidos en
    un directorio en específico. En el servant completo, este servidor se 
    estará ejecutando en un su propio hilo. 
    """

    hostname='localhost' #this might change, need to check
    dir = abspath(directory)
    #print("Montando servidor en directorio: ", directory)
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=dir)
    #Server will always use port 49999
    httpd = http.server.HTTPServer((hostname, 49999), Handler, False)
    httpd.server_bind()
    address="http://%s:%d" % (httpd.server_name, httpd.server_port)
    #print(httpd.server_address[0])
    #print("Servidor escuchando en :", address)
    httpd.server_activate()
    httpd.serve_forever()
    
    
    
def getFile(ipAddress, filename, port):
    argument = 'http://' + ipAddress + ':' + port + '/' + filename
    r = requests.get(argument, stream=True)
    route = 'shared_content\\'+ filename
    with open(route, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    print('Archivo guardado correctamente.\n')
    #cache_manager.print_cache()
    
    
def download_file():
    print("Inserta la dirección IP: ")
    ipAddress = input()
    print("Inserta el puerto")
    port = input()       
    print("Inserta el nombre del archivo")
    filename = input()
    #print("Obteniendo archivo...")
    getFile(ipAddress, filename, port)
    
    
def search(keyword:str) -> list[str]:
    # Create the search message
    msg_type = '00C8'
    payload_lenght = "{:04d}".format(len(keyword))
    search_msg = 'printf "' + payload_lenght + msg_type + keyword
    search_msg = search_msg + '" | ncat localhost 6699'
    
    #~ Execute the login line in terminal
    search_result = os.popen(search_msg).read()
    
    if len(search_result) >= 1:
        results = search_result.split("00c9")
        results = format_results(results)
        
        for i in range(len(results)):
            answer = {}
            answer["Filename"] = results[i][5]
            answer["IP"]= results[i][6]
            answer["Port"]= results[i][7]
            answer["Tiempo"]= randint(200,300)
            # Crea el identificador único de la respuesta (Se remplazara por la IP )
            identificador_respuesta = uuid.uuid4().hex[:8]
            # Guarda la respuesta en la memoria caché
            cache_manager.insert(identificador_respuesta, answer)
        
        #cache_manager.print_cache()
        return results
    else:
        return search_result
        
def format_results(search_results:str) -> list[str]:
    #~ Giving format to the result
    results = []
    for i in range(1, len(search_results)):
        results.append(search_results[i].split(" "))
        #~ delete the length of the payload of the results to show
        results[i-1].pop()
    
    return results  
              
    #~ Print the search results
    #print(tabulate(results, headers=["Distro", "Version", "Archiquecture", "Size", "Target", "Name", "IP", "Port"]))
     

def options_menu():
    salir = False
    while(salir != True):
        print("\nElige una operación\n1. Buscar una imagen\n2. Cerrar sesión")
        choice = input()
        if choice == "1":
            print("\nInserta el nombre de la distribución que quieres encontrar:")
            keyword = input()
            #~ Search a keyword
            resultados = search(keyword)
            if len(resultados) >= 1:
                #~ Print the search results
                print(tabulate(resultados, headers=["Distro", "Version", "Archiquecture", "Size", "Target", "Name", "IP", "Port"]))
                print("\n¿Quieres descargar alguna imagen? (s/n)" )
                if input() == 's':
                    download_file()
                    opcion = 's'
                    while opcion != 'n':
                        print("\n¿Quieres descargar otra imagen de esta busqueda? (s/n)" )
                        opcion = input()
                        if opcion == 's':
                            download_file()
            else:
                print("Lo siento, no se encontraron resultados para esa palabra clave\n")
            
            print("¿Quieres seguir usando el sistema? (s/n)" )
            if input() == 'n':
                print("Cerrando sesión y apagando el servidor HTTP...")
                #db.close_connection()
                salir = True

        elif choice == "2":
            print("Cerrando sesión y apagando el servidor HTTP...")
            #db.close_connection()
            salir = True
        elif choice == "":
            pass
        else:
            print("La opción introducida no es válida.")

    
def check_shared_folder(number:int, user:str, password:str):
    while True:
        files = os.listdir('shared_content')
        number_files = len(files)
        if number_files != number:
            number = number_files
            #~ Loging message
            msg = login_msg(user, password)
            #~ Execute the login line in terminal
            resultado_login = os.popen(msg).read()
            if resultado_login == '00190003napster@napster.com':
                print("Error al actualizar los archivos compartidos\n")
            else:
                print("Se actualizaron los archivos compartidos en el servidor, presiona enter...")
        else:
            time.sleep(5) # Sleep for 5 seconds
            
def check_connection(ip, port) -> bool:
    s = socket.socket()
    try:
        print(f"Connecting to {ip}:{port}")
        s.connect((ip, port))
    except socket.error as msg:
        #print(f"Failed to connect: {msg}")
        return False
    else:
        #print(f"Successfully connected to {ip}:{port}")
        return True
 