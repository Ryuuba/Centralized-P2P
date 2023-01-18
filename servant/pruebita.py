import os
import hashlib

if __name__ == '__main__':
            
    # Notification message
    with open("/home/alanbc/Documentos/distribuciones") as file:
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
            print(anuncio)
            anuncio_lenght = "{:04d}".format(len(anuncio))
            # login_msg = login_msg + anuncio_lenght + '0064' + anuncio
            

    
    