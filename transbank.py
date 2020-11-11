# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:58:46 2020

@author: Iván
"""

import pandas as pd
from proyecto_crt.resources.file_manager import *

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



