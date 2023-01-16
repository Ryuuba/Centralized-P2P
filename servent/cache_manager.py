from threading import Thread
import time
import servent
from random import randint

# Se inicializa la memoria caché como una colección
cache_manager = {}

# Función que revisa el tiempo de vida de una respuesta
def revisa_tiempo():
    """ Esta función revisa si una respuesta ya caduco"""
    for respuesta in list(cache_manager):
        if cache_manager[respuesta]["Tiempo"] >= 1:
            cache_manager[respuesta]["Tiempo"] -= 1
        elif cache_manager[respuesta]["Tiempo"] == 0:
            # Revisa si el servent que tiene el archivo aun esta conectado
            connection = servent.check_connection(cache_manager[respuesta]["IP"],int(cache_manager[respuesta]["Port"]))
            if connection == False:
                del(cache_manager[respuesta])
            else:
                cache_manager[respuesta]["Tiempo"] = randint(200,300)

# Función que se ejecuta de fondo para estar revisando la memoria caché
def ciclo_infinito():
    """ Esta soló es un ciclo infinito que revisa si una respuesta ya caduco."""
    x = 1
    while x >= 1:
        revisa_tiempo()
        # Espera 1 segundo
        time.sleep(1)
        
        
def start()->dict:
    """ Esta función inicializa la memoria caché de nuestro servent 
    argumentos:
    cache: memoria caché donde se almacenan las respuestas """

    # Hilo que se ejecutara de fondo para revisar la vida de cada petición
    thread = Thread(target=ciclo_infinito)
    thread.daemon = True                        # El hilo muere si el hilo principal muere
    thread.start()                              # Inicia el hilo
    
    # Devuelve la memoria caché
    return cache_manager

 
def insert(ip_address:str, answer:dict)->dict:
    """ Esta función guarda una respuesta recibida por el servent
    su memoria caché. 
    argumentos:
    cache: memoria caché donde se almacenan las respuestas
    ip_address: de dónde obtuvo la respuesta
    answer: respuesta que obtuvo"""
       
    # Guarda la respuesta que obtuvo y de donde la obtuvo
    cache_manager[ip_address] = answer
    # Devuelve la memoria caché
    return cache_manager

def content():
    """ Esta función devuelve el conenido de la memoria caché del servent."""
    return cache_manager

def print_cache():
    """ Esta función imprime el conenido de la memoria caché del servent."""
    for respuesta in list(cache_manager):
        print(cache_manager[respuesta]["Filename"],cache_manager[respuesta]["IP"],cache_manager[respuesta]["Port"],cache_manager[respuesta]["Tiempo"])