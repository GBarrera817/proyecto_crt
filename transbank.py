# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:58:46 2020

@author: Iván
"""

import pandas as pd
import proyecto_crt.resources.file_manager as fm

# Ruta estática desde donde se leerán los archivos
DAT_FILES_FOLDER = r'proyecto_crt/datos/'

# Obtención de los nombres de los archivos .dat
# Se debe pasar como parámetros el directorio donde están los archivos
# y la extensión de los archivos que se van a buscar
dat_files_names = []
dat_files_names = list_files(DAT_FILES_FOLDER, '.dat')
print(dat_files_names)

# Limpieza de los archivos .dat.
# Se debe pasar como parámetro la lista con los nombres de los archivos .dat
# que retorna la función list_files()
dat_files_cleaned = []
dat_files_cleaned = dat_files_clean(dat_files_names)
print(dat_files_cleaned)

# Se guardan los archivos .dat filtrados a .csv
save_files(dat_files_names, dat_files_cleaned)

# Lectura de archivo
csv_files = []
csv_files = list_files(DAT_FILES_FOLDER, '.csv')
print(csv_files)

# Se lee el archivo csv guardado en la posición 'i'
df = pd.read_csv(csv_files[2], sep=';', encoding='latin-1')


df = pd.read_csv(csv_files[2], sep=";", names=['Tipo Transacción', 'Fecha Venta', 'Tipo Tarjeta', 'Identificador',
       'Tipo Venta', 'Código Autorización Venta', 'Nº Cuota',
       'Monto Transacción', 'Monto Afecto', 'Comisión e IVA Comisión',
       'Monto Exento', 'Nº Boleta', 'Monto Anulación', 'Monto Retenido',
       'Devolución Comisión', 'Monto Retención', 'Motivo', 'Período de Cobro',
       'Detalle de cobros u observación', 'Monto', 'IVA', 'Fecha Abono',
       'Cuenta de Abono', 'Local'], encoding= "ISO-8859-1").drop([0])

df.head()



# Manipulación de archivo B-Sale

archivo='proyect_crt/datos/docSearchExport_cc0f2b54bf6e4b085d07fc2bdcdabf5fd73b1843.xlsx'

df1 = pd.read_excel(archivo)

df1.to_csv('C:\\Users\\Iván\\Desktop\\Betaliers\\Proyecto CRT\\docSearchExport_cc0f2b54bf6e4b085d07fc2bdcdabf5fd73b1843.csv', encoding='utf8', sep=';')

archivo2='C:\\Users\\Iván\\Desktop\\Betaliers\\Proyecto CRT\\docSearchExport_cc0f2b54bf6e4b085d07fc2bdcdabf5fd73b1843.csv'


newlines2 = []
i=0
with open(archivo2, 'r', encoding='utf8') as input_file2:
    lines2 = input_file2.readlines()
    newlines2 = []
    print(lines2)
    i=0
    for linea2 in lines2:
        #print(linea)
        i += 1
        linea2 = linea2.split(';')
        
        if linea2[1] == 'Tipo Documento'and linea2[2]=='Nº Documento':
            print(linea2)
            print(i)
            break
    print(i)
    newLines2 = lines2[i-1:]
    
    
save='C:\\Users\\Iván\\Desktop\\Betaliers\\Proyecto CRT\\b-sale2020.csv'
    
f2=open(save,'w')
for linea2 in newLines2:
    f2.write(linea2)
f2.close()    

ruta='C:\\Users\\Iván\\Desktop\\Betaliers\\Proyecto CRT\\b-sale2020.csv'

df0 = pd.read_csv(ruta, sep=';', encoding='Latin-1')
df1=df0.drop(df0.columns[[0]], axis='columns')
df1

BE=df1[df1['Tipo Documento'] == 'Boleta Electrónica']
FO=df1[df1['Tipo Documento'] == 'Factura Electrónica']

with pd.ExcelWriter('C:\\Users\\Iván\\Desktop\\Betaliers\\Proyecto CRT\\B-SALE.xlsx') as writer:
    BE.to_excel(writer, sheet_name='Boleta electrónica')
    FO.to_excel(writer, sheet_name='Factura Electrónica')