import pandas as pd
import proyecto_crt.resources.file_manager as fm

archivo_tbank = 'proyecto_crt/datos/Transbank 2020 CRT.xlsx'

df = pd.read_excel(archivo_tbank)
df_nuevo = df.iloc[25:]

df_nuevo.head(20)

