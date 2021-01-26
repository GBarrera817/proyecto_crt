# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:50:40 2020
GUI para CRT
@author: Pipe San Martín
"""

# importar librerías gráficas
from tkinter import *   # Carga módulo tk (widgets estándar)
from tkinter import filedialog
from tkinter import ttk	# Carga ttk (para widgets nuevos 8.5+)
import os
import pandas as pd
from threading import Thread


# Crea una clase Python para definir el interfaz de usuario de
# la aplicación. Cuando se cree un objeto del tipo 'Aplicacion'
# se ejecutará automáticamente el método __init__() qué 
# construye y muestra la ventana con todos sus widgets: 
class Application:
	def __init__(self):

		# Define la ventana principal de la aplicación
		self.root = Tk()
		self.root.title('Boletafinder') # Títutlo de la ventana
		self.root.geometry("1100x300") # Tamaño de la ventana: anchura x altura
		self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='resources/icons/crt.png'))
		#center_window(1000, 300)
		
		self.frame = ttk.Frame(self.root, borderwidth=5,
                               relief='solid', padding=(10, 10), height=1100, width=300) # relief = (flat, groove, raised, ridge, solid, or sunken)

		# Etiquetas
		self.lbl_tbank = ttk.Label(self.frame, text='Archivo Transbank', padding=(5, 5))
		self.lbl_bsale = ttk.Label(self.frame, text='Archivo Bsale', padding=(5, 5))
		self.lbl_tban_hist = ttk.Label(self.frame, text='Histórico Transbank', padding=(5, 5))
		self.lbl_result = ttk.Label(self.frame, text='Resultado', padding=(5, 5))
		self.statusTbnk = ttk.Label(self.frame, text='Sin archivo', padding=(5, 5))
		self.statusBsale = ttk.Label(self.frame, text='Sin archivo', padding=(5, 5))
		self.statusTbnkHist = ttk.Label(self.frame, text='Sin archivo', padding=(5, 5))
		self.status = ttk.Label(self.frame, text='Aun no ha procesado', padding=(5, 5))

        # Radiobuttons
		self.seleccionado = IntVar() # Guarda la opcion que se marque en los radio button
		self.radio_debito = ttk.Radiobutton(self.frame, text='Proceso débito', value=1, variable=self.seleccionado, command=self.clickeado)
		self.radio_credito = ttk.Radiobutton(self.frame, text='Proceso crédito', value=2, variable=self.seleccionado, command=self.clickeado)
		self.radio_debito.focus_set()

		# Botones
		self.btn_cargar_tbank = ttk.Button(self.frame, text='Cargar', command=self.carga_transbank)
		self.btn_cargar_bsale = ttk.Button(self.frame, text='Cargar', command=self.carga_bsale, )
		self.btn_cargar_historico = ttk.Button(self.frame, text='Cargar histórico', command=self.cargar_tbank_historico)
		self.btn_procesar = ttk.Button(self.frame, text='Procesar', command=self.procesamiento)
		self.btn_cargar_tbank.focus_set()

		# Posiciones etiquetas y entradas
		self.frame.grid(column=0, row=0)
		#self.frame.place(x=1100, y=300)

		self.radio_debito.grid(column=0, row=0, padx=50, pady=10)
		self.radio_credito.grid(column=1, row=0, padx=50, pady=10)

		self.lbl_tbank.grid(column=0, row=1, padx=10, pady=10) # Tbank
		self.btn_cargar_tbank.grid(column=1, row=1, padx=10, pady=10)
		self.statusTbnk.grid(column=2, row=1, padx=2, pady=0)

		self.lbl_bsale.grid(column=0, row=2, padx=10, pady=10) # Bsale
		self.btn_cargar_bsale.grid(column=1, row=2, padx=10, pady=10)
		self.statusBsale.grid(column=2, row=2, padx=2, pady=0)

		self.lbl_tban_hist.grid(column=0, row=3, padx=10, pady=10)  # Tbank Hist
		self.btn_cargar_historico.grid(column=1, row=3, padx=10, pady=10)
		self.statusTbnkHist.grid(column=2, row=3, padx=10, pady=10)

		self.btn_procesar.grid(column=1, row=4, padx=10, pady=10)
		self.lbl_result.grid(column=0, row=5, padx=10, pady=10) # Resultado
		self.status.grid(column=1, row=5, padx=10, pady=10)

		self.root.mainloop()
	

	def clickeado(self):
		if self.seleccionado.get() == 1:
			 
			self.btn_cargar_historico.configure(state='disabled')
		else:
			self.btn_cargar_historico.configure(state='enable')
		

	def dat_files_clean_worker(self):
		"""Limpieza de los archivos '.dat'.
		Se eliminan las filas que no son de interés para la
		obtención de información.

		Parameters
		----------

		files : list
			nombres de los archivos .dat

		Returns
		-------

		filtered_file : list
			lista con el contenido relevante para ser procesado.

		"""

		file_name_dat = self.file_transbank

		with open(file_name_dat, 'r', encoding='iso-8859-1') as input_file:
			lines = input_file.readlines()
			filtered_file = []
			num_lineas = 0
			for linea in lines:
				# print(linea)
				num_lineas += 1
				if linea.startswith('Tipo Transacc'):
					break
			filtered_file = lines[num_lineas-1:]
			
		head, tail = os.path.split(file_name_dat)
		file_name = tail.replace('.dat', '')
		# print("Head: " + head, "tail: " + tail)

		# Nuevo nombre de archivo
		new_files_csv = '{}/{}_{}.{}'.format(head, 'eq_beta', file_name, 'csv')

		# Escritura de los datos de la lista al archivo
		with open(new_files_csv, 'w') as output_file:
			for linea in filtered_file:
				output_file.write(linea)
		
		self.file_name = file_name
		self.csv_file = new_files_csv
		

	def carga_transbank(self):
		file = filedialog.askopenfilename(initialdir='/media/Datos/Documentos/archivos_proyecto_crt/2020/', filetypes=(("dat files", "*.dat"), ("All files", "*.*")))

		# La variable file guardará la ruta del archivo
		self.file_transbank = file
		#print(self.file_transbank)
		
		self.dat_files_clean_worker()

		#print(self.file_name)
		
		# Aparece en el label la ruta del archivo leído
		self.statusTbnk.configure(text=self.file_name+'.csv')


	def carga_bsale(self):
		file = filedialog.askopenfilename(initialdir='/media/Datos/Documentos/archivos_proyecto_crt/2020/',filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
		file_bsale = file

		# head: ruta del archivo
		# tail: nombre del archivo + extension
		head, tail = os.path.split(file_bsale)
		self.statusBsale.configure(text=tail)
		
		self.xlsx_bsale = pd.read_excel(file_bsale, header=11, sheet_name=None, engine='openpyxl')

		self.df_bsale = self.xlsx_bsale
		# Se filtra el archivo solo por Boleta y Factura
		self.df_bsale = self.xlsx_bsale.get('docSearchExport_cc0f2b54bf6e4b0') # HAY QUE LEER LA HOJA DINAMICAMENTE
		self.df_bsale_bol_fact = self.df_bsale[(self.df_bsale['Tipo Documento'] == 'Boleta Electrónica') | (self.df_bsale['Tipo Documento'] == 'Factura Electrónica')]


	def cargar_tbank_historico(self):
		file = filedialog.askopenfilename(initialdir='/media/Datos/Documentos/archivos_proyecto_crt/2020/',filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

		# head: ruta del archivo
		# tail: nombre del archivo + extension
		head, tail = os.path.split(file)

		print(head, tail)
	
		df_tbank = pd.read_excel(file, sheet_name=None, skiprows=1, engine='openpyxl')
		
		#print('TIPO: ' + type(df_tbank))
		# Solo se leerán las hojas que sean de crédito
		lista_credito_historico = []

		for df in df_tbank:
			# Busca solo los sheet de Credito
			if 'credito' in df.lower() or 'crédito' in df.lower():  
				#print(type(df), df, df_tbank[df])
				print(df)
				columnas = df_tbank[df].loc[26].tolist()
				# Se establece las nuevas columnas que se encuentran en la fila 26
				df_tbank[df].columns = columnas
				# Agregamos los datos de credito al diccionario
				lista_credito_historico.append(df_tbank[df].loc[26:, ['Fecha Venta', 'Código Autorización Venta', 'Nº Cuota', 'Nº Boleta']])

		# Se unen todos los sheets de credito en un dataframe
		df_credito_historico = pd.concat(lista_credito_historico)
		df_credito_historico = df_credito_historico.reset_index(drop=True)

		self.statusTbnkHist.configure(text=tail)
		self.df_credito_historico = df_credito_historico
		

	def procesamiento(self):

		if self.seleccionado.get() == 1:
			print('Hago el proceso de debito')

			# Cargar archivo tbank en un dataframe
			self.df_transbank = pd.read_csv(self.csv_file, delimiter=';')

			# self.resultado = resultado
			self.status.configure(text='En proceso...')

			# Procesamiento archivo tbank
			self.df_transbank['Nº Boleta'].fillna(" ", inplace=True)

			# Creacion columna fin_de_mes
			tmp_fecha = []
			for fecha in self.df_transbank['Fecha Venta']:
				fecha_nueva = fecha[:10]
				tmp_fecha.append(fecha_nueva)
			self.df_transbank['fecha_formateada'] = tmp_fecha
			# Convertir "Fecha Venta" a datetime
			self.df_transbank['fecha_formateada'] = pd.to_datetime(self.df_transbank['fecha_formateada'], format='%d/%m/%Y')
			# Creamos una columna para saber si 'Fecha Venta' es fin de mes
			self.df_transbank['es_fin_de_mes'] = self.df_transbank['fecha_formateada'].dt.is_month_end
			#self.df_transbank['es_fin_de_mes'][0]
			
			# Cruce de información
			boletas = []
			trucheo = []

			for indice, boleta in zip(self.df_transbank.index, self.df_transbank['Nº Boleta']):
				if boleta == ' ' or boleta == 0:  # Si 'N° boleta es vacío o tiene 0
					if not self.df_transbank['es_fin_de_mes'][indice]:  # Si la fila en la que voy es fin de mes
						bol = self.df_bsale[self.df_bsale.eq(self.df_transbank['Código Autorización Venta'][indice]).any(1)]
						if len(bol) == 1:
							bol = bol['Nº Documento'].item()
							boletas.append(bol)
						# No se encontró  
						elif len(bol) == 0:
							bol = "Apocalipsis Zombie!!"
							boletas.append(bol)
						# Hay duplicados
						else:
							bol = "REVISAR: Duplicado o +"
							boletas.append(bol)
							trucheo.append(indice)
					else: 
						bol = self.df_bsale[self.df_bsale.eq(self.df_transbank['Código Autorización Venta'][indice]).any(1)]
						if len(bol) == 1:
							bol = bol['Nº Documento'].item()
							boletas.append(bol)
						#No se encontró  
						elif len(bol) == 0:
							bol = "Revisar: fin de mes"
							boletas.append(bol)
						# Hay duplicados
						else:
							bol = "Duplicado o +"
							boletas.append(bol)
							trucheo.append(indice)
				else:
					boletas.append(boleta)

			# Creo la columna 'boletas_completas' y le asigno los resultados de las boletas que se encontraron
			self.df_transbank['boletas_completas'] = boletas
			# Reemplazo los valores de 'Nº Boleta' por los de 'boletas_completas'
			self.df_transbank['Nº Boleta'] = self.df_transbank['boletas_completas']
			# Renombrar columna
			self.df_transbank.rename(columns={'Nº Boleta':'N° Boleta'}, inplace=True)
			# Eliminar columna 'boletas_completas'
			self.df_transbank.drop(columns=['boletas_completas'], inplace=True)
			
			self.resultado = self.df_transbank
			self.status.configure(text='Todo listo')
		else:
			print('Hago el proceso de credito')
			# Cruce de información Credito con Bsale vs Tbank (csv) vs Tbank Historico

			boletas = []
			trucheo = []

			self.df_tranbank = self.csv_file
			print(self.df_tranbank)

			for indice, boleta in zip(self.df_tranbank.index, self.df_tranbank['Nº Boleta']):
				if boleta == ' ' or boleta == 0: # Si 'N° boleta es vacío
					# Si N° Cuota es 'S/C' o '1/3'
					if self.df_tranbank['Nº Cuota'][indice] == 'S/C' or self.df_tranbank['Nº Cuota'][indice] == '01/3': #verificar nombre columna
						if not self.df_tranbank['es_fin_de_mes'][indice]: # Si la fila en la que voy es fin de mes
							bol = self.df_bsale_bol_fact[self.df_bsale_bol_fact.eq(self.df_transbank['Código Autorización Venta'][indice]).any(1)]
							if len(bol) == 1:
								bol = bol['Nº Documento'].item()
								boletas.append(bol)
							#No se encontró  
							elif len(bol) == 0:
								bol = "Apocalipsis Zombie!!"
								boletas.append(bol)
							# Hay duplicados
							else:
								bol = "REVISAR: Duplicado o +"
								boletas.append(bol)
								trucheo.append(indice)
						else: # 
							bol = self.df_bsale_bol_fact[self.df_bsale_bol_fact.eq(self.df_transbank['Código Autorización Venta'][indice]).any(1)]
							if len(bol) == 1:
								bol = bol['Nº Documento'].item()
								boletas.append(bol)
							#No se encontró  
							elif len(bol) == 0:
								bol = "Revisar: fin de mes"
								boletas.append(bol)
							# Hay duplicados
							else:
								bol = "Duplicado o +"
								boletas.append(bol)
								trucheo.append(indice)
					else:
						bol = self.df_credito_historico[self.df_credito_historico.eq(self.df_transbank['Código Autorización Venta'][indice]).any(1)]
						if len(bol) == 1:
							bol = bol['Nº Documento'].item()
							boletas.append(bol)
						#No se encontró  
						elif len(bol) == 0:
							bol = "Apocalipsis Zombie!!" # -> 'cambiar mensaje'
							boletas.append(bol)
						# Hay duplicados
						else:
							bol = "REVISAR: Duplicado o +" # -> 'cambiar mensaje'
							boletas.append(bol)
							trucheo.append(indice)
				else:
					boletas.append(boleta)
			self.status.configure(text='Todo listo')
		
		self.btn_guardar = ttk.Button(self.frame, text='Guardar resultado como', command=self.guarda_archivo)        
		self.btn_guardar.grid(column=2, row=5)
		
	def guarda_archivo(self):
		
		savefile = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
															("All files", "*.*")))
		
		self.resultado.to_excel(savefile, index=False, engine='openpyxl')
		self.status.configure(text='Procesado con éxito')


def main():
    mi_app = Application()
    return 0


# Mediante el atributo __name__ tenemos acceso al nombre de un
# un módulo. Python utiliza este atributo cuando se ejecuta
# un programa para conocer si el módulo es ejecutado de forma
# independiente (en ese caso __name__ = '__main__') o es 
# importado:
if __name__ == '__main__':
    main()



# Historico de Tranbank 2020
df_tbank = pd.read_excel('/content/drive/MyDrive/proyecto_crt/datos/Transbank 2020 CRT.xlsx', sheet_name=None, skiprows=1)

# Solo se leerán las hojas que sean de crédito
lista_credito_historico = []

for df in df_tbank:
  # Busca solo los sheet de Credito
  if 'credito' in df.lower() or 'crédito' in df.lower():  
    #print(type(df), df, df_tbank[df])
    print(df)
    columnas = df_tbank[df].loc[26].tolist()
    # Se establece las nuevas columnas que se encuentran en la fila 26
    df_tbank[df].columns = columnas
    # Agregamos los datos de credito al diccionario
    lista_credito_historico.append(df_tbank[df].loc[26:, ['Fecha Venta', 'Código Autorización Venta', 'Nº Cuota', 'Nº Boleta']])

# Se unen todos los sheets de credito en un dataframe
df_credito_historico = pd.concat(lista_credito_historico)

df_credito_historico = df_credito_historico.reset_index(drop=True)

df_credito_historico['Nº Cuota'].value_counts()

