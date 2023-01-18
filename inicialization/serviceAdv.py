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




