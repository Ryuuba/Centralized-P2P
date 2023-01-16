# Es el que se va a encargar de los mensajes,es decir lo que tiene que hacer es 
# notificar la parte de los recursos compartidos, entonces que tenemos que hacer 
# para implementar el ServiceAdvertisement, se debe de leer la carpeta de los 
# recursos compartidos. Una vez que leemos la carpeta de los recursos compartidos 
# deberíamos de tener un bucle que se envíen tanto mensajes como contenidos se 
# vayan a compartir y ese ServiceAdvertisement lo que tenia que hacer es de 
# alguna manera generar los mensajes (debemos de tener la estructura para enviar el mensaje) 



# Se tiene que encargar de leer el contenido de la carpeta, con base del contenido de la carpeta
# compartida, enviarlos

#Enviar un mensaje por cada servicio compartido

#usar un socket modo avion enviar sin esperar la respuesta

#cuando enviamos los contenidos podemos usar el nedcat, para ver que el servidor le estan llegando los mensajes que 


# todo lo que yo tengo en mi carpeta lo mando al servidor


#Cuando recibimos un contenido tendriamos que volver a notificar, es decir, si ya tenemos un contenido nuevo
#deberiamos de notificarlo en el servidor que ya podemos compartir otra cosa

import os
import socket
directorio = ""

class imagen(object):
    def __init__ (self, path):
        self.imagenes_iso = []
        self.path = path
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def getPath(self):
        return self.path

    def __str__ ():
        return "%s" % (self.path)


    def listaArchivos(directorio):
        with os.scandir(directorio) as ficheros:
            for fichero in ficheros:
                print(fichero.name)
        

    def buscarArchivoCompartido(directorio):
        contenido = os.listdir(directorio)
        imagenes_iso = []
        md5 = ""
        arch = ""
        for fichero in contenido:
            if os.path.isfile(os.path.join(directorio, fichero)) and fichero.endswith('.iso'):
                print("el fichero es..: " + fichero)
                pesoArchivo = os.path.realpath(fichero)
                print("peso es..: " + pesoArchivo)
                #pesoArchivo = os.stat(fichero.dir_path+"/"+fichero.st_size)
                #pesoArchivo = os.stat(fichero).st_size
                metadatos = fichero.split("-")
                print("los metadatos son: ")
                print(metadatos)
                distro = metadatos[0]
                version = metadatos[1]
                imagenes_iso.append(str(fichero)+" "+md5+" "+str(pesoArchivo)+" "+str(distro)+" "+str(version)+" "+str(arch))
                print("La lista es: ")
                print(imagenes_iso)
                
        
    def enviarArchivoServidor(host, puerto,):
            # create an INET, STREAMing socket
            #
            # bind the socket to a public host, and a well-known port
            serversocket.bind((host, puerto))
            serversocket.connect(host,puerto)
            #Enviar el data

imagenIso = imagen
miDirectorio = "/home/alanbc/Documentos/distribuciones"
imagenIso.buscarArchivoCompartido(miDirectorio)




