import inicialization.servant.cache_manager as cache_manager
import time
        
# Inicializa la memoria cache
cache = cache_manager.start()

#peticion = {"Distribucion":"Fedora","Resultados":10,"Version":35,"Cores":4,"conexiones":10}

cache, respuesta = cache_manager.buscar(cache)
cache, respuesta = cache_manager.buscar(cache)
cache, respuesta = cache_manager.buscar(cache)
cache, respuesta = cache_manager.buscar(cache)
cache, respuesta = cache_manager.buscar(cache)

while True:
    cache_manager.print_cache()
    print("\n")
    time.sleep(5)
    
quote_a = bytes.fromhex(quote_h).decode("ASCII")