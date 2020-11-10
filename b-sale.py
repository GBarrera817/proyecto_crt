# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 22:12:02 2020

@author: Iván
"""


import pandas as pd

archivo='C:\\Users\\Iván\\Desktop\\Betaliers\\Proyecto CRT\\docSearchExport_cc0f2b54bf6e4b085d07fc2bdcdabf5fd73b1843.xlsx'

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





