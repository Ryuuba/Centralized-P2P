import servent
import os
from threading import Thread
import db
from tabulate import tabulate

def options_menu():
    salir = False
    while(salir != True):
        print("\nElige una operación\n1. Buscar una imagen\n2. Cerrar sesión")
        choice = input()
        if choice == "1":
            print("\nInserta el nombre de la distribución que quieres encontrar:")
            keyword = input()
            #~ Search a keyword
            resultados = db.search_content(keyword)
            if len(resultados) >= 1:
                #~ Print the search results
                print(tabulate(resultados, headers=["Distro", "Version", "Archiquecture", "Size", "Target", "Name", "IP", "Port"]))
                print("\n¿Quieres descargar alguna imagen? (s/n)" )
                if input() == 's':
                    servent.download_file()
                    opcion = 's'
                    while opcion != 'n':
                        print("\n¿Quieres descargar otra imagen de esta busqueda? (s/n)" )
                        opcion = input()
                        if opcion == 's':
                            servent.download_file()
            else:
                print("Lo siento, no se encontraron resultados para esa palabra clave\n")
            
            print("¿Quieres seguir usando el sistema? (s/n)" )
            if input() == 'n':
                print("Cerrando sesión y apagando el servidor HTTP...")
                db.close_connection()
                salir = True

        elif choice == "2":
            print("Cerrando sesión y apagando el servidor HTTP...")
            db.close_connection()
            salir = True
        else:
            print("La opción introducida no es válida.")

    #Another thread should continously probe shared folder for any changes
    #When a change is detected, servent logs in to server and redoes service advertisement

if __name__ == '__main__':
        
    """print("Ingrese su usuario: ")
    user = input()
    print("\nIngrese su contraseña: ")
    password = input()"""
    user = 'jesus'
    password = 'jesus0000'
    
    #~ Loging message
    login_msg = servent.login_msg(user, password)
    #~ Execute the login line in terminal
    resultado_login = os.popen(login_msg).read()
    
    if resultado_login == '00190003napster@napster.com':
        print("Ingresa un usuario y contraseña validos\n")
    else:
        print("Bienvenido al sistema de distribución de imagenes de Linux", user)

        #Server starts and die if the main thread die
        thread = Thread(target=servent.mountServer, args=("shared_content/",))
        thread.daemon = True
        thread.start()  

        options_menu()