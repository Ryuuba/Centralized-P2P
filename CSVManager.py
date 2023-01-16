import socket, pickle
import sys
import os
import csv
from csv import writer
import pathlib
import glob
import pandas as pd


def append_list_as_row(file_name,list_of_elem):
	with open(file_name, 'a') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)
		
	# ~ with open(file_name,'a') as sfswrite_obj:
		# ~ number = [4]
		# ~ csv_writer = writer(write_obj,delimeter='')
		# ~ csv_writer.writerow(number)
	
 
# ~ # reading the csv file using read_csv
# ~ # storing the data frame in variable called df
# ~ df = pd.read_csv('md5file.csv')
 
# ~ # creating a list of column names by
# ~ # calling the .columns
# ~ list_of_column_names = list(df.columns)
 
# ~ # displaying the list of column names
# ~ print('List of column names : ',
      # ~ list_of_column_names)
      
csvFile = open('md5file.csv')
csvreader = csv.reader(csvFile)
numArchivos = 0
for row in csvreader:
	numArchivos = int(row[0])
	break
csvFile.close()

totalArchivos = 0
dir = "archivos"
for path in os.listdir(dir):
	if os.path.isfile(os.path.join(dir, path)):
		if path.endswith("iso"):
			totalArchivos += 1
print(totalArchivos)

if totalArchivos != numArchivos:
	listNewRow = []
	listaArchivos = glob.glob('archivos/*.iso')
	
	latestFile = max(listaArchivos,key=os.path.getctime)
	metadatos = latestFile.split("-");
	nombreConSlash = metadatos[0]
	nombre = nombreConSlash.split("/")[1];
	listNewRow.append(nombre)
	print(latestFile)
	print("Ingrese el sha256")
	sha256 = input()
	listNewRow.append(sha256)
	# ~ archivo = open('md5file.csv')
	# ~ #Aqui se le agrega el tamaño del archivo
	pesoArchivo = os.stat(str(latestFile)).st_size
	print(pesoArchivo)
	listNewRow.append(pesoArchivo)
	version = metadatos[1]
	listNewRow.append(version)
	arch = metadatos[3]
	listNewRow.append(arch)
	plataforma = metadatos[2]
	listNewRow.append(plataforma)
	nombreArchivo = latestFile.split("/");
	listNewRow.append(nombreArchivo[1])
	print(listNewRow)
	
	append_list_as_row('md5file.csv',listNewRow)
	infile = open("md5file.csv","r")
	reader = csv.reader(infile)
	mylist = list(reader)
	infile.close()
	mylist[0][0]=totalArchivos
	outfile = open("md5file.csv","w")
	writer = csv.writer(outfile)
	writer.writerows(mylist)
	
	outfile.close()
	
