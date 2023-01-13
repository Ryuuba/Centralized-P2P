import client
import os
import db
from tabulate import tabulate

if __name__ == '__main__':
        
    """print("Ingrese su usuario: ")
    user = input()
    print("\nIngrese su contraseña: ")
    password = input()"""
    
    #~ Loging message
    login_msg = client.login_msg("jesus", "jesus0000")
    
    #~ Execute the login line in terminal
    os.system(login_msg)
    print("\n")
    
    #~ Search a keyword
    resultados = db.search_content("Fedora")
    #~ Print the search results
    print(tabulate(resultados, headers=["Distro", "Version", "Archiquecture", "SHA256", "Size", "Target"]))