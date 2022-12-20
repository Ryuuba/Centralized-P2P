import socket, pickle
import sys
import os
import csv

class ServiceAdrvertisement:
		# Constructor
		def __init__(self, dir_path):
			self.dir_path = os.path.realpath(dir_path)
			self.listaArchivos = []
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
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
						md5=""
						arch=""
						csvFile = open('md5file.csv')

						type(csvFile)
						csvreader = csv.reader(csvFile)
						for row in csvreader:
							if file == row[0]:
								md5 = row[1]
								arch = row[2]
								
						metadatos = file.split("-");
						print(metadatos)
						distro = metadatos[0]
						version = metadatos[1]
						# ~ #Aqui se le agrega el tamaño del archivo
						pesoArchivo = os.stat(self.dir_path+"/"+str(file)).st_size
						print(pesoArchivo)
						self.listaArchivos.append(str(file)+" "+md5+" "+str(pesoArchivo)+" "+str(distro)+" "+str(version)+" "+str(arch))
						print (str(file)+" "+md5+" "+str(pesoArchivo))
						
			return self.listaArchivos
			
		def sendServer(self,host,port):
			serverAddress = (host, port)
			self.sock.connect(serverAddress)
			data = pickle.dumps(self.listaArchivos)
			self.sock.sendall(data)
			self.sock.close()
			
files = ServiceAdrvertisement("/home/tijuana/distribuidos/proyecto final/archivos")

lista = files.searchAllFiles()
print("Las Listas\n")
for elemento in lista:
    print(elemento)
    
lista = files.searchExtFiles(".iso")
for elemento in lista:
    print(elemento)
 
files.sendServer("localhost",3333)







