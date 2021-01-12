# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:50:40 2020

GUI para CRT


@author: Pipe San Martín
"""

# importar la librería
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog

import pandas as pd
import os


class MiVentana:
    
    def __init__(self, win):
        
        # Etiquetas
        
        self.lbl1=Label(win, text='Archivo Transbank')
        self.lbl2=Label(win, text='Archivo Bsale')
        self.lbl3=Label(win, text='Resultado')
        
        self.t1=Label(win, text='Sin archivo')
        self.t2=Label(win, text='Sin archivo')
        self.t3=Label(win, text='Aun no ha procesado')
        
        # Botones
        self.btn1 = Button(win, text='Cargar', command=self.carga_transbank)
        self.btn2 = Button(win, text='Cargar', command=self.carga_bsale)
        self.btn3 = Button(win, text='Procesar', command=self.procesamiento)
        
        # Posiciones etiquetas y entradas
        self.lbl1.place(x=50, y=50)
        self.t1.place(x=300, y=50)
        self.btn1.place(x=200, y=50)
        
        self.lbl2.place(x=50, y=100)
        self.t2.place(x=300, y=100)
        self.btn2.place(x=200, y=100)
        
        self.btn3.place(x=50, y=150)
        
        self.lbl3.place(x=50, y=200)
        self.t3.place(x=200, y=200)
    
    
    def carga_transbank(self):
        
        file = filedialog.askopenfilename(initialdir='datos/2020/',
            filetypes=(("CSV files", "*.csv"),
                       ("All files", "*.*") ))
        
        # La variable file guardará la ruta del archivo
        file_transbank = file
        # print(file_transbank)
        # # Aparece en el label la ruta del archivo leído
        self.t1.configure(text=file_transbank)
                
        # Procesamiento del archivo tbank
        df_transbank = pd.read_csv(file_transbank, delimiter=';')
        self.df_transbank = df_transbank
        
    def carga_bsale(self):
        
        file = filedialog.askopenfilename(initialdir='datos/',
            filetypes=(("Excel files", "*.xlsx"),
                       ("All files", "*.*")))
        
        file_bsale = file
        self.t2.configure(text=file_bsale)
        
        # Se filtra el archivo solo por Boleta y Factura
        self.xlsx_bsale = pd.read_excel(file_bsale, header=11, sheet_name=None, engine='openpyxl')
        self.df_bsale = self.xlsx_bsale
        
        
    def procesamiento(self):

        #self.resultado = resultado
        self.t3.configure(text='En proceso... por favor, espere')

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
        
        #print(self.df_transbank.head())
        
        self.resultado = self.df_transbank
        
        self.btn4 = Button(ventana, text='Guardar resultado como', command=self.guarda_archivo)        
        self.btn4.place(x=350, y=200)
        
    def guarda_archivo(self):
        
        savefile = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
                                                            ("All files", "*.*")))
        
        self.resultado.to_excel(savefile, index=False, engine='openpyxl')
        
        self.t3.configure(text='Procesado con éxito')


ventana = Tk()
miwin = MiVentana(ventana)
ventana.title('Boletafinder')
ventana.geometry("1000x300+10+10")
ventana.mainloop()