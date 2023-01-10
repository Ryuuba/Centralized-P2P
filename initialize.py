import initialize_login
import client
import server
import socket
import threading
import time

"""
TODO:
    -Check that generated message follows established format
    -Check that current serialization works with server
    -Generate servent keys and send public key to central server (?)
        -Which code is used when servent sends its public key to the central server? Does sservent needs to gen/send key at all?
    -Integrate this code with other modules and test login process together with service advertisement
    -Implement answer message parsing
"""

def run_server(route):
    #HTTP server port number should be reported back to server
    print("Inciando servidor...")
    server.mountServer(route)

#One thread should be executing initialize_cacheman

#Another thread executes this servent's server
thread = threading.Thread(target=run_server, args=("/run/media/cardcathouse/",))
thread.start()
#Socket creation
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#This port number is central server's listening port
port = "6699"
time.sleep(1)
#As central server is run on the same machine as the servent, localhost should work. TODO: ask how this will work on production
server_address = ('localhost', int(port))
initialize_login.loginToSystem(sock, server_address,port)
print("Bienvenido al sistema de distribución de imagenes de Linux")
#After successful login, should execute initialize_servicead

#After service advertisement, client runs until user quits program.
#When run on cluster, this could be rank 0

print("Inserta la dirección IP del servidor: ")
ipAddress = input()
print("Inserta el puerto del servidor:")
port = input()
choice = '1'
while(choice == '1'):
    print("Selecciona una opción:\n1. Obtener un archivo\n2.Salir")
    choice = input()
    if choice == '1':
            print("Inserta el nombre del archivo que quieres obtener: ")
            filename = input()
            print("Obteniendo archivo....")
            #For now we assume user will always input an existing file, and that there will be no errors in sending and receiving the file
            client.getFile(ipAddress, filename, port)
            print("Archivo obtenido de manera exitosa.")
    else:
        print("Saliendo del sistema...")
        #Assuming the whole system shuts down when user quits client
        thread.join()
        break