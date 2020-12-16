import pandas as pd
import proyecto_crt.resources.file_manager as fm

# Ruta estática desde donde se leerán los archivos
DAT_FILES_FOLDER = r'proyecto_crt/datos/2020/'

# Obtención de los nombres de los archivos .dat
# Se debe pasar como parámetros el directorio donde están los archivos
# y la extensión de los archivos que se van a buscar
dat_files_names = fm.list_files(DAT_FILES_FOLDER, 'dat')
print(dat_files_names)

# Limpieza de los archivos .dat.
# Se debe pasar como parámetro la lista con los nombres de los archivos .dat
# que retorna la función list_files()
dat_files_cleaned = fm.dat_files_clean(dat_files_names)
print(dat_files_cleaned)

# Se guardan los archivos .dat filtrados a .csv
fm.save_files(dat_files_names, dat_files_cleaned)

# Lectura de archivo
csv_files = fm.list_files(DAT_FILES_FOLDER, 'csv')
#print(csv_files)

for csv in csv_files:
       print(f"[{csv_files.index(csv)}]", csv)


# Se lee el archivo csv guardado en la posición 'i'

df_tbdebito_enero = pd.read_csv(csv_files[1], sep=';', encoding=fm.get_file_encoding(csv_files[1]))

df_tbdebito_febrero = pd.read_csv(csv_files[2], sep=';', encoding=fm.get_file_encoding(csv_files[2]))

#df_bsale_enero = pd.read

#df_bsale_febrero = 


df_tbdebito_enero.head(10)
df_tbdebito_enero.info()

df_tbdebito_febrero.head(10)
df_tbdebito_febrero.info()



# Manipulación de archivo B-Sale

archivo = DAT_FILES_FOLDER+'docSearchExport_cc0f2b54bf6e4b085d07fc2bdcdabf5fd73b1843.xlsx'
print(archivo)

df1 = pd.read_excel(archivo)

df1.head()

df1.to_csv(DAT_FILES_FOLDER+'prueba.csv', encoding='utf8', sep=';')

archivo2 = DAT_FILES_FOLDER+'prueba.csv'
print(archivo2)
    
bsale_output = fm.bsale_clean_file(archivo2)
print(bsale_output)
#Guardar archivo

bsale = []
bsale.append(archivo2)
print(bsale)
fm.save_files(bsale, bsale_output)

df0 = pd.read_csv(archivo2, sep=';', encoding='utf8')
df1=df0.drop(df0.columns[[0]], axis='columns')
df1

