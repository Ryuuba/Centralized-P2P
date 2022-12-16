from random import randint

def start()->dict:
    """ Esta función inicializa la memoria caché de nuestro servent 
    argumentos:
    cache: memoria caché donde se almacenan las respuestas """
    
    # Se inicializa la memoria caché como una colección
    cacheManager = {}
    # Devuelve la memoria caché
    return cacheManager

 
def insert(cache:dict, ip_address:str, answer:dict)->dict:
    """ Esta función guarda una respuesta recibida por el servent
    su memoria caché. 
    argumentos:
    cache: memoria caché donde se almacenan las respuestas
    ip_address: de dónde obtuvo la respuesta
    answer: respuesta que obtuvo"""
       
    # Guarda la respuesta que obtuvo y de donde la obtuvo
    cache[ip_address] = answer
    # Devuelve la memoria caché
    return cache


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
    answer["IP"]= randint(1,100)
    answer["Tiempo"]= randint(8,20)
    
    # Guarda la respuesta en la memoria caché
    cache = insert(cache,answer["IP"],answer)
    
    return cache,answer

