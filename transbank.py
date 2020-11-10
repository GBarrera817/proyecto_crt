# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:58:46 2020

@author: Iván
"""

import pandas as pd
from proyecto_crt.lib.file_manager import dat_files_clean, list_files, save_files
import os

DAT_FILES_FOLDER = r'proyecto_crt/datos/'

dat_files_names = []
dat_files_names = list_files(DAT_FILES_FOLDER, '.dat')
print(dat_files_names)


dat_files_cleaned = []
dat_files_cleaned = dat_files_clean(dat_files_names)
#print(dat_files_cleaned)

save_files(dat_files_names, dat_files_cleaned)

#Lectura de archivo

csv_files = []
csv_files = list_files(DAT_FILES_FOLDER, '.csv')
print(csv_files)

df = pd.read_csv(csv_files[2], sep=';', encoding='utf8')

df.head()



