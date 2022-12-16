import initialize_cache_manager as cache_manager
import buscar
import time
        
# Inicializa la memoria cache
cache = cache_manager.start()

# Peticion que realizara
peticion = {"Tipo_Distro":"Ubuntu","Max_Results":5,"Version":20.2,"Cores":2,"Max_Conections":5}

# Guarda el resultado y la cache
cache, respuesta = buscar.search(cache, peticion)
cache, respuesta = buscar.search(cache, peticion)
cache, respuesta = buscar.search(cache, peticion)
cache, respuesta = buscar.search(cache, peticion)
cache, respuesta = buscar.search(cache, peticion)


# Revisa que si se eliminen las respuestas cuando termina su tiempo de vida
x =1 
while x >= 1:
    #cache = cache_manager.content()
    cache_manager.print_cache()
    print("\n")
    time.sleep(5)
