import initialize_login
import client
import server
import socket
import sys
import threading
import time

def run_server(route):
    #Should the port number assigned to server be reported back somewhere?
    print("Inciando servidor...")
    server.mountServer(route)

#One thread should be executing initialize_cacheman

#Another thread executes this servent's server
thread = threading.Thread(target=run_server, args=("/run/media/cardcathouse/",))
thread.start()

#Socket creation
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = "49999"
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