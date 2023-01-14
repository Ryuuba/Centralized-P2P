import socket, pickle
import sys
import os
import csv

"""
Service advertisment notification should follow this format:
[PS][MT][DN][SHA][SZ][VN][P][FN]
PS = Payload size (in bytes)
MT = Message Type (always 0x0064)
DN = Distro name (e.g. "Fedora", "Manjaro", etc.)
SHA = Distro's SHA256 signature
SZ = File size
VN = Distro version number
P = Platform (e.g. "Desktop", "Raspberry Pi", "Server", etc.)
FN = filename

example:
01410064PopOS b961a5c7e205fd2cb37c8782b471858cbf4fb453bc5deeb0652bb028efccbfb1 3134275584 22.04 AMD64 Nvidia-Desktop pop-os_22.04_amd64_nvidia_20.iso
TODO: 
    -CSV is missing some fields (distro name, version number, platform)
    -compose message to send through socket
    -change md5 for sha256
    -how to get distro name? Manual input? Rename all files? Detect number?
    -actually write files to csv...
    -identify when file is on csv already


    On searchExtFiles, if file is ISO, the following should happen:
        -read distro name from filename. distro name is all letter before "-", "_" or number
        -check if file is not on csv already:
        -if on csv
            -skip to next file
        -if file not on csv
            -read image information from filename and sha256 signature from file with ".sha256" extension
            -sha256 filename should match iso filename
            -write information to csv
    
    Method:
    -csv content is replaced whenever folder is probed
    -Read all files from shared folder but only work with isos
        -distro name is usually first word before "-" "_" or a number
        -version are numbers before next "-" or "_"
        -print filename and ask user platform ("desktop, etc...)
        -it's probably easier to ask user to input platform given the variety of names 

"""

class ServiceAdvertisement:
	# Constructor
    def __init__(self, dir_path, sock):
        self.dir_path = os.path.realpath(dir_path)
        self.listaArchivos = []
        self.sock = sock

    def searchFilesAndSend(self,ext):
        #Create array that will store file info
        self.listaArchivos = []
        #Open csv file and delete all its content
        csvFile = open('')
        #Extract information for every file
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                correct = False
                while correct == False:
                    distroName = ""
                    sha = ""
                    filesize = ""
                    version = ""
                    platform = ""
                    fileName = file
                    #Control variables
                    if file.endswith(".iso"):
                        print("Analizando archivo " + file + "\n")
                        print("Inserta el nombre de la distribución: ")
                        distroName = input()
                        print("Inserta la firma SHA-256: ")
                        sha = input()
                        filesize = os.stat(self.dir_path+"/"+str(file)).st_size
                        print("Inserta el número de versión del sistema operativo: ")
                        version = input()
                        print("Inserta la plataforma del sistema operativo: ")
                        platform = input()
                        print("Se enviarán estos datos:\n")
                        print("Nombre de la distribución: " + distroName
                        + "\nFirma SHA-256: " + sha
                        + "\nTamaño del archivo: " + filesize
                        + " bytes\nVersión: " + version
                        + "\nPlataforma: " + platform + 
                        "\n¿Esto es correcto? 1. Sí     2.No")
                        choice = input()
                        if choice == '2':
                            "Ingresa los datos de nuevo...\n"
                        else:
                            #Write info on csv
                            print("Hola")
            #Then send all notifications to 


                """
                if file.endswith(ext):
                    sha256=""
                    arch=""
                    csvFile = open('md5file.csv')
                    iso = ""
                    distroName = ""
                    versionNumber = ""
                    platform = ""



                    type(csvFile)
                    csvreader = csv.reader(csvFile)
                    for row in csvreader:
                        if file == row[0]:
                            sha256 = row[1]
                            arch = row[2]
                    type(iso)
                    doneName = False
                    doneVersion = False
                    doneArch = False
                    donePlatform = False
                    for element in file:
                        while element != "-" or "_" and doneName == False:
                            distroName = distroName + element
                        doneName = True
                        if element.isnumeric():
                            versionNumber = versionNumber + element
                        


                            
                    metadatos = file.split("-");
                    print(metadatos)
                    distro = metadatos[0]
                    version = metadatos[1]
                    # ~ #Aqui se le agrega el tamaño del archivo
                    pesoArchivo = os.stat(self.dir_path+"/"+str(file)).st_size
                    print(pesoArchivo)
                    self.listaArchivos.append(str(file)+" "+sha256+" "+str(pesoArchivo)+" "+str(distro)+" "+str(version)+" "+str(arch))
                    print (str(file)+" "+sha256+" "+str(pesoArchivo))
                    """
                    
        return self.listaArchivos
        
    def sendServer(self,host,port):
        serverAddress = (host, port)
        self.sock.connect(serverAddress)
        data = pickle.dumps(self.listaArchivos)
        self.sock.sendall(data)
        self.sock.close()
			
print("Insert")
files = ServiceAdvertisement("/home/tijuana/distribuidos/proyecto final/archivos")

    
lista = files.searchExtFiles(".iso")
for elemento in lista:
    print(elemento)
 
#files.sendServer("localhost",3333)