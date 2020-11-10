# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:58:46 2020

@author: Iván
"""

import pandas as pd
from proyecto_crt.lib.file_manager import dat_files_clean, list_files, save_files
import os

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
#print(dat_files_cleaned)

# Se guardan los archivos .dat filtrados a .csv
save_files(dat_files_names, dat_files_cleaned)

# Lectura de archivo
csv_files = []
csv_files = list_files(DAT_FILES_FOLDER, '.csv')
print(csv_files)

df = pd.read_csv(csv_files[2], sep=';', encoding='utf8')

df.head()



