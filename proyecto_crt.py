"""Este proyecto tiene como objetivo completar la infomarmación faltante de los archivos que se descargan en Transbank, específicamente, completar el campo "N° Boleta"
"""

__author__ = 'Equipo Betaliers'
__email__ = 'proyect.betaliers.crtecommerce@gmail.com'
__status__ = 'Beta'
__version__ = '0.1'


import pandas as pd
import os
import resources.main as fm


def main():
	fallo = False

	# Ruta estática desde donde se leerán los archivos
	CRT_PATH = os.path.dirname(os.path.abspath(__file__))
	DAT_FILES_PATH = os.path.join(CRT_PATH, 'datos/2020/')

	# Obtención de los nombres de los archivos .dat
	# Se debe pasar como parámetros el directorio donde están los archivos
	# y la extensión de los archivos que se van a buscar
	dat_files_names = fm.list_files(DAT_FILES_PATH, 'dat')
	print(dat_files_names)

	# Limpieza de los archivos .dat.
	# Se debe pasar como parámetro la lista con los nombres de los archivos .dat
	# que retorna la función list_files()
	dat_files_cleaned = fm.dat_files_clean(dat_files_names)
	print(dat_files_cleaned)

	# Se guardan los archivos .dat filtrados a .csv
	fm.save_files(dat_files_names, dat_files_cleaned)

	# Lectura de archivo
	# csv_files = fm.list_files(DAT_FILES_FOLDER, 'csv')
	# #print(csv_files)

	# for csv in csv_files:
	# 	print(f"[{csv_files.index(csv)}]", csv)


	

	if not fallo:
		print("Todo va super!")
	else:
		print("\Algo falló :C")

	return 0 if not fallo else 1


if __name__ == "__main__":
    exit(main())