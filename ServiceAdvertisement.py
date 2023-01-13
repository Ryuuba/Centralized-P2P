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
"""

class ServiceAdvertisement:
	# Constructor
    def __init__(self, dir_path):
        self.dir_path = os.path.realpath(dir_path)
        self.listaArchivos = []
        #TODO
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock = sock
        
    def searchAllFiles(self):
        self.listaArchivos = []
        for root, dirs, files in os.walk(self.dir_path):
            print ("\n"+root+"\n")
            for file in files:
                self.listaArchivos.append(file)
                print ("/"+str(file))
        return self.listaArchivos


    def searchExtFiles(self,ext):
        self.listaArchivos = []
        for root, dirs, files in os.walk(self.dir_path):
            print (root+"\n")
            for file in files:
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
                        while element.isnumeric() or element == '.' and doneVersion == False:
                            versionNumber = versionNumber + element
                        doneVersion == True

                    metadatos = file.split("-");
                    print(metadatos)
                    distro = metadatos[0]
                    version = metadatos[1]
                    # ~ #Aqui se le agrega el tamaño del archivo
                    pesoArchivo = os.stat(self.dir_path+"/"+str(file)).st_size
                    print(pesoArchivo)
                    self.listaArchivos.append(str(file)+" "+sha256+" "+str(pesoArchivo)+" "+str(distro)+" "+str(version)+" "+str(arch))
                    print (str(file)+" "+sha256+" "+str(pesoArchivo))
                    
        return self.listaArchivos
        
    def sendServer(self,host,port):
        serverAddress = (host, port)
        self.sock.connect(serverAddress)
        data = pickle.dumps(self.listaArchivos)
        self.sock.sendall(data)
        self.sock.close()
			

files = ServiceAdvertisement("/home/tijuana/distribuidos/proyecto final/archivos")

lista = files.searchAllFiles()
print("Las Listas\n")
for elemento in lista:
    print(elemento)
    
lista = files.searchExtFiles(".iso")
for elemento in lista:
    print(elemento)
 
#files.sendServer("localhost",3333)