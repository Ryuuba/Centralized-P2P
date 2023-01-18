##funcion que reciba la respuesta

from threading import Thread
import time
from random import randint
import uuid

#debemos inicializar la variable cache manager vacia (esta mas adelante sera un diccionario)
cache_manager = {}

#debemos validar el timpo de una respuesta si esta tarda demasiado de deber eliminar
def tiempo_vida():
    for cache in list(cache_manager):
        if cache_manager[cache]["Tiempo"] == 0:
            del(cache_manager[cache])
        elif cache_manager[cache]["Tiempo"] >= 1:
            cache_manager[cache]["Tiempo"] -= 1

# Se debe ejecutar una funcion que sea infinita que revise el tiempo de vida
def ciclo():
    while (1):
        tiempo_vida()
        time.sleep(1)
        
def start()->dict:
    thread = Thread(target=ciclo)
    thread.daemon = True
    thread.start()
    return cache_manager

###GET SET Y PRINT
def set_cache(ip_address:str, answer:dict)->dict:
    cache_manager[ip_address] = answer
    return cache_manager

def get_cache():
    return cache_manager

def print_cache():
    for respuesta in list(cache_manager):
        print(cache_manager[respuesta]["Filename"],cache_manager[respuesta]["Tiempo"])

def buscar(cache:dict)-> tuple:
    respuestaPeticion = {}
    respuestaPeticion["Filename"]= "filename_respuesta"
    respuestaPeticion["MDS"]= "MDS_respuesta"
    respuestaPeticion["Size"]= "Size_respuesta"
    respuestaPeticion["Distro"]= "Distro_respuesta"
    respuestaPeticion["ARCK"]= "ARCK_respuesta"
    respuestaPeticion["IP"]= "IP_respueta"
    respuestaPeticion["Tiempo"]= randint(8,20)
    
    # Crea el identificador único de la respuesta 
    identificador_respuesta = uuid.uuid4().hex[:8]
    
    # Guarda la respuesta en la memoria caché
    cache = set_cache(identificador_respuesta, respuestaPeticion)
    
    return cache,respuestaPeticion
