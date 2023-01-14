import initialize_login
import server
import socket
import threading
import time
import ServiceAdvertisement

def run_server(route):
    #HTTP server port number should be reported back to server
    print("Inciando servidor...")
    server.mountServer(route)

#Initial socket creation for login
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#This port number is central server's listening port
port = "6699"

#As central server is run on the same machine as the servent, localhost should work. TODO: ask how this will work on production. probably hardcoded?
server_address = ('localhost', int(port))
#Ask for directory to be used to mount HTTP server and service advertisement
serverDirMount = ""

loginResult = initialize_login.loginToSystem(sock, server_address,port)
#Login process. If user enters erronous information, program will quit.
if loginResult == False:
    quit()
else:
    print("Bienvenido al sistema de distribución de imagenes de Linux\nIniciando proceso de notificación al servidor...")
    print("Inserta la ruta del directorio que será usado para compartir archivos:")
    serverDirMount = input()
    #do service advertisement.
    print("Proceso de notificación de servicios terminado. Iniciando servidor HTTP en " + serverDirMount)

#Another thread executes this servent's server
thread = threading.Thread(target=run_server, args=(serverDirMount,))

#Server starts
thread.start()

#One thread should be executing initialize_cacheman
print("Iniciando gestor de caché...")

#After service advertisement and server mount, client shows menu and runs until user quits program
choice = "1"
while(choice != "2"):
    print("Elige una operación\n1. Buscar una imagen\n2. Sincronizar archivos compartidos al servidor\n3. Cerrar sesión")
    choice = input()
    if choice == "1":
        print("Inserta el nombre de la distribución que quieres encontrar:")
        distro = input()
        #TODO: search and fetch
        print("El archivo se descargó correctamente.\n¿Quieres seguir usando el sistema? (s/n)" )
        choice2 = input()
        if input == "n":
            print("Cerrando sesión y apagando el servidor HTTP...")
            thread.join()
            choice = "2"
    elif choice == "2":
        print("Cerrando sesión y apagando el servidor HTTP...")
        thread.join()
    else:
        print("La opción introducida no es válida.")

