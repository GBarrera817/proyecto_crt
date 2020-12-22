"""Este proyecto tiene como objetivo completar la infomarmación faltante de los archivos que se descargan en Transbank, específicamente, completar el campo "N° Boleta"
"""

__author__ = 'Equipo Betaliers'
__email__ = 'proyect.betaliers.crtecommerce@gmail.com'
__status__ = 'Beta'
__version__ = '0.1'


import pandas as pd
import os
import resources.main as fm

CRT_PATH = os.path.dirname(os.path.abspath(__file__))
BSALE_PATH = os.path.join(CRT_PATH, 'datos/')
DAT_FILES_PATH = os.path.join(CRT_PATH, 'datos/2020/')


def main():
	fallo = False

	# Ruta estática desde donde se leerán los archivos
	

	# Obtención de los nombres de los archivos .dat
	# Se debe pasar como parámetros el directorio donde están los archivos
	# y la extensión de los archivos que se van a buscar
	dat_files_names = fm.list_files(DAT_FILES_PATH, 'dat')
	#print(dat_files_names)

	# for dat in dat_files_names:
	# 	print(f"[{dat_files_names.index(dat)+1}]", dat)
	#print(dat_files_names)

	# Limpieza de los archivos .dat.
	# Se debe pasar como parámetro la lista con los nombres de los archivos .dat
	# que retorna la función list_files()
	#print(dat_files_names[0])

	# El primer archivo .dat
	dat_files_cleaned = fm.dat_files_clean(dat_files_names[0])
	print(type(dat_files_cleaned))
	#print()
	#print(dat_files_cleaned)

	# Se guardan los archivos .dat filtrados a .csv
	fm.save_files(dat_files_names, dat_files_cleaned)

	# Lectura de archivo
	#csv_files = fm.list_files(DAT_FILES_PATH, 'csv')
	#print(csv_files)

	#for csv in csv_files:
		#print(f"[{csv_files.index(csv)}]", csv)

	#Bsale
	#xlsx_bsale = pd.read_excel(BSALE_PATH+'docSearchExport_cc0f2b54bf6e4b085d07fc2bdcdabf5fd73b1843.xlsx', header=11, sheet_name=None, engine='openpyxl')
	#xlsx_bsale

	#print(xlsx_bsale.keys())
	#df_bsale = xlsx_bsale.get('docSearchExport_cc0f2b54bf6e4b0')
	#print(df_bsale.columns)

	# Separo el archivo bsale con los datos de Boleta y Factura
	#df_bsale_bol_fact = df_bsale[(df_bsale['Tipo Documento'] == 'Boleta Electrónica') | (df_bsale['Tipo Documento'] == 'Factura Electrónica')]
	#print(df_bsale_bol_fact)

	#df_transbank = pd.read_csv(csv_files[8], delimiter=';')
	#print(df_transbank)

	# if not fallo:
	# 	print("Todo va super!")
	# else:
	# 	print("\Algo falló :C")

	return 0 if not fallo else 1


if __name__ == "__main__":
	exit(main())