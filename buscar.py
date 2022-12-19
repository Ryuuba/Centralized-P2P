import initialize_cache_manager as cache_manager
from random import randint
import uuid

def search(cache:dict, peticion:dict)->tuple[dict,dict]:
    # Busqueda
    
    
    
    # Se inicializa la respuesta
    answer = {}
    # Se registras los valores obtenidos (Por ahora solo guarda un texto de prueba)
    answer["Filename"]= "filename_respuesta"
    answer["MDS"]= "MDS_respuesta"
    answer["Size"]= "Size_respuesta"
    answer["Distro"]= "Distro_respuesta"
    answer["ARCK"]= "ARCK_respuesta"
    answer["IP"]= "IP_respueta"
    answer["Tiempo"]= randint(8,20)
    
    # Crea el identificador único de la respuesta 
    identificador_respuesta = uuid.uuid4().hex[:8]
    
    # Guarda la respuesta en la memoria caché
    cache = cache_manager.insert(identificador_respuesta, answer)
    
    return cache,answer

