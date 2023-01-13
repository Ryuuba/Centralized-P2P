import initialize_login
import client
import server
import socket
import threading
import time
from signal import pthread_kill, SIGTSTP
from itertools import count

"""
TODO:
    -Check that current serialization works with server
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

#Server starts
thread.start()

#Initial socket creation for login
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#This port number is central server's listening port
port = "6699"
#Sleep for one second so serevent's server information can be displayed correctly
time.sleep(1)

#As central server is run on the same machine as the servent, localhost should work. TODO: ask how this will work on production
server_address = ('localhost', int(port))

#Login process. Server closes socket whenever it recieves erronous login information.
#In order to allow user to retry logging in, we create a new socket if the login process fails.
#If login is successfull, this socket will be kept open throughout the execution
#Currently, login only works when user inputs correct information on the first try. 
loginResult = False
attempt = 0
while loginResult == False:
    if attempt == 1:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    loginResult = initialize_login.loginToSystem(sock, server_address,port)
    if loginResult == False:
        #Creating new socket to reconnect to server
        attempt = 1
print("Bienvenido al sistema de distribución de imagenes de Linux")

#After successful login, should execute initialize_servicead


#After service advertisement, client shows menu and runs until user quits program
choice = "1"
while(choice != "2"):
    print("Elige una operación\n1. Buscar una imagen\n2. Cerrar sesión")
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

#Another thread should continously probe shared folder for any changes
#When a change is detected, servent logs in to server and redoes service advertisement



"""
#This code is used to test this servent's HTTP server
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
"""
