import cache_manager
import time
        
# Inicializa la memoria cache
cache = cache_manager.start()

peticion = {"Tipo_Distro":"Ubuntu","Max_Results":5,"Version":20.2,"Cores":2,"Max_Conections":5}

cache, respuesta = cache_manager.buscar(cache, peticion)
cache, respuesta = cache_manager.buscar(cache, peticion)
cache, respuesta = cache_manager.buscar(cache, peticion)
cache, respuesta = cache_manager.buscar(cache, peticion)
cache, respuesta = cache_manager.buscar(cache, peticion)

# Revisa que si se eliminen las respuestas cuando termina su tiempo de vida
while (1):
    #cache = cache_manager.content()
    cache_manager.print_cache()
    print("\n")
    time.sleep(5)