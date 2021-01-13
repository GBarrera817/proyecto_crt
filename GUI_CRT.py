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
		
		# Etiquetas
		self.lbl1 = ttk.Label(self.root, text='Archivo Transbank')
		self.lbl2 = ttk.Label(self.root, text='Archivo Bsale')
		self.lbl3 = ttk.Label(self.root, text='Resultado')
		self.statusTbnk = ttk.Label(self.root, text='Sin archivo')
		self.statusBsale = ttk.Label(self.root, text='Sin archivo')
		self.status = ttk.Label(self.root, text='Aun no ha procesado')

		# Botones
		self.btn1 = ttk.Button(self.root, text='Cargar', command=self.carga_transbank)
		self.btn2 = ttk.Button(self.root, text='Cargar', command=self.carga_bsale)
		self.btn3 = ttk.Button(self.root, text='Procesar', command=self.procesamiento)
		self.btn3.focus_set()
	
		# Posiciones etiquetas y entradas
		self.lbl1.place(x=50, y=50)
		#self.lbl1.pack(side=TOP)
		self.lbl2.place(x=50, y=100)
		self.lbl3.place(x=50, y=200)
		self.statusTbnk.place(x=300, y=50)
		self.statusBsale.place(x=300, y=100)
		self.status.place(x=200, y=200)
		self.btn1.place(x=200, y=50)
		self.btn2.place(x=200, y=100)
		self.btn3.place(x=500, y=150)

		self.root.mainloop()
	
		
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
		
		self.tail = tail
		self.csv_file = new_files_csv
		

	def carga_transbank(self):

		file = filedialog.askopenfilename(initialdir='datos/2020/', filetypes=(("dat files", "*.dat"), ("All files", "*.*")))

		# La variable file guardará la ruta del archivo
		self.file_transbank = file
		print(self.file_transbank)
		
		self.dat_files_clean_worker()
		
		# Aparece en el label la ruta del archivo leído
		self.statusTbnk.configure(text=self.tail)
			
	def carga_bsale(self):
		file = filedialog.askopenfilename(initialdir='datos/', filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
		file_bsale = file

		# head: ruta del archivo
		# tail: nombre del archivo + extension
		head, tail = os.path.split(file_bsale)
		self.statusBsale.configure(text=tail)
		
		# Se filtra el archivo solo por Boleta y Factura
		self.xlsx_bsale = pd.read_excel(file_bsale, header=11, sheet_name=None, engine='openpyxl')
		self.df_bsale = self.xlsx_bsale


	def procesamiento(self):

		# Cargar archivo tbank en un dataframe
		self.df_transbank = pd.read_csv(self.csv_file, delimiter=';')
		#self.df_transbank = self.df_transbank

		#self.resultado = resultado
		self.status.configure(text='En proceso...')

		# Procesamiento archivo tbank
		self.df_transbank['Nº Boleta'].fillna(" ", inplace=True)

		# Se filtra el archivo solo por Boleta y Factura
		self.df_bsale = self.xlsx_bsale.get('docSearchExport_cc0f2b54bf6e4b0')
		self.df_bsale_bol_fact = self.df_bsale[(self.df_bsale['Tipo Documento'] == 'Boleta Electrónica') | (self.df_bsale['Tipo Documento'] == 'Factura Electrónica')]
		
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
		
		self.btn4 = Button(text='Guardar resultado como', command=self.guarda_archivo)        
		self.btn4.place(x=350, y=200)
		
	def guarda_archivo(self):
		
		savefile = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
															("All files", "*.*")))
		
		self.resultado.to_excel(savefile, index=False, engine='openpyxl')
		self.status.configure(text='Procesado con éxito')


# Centrar la ventana
def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


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