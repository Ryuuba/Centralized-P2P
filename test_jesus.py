import initialize_cache_manager
from threading import Thread
import time

# Función que revisa el tiempo de vida de una respuesta
def revisa_tiempo():
    for respuesta in list(cache_manager):
        if cache_manager[respuesta]["Tiempo"] >= 1:
            cache_manager[respuesta]["Tiempo"] -= 1
        elif cache_manager[respuesta]["Tiempo"] == 0:
            # La respuesta tiene un tiempo de vida
            del(cache_manager[respuesta])  

# Función que se ejecuta de fondo para estar revisando la memoria caché
def ciclo_infinito():
    x = 1
    while x >= 1:
        revisa_tiempo()
        # Espera 1 segundo
        time.sleep(1)

# Inicializa la memoria cache
cache_manager = initialize_cache_manager.start()

# Hilo que se ejecutara de fondo para revisar la vida de cada petición
thread = Thread(target=ciclo_infinito)
thread.daemon = True                        # El hilo muere si el hilo principal muere
thread.start()                              # Inicia el hilo

# Peticion que realizara
peticion = {"Tipo_Distro":"Ubuntu","Max_Results":5,"Version":20.2,"Cores":2,"Max_Conections":5}


# Guarda el resultado y la cache
cache_manager, respuesta = initialize_cache_manager.search(cache_manager, peticion)
cache_manager, respuesta = initialize_cache_manager.search(cache_manager, peticion)
cache_manager, respuesta = initialize_cache_manager.search(cache_manager, peticion)
cache_manager, respuesta = initialize_cache_manager.search(cache_manager, peticion)
cache_manager, respuesta = initialize_cache_manager.search(cache_manager, peticion)


# Revisa que si se eliminen las respuestas cuando termina su tiempo de vida
y =1 
while y >= 1:
    print(cache_manager,"\n")
    time.sleep(1)
