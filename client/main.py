import os
import hashlib

if __name__ == '__main__':
        
    print("Ingrese su usuario: ")
    user = input()
    print("\nIngrese su contraseña: ")
    password = input()
    
    # Login message
    msg_user = user + ' ' + password + ' 20041 netcat'
    payload_lenght = "{:04d}".format(len(msg_user))
    msg_type = '0002'
    login_msg = 'printf "' + payload_lenght + msg_type + msg_user
    
    # Notification message
    with open('share_content/files.txt', 'rb') as file:
        for line in file:
            archivo = line.split()
            distro = archivo[0].decode()
            sha256 = hashlib.sha256(line.rstrip()).hexdigest()
            size = archivo[1].decode()
            version = archivo[2].decode()
            arch = archivo[3].decode()
            target = archivo[4].decode()
            file_name = archivo[5].decode()
            anuncio = distro + " " + sha256 + " " + size + " " + version + " " + arch + " " + target + " " + file_name
            anuncio_lenght = "{:04d}".format(len(anuncio))
            login_msg = login_msg + anuncio_lenght + '0064' + anuncio
            
    login_msg = login_msg + '" | ncat localhost 6699'
    #print(login_msg)
    
    # Execute the login line in terminal
    os.system(login_msg)