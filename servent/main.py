import servent
import os
from threading import Thread

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
    
    print(resultado_login)
    
    if resultado_login == '00190003napster@napster.com':
        print("Ingresa un usuario y contraseña validos\n")
    else:
        print("Bienvenido al sistema de distribución de imagenes de Linux", user)

        #Server starts and die if the main thread die
        thread = Thread(target=servent.mountServer, args=("shared_content/",))
        thread.daemon = True
        thread.start()
        
        #continuously checks the shared folder
        files_first_time = os.listdir('shared_content')
        thread = Thread(target=servent.check_shared_folder, args=(len(files_first_time), user, password,))
        thread.daemon = True
        thread.start() 

        servent.options_menu()