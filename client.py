"""
Este modulo actúa como la parte del cliente del servent.
Su única tarea (por ahora) es obtener las imágenes de Linux desde un peer
por medio de peticiones HTTP. Se le proporciona como argumentos la dirección IP y
puerto del peer, así como el nombre del archivo a descargar. El archivo es recibido
como un flujo de datos binario, el cuál se escribe en un archivo con el mismo
nombre y extensión proporcionado en el argumento.
"""

import requests
#import initialize_cache_manager as cache_manager
import buscar


def getFile(ipAddress, filename, port):
    print('Guardando...')
    argument = 'http://' + ipAddress + ':' + port + '/' + filename
    r = requests.get(argument, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    print('Archivo guardado correctamente.')
    
    # Guarda el resultado de la petición
    peticion ={}
    cache, respuesta = buscar.search(cache, peticion)
    

# Inicializa la memoria cache
#cache = cache_manager.start()

print("Inserta la dirección IP: ")
ipAddress = input()
print("Inserta el puerto")
port = input()
while(True):
    print("Inserta el nombre del archivo")
    filename = input()
    print("Obteniendo archivo...")
    getFile(ipAddress, filename, port)
    print("Archivo obtenido.")
    #cache_manager.print_cache()

#cache = cache_manager.content()    
