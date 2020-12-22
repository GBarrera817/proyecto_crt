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
        
        # with open(file_transbank, 'r', encoding='iso-8859-1') as input_file:
        #     lines = input_file.readlines()
        #     print(lines)
        #     filtered_file = []
        #     num_lineas = 0
        #     for linea in lines:
        #         #print(linea)
        #         num_lineas += 1
        #         if linea.startswith('Tipo Transacc'):
        #             break
        #     filtered_file = lines[num_lineas-1:]
        #print(filtered_file)
            
        # Transformación a csv    
        
        #head, tail = os.path.split(file_transbank)
        #print(head)
        #print(tail)
        #tail = tail.replace('.dat', '')

        #new_files_csv = '{}/{}_{}.{}'.format(head, '1eq_beta', file_transbank, 'csv')
        # with open(file_transbank, 'w') as output_file:
        #     for linea in filtered_file:
        #         output_file.write(linea)
        # print(output_file)
                
        # Procesamiento del archivo tbank
        df_transbank = pd.read_csv(file_transbank, delimiter=';')
        df_transbank['Nº Boleta'].fillna(" ", inplace=True)
        
        self.df_transbank = df_transbank
        
    def carga_bsale(self):
        
        file = filedialog.askopenfilename(initialdir='datos/',
            filetypes=(("Excel files", "*.xlsx"),
                       ("All files", "*.*")))
        
        file_bsale = file
        self.t2.configure(text=file_bsale)
        
        # Se filtra el archivo solo por Boleta y Factura
        xlsx_bsale = pd.read_excel(file_bsale, header=11, sheet_name=None, engine='openpyxl')
        df_bsale = xlsx_bsale.get('docSearchExport_cc0f2b54bf6e4b0')
        df_bsale_bol_fact = df_bsale[(df_bsale['Tipo Documento'] == 'Boleta Electrónica') | (df_bsale['Tipo Documento'] == 'Factura Electrónica')]
        #print(df_bsale_bol_fact)
        
        self.df_bsale = df_bsale_bol_fact
        
        
    def procesamiento(self):
        
        #resultado = pd.read_csv(self.file_transbank, encoding='latin-1')
        # df
        #self.resultado = resultado
        self.t3.configure(text='En proceso')
        
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
            if boleta == ' ' or boleta == '0000000000': # Si 'N° boleta es vacío o tiene 0000000000
                if not self.df_transbank['es_fin_de_mes'][indice]: # Si la fila en la que voy es fin de mes
                    bol = self.df_bsale[self.df_bsale.eq(self.df_transbank['Código Autorización Venta'][indice]).any(1)]
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

        self.df_transbank['boletas_completas'] = boletas
        # Renombrar columna
        self.df_transbank.rename(columns={'boletas_completas':'N° Boleta'}, inplace=True)
        # Eliminar columna 'Nº Boleta'
        self.df_transbank.drop(columns=['Nº Boleta'])
        
        # Reemplazarla la columna eliminada por 'N° Boleta'

        self.df_transbank = self.df_transbank.reindex(columns=['Tipo Transacción', 'Fecha Venta', 'Tipo Tarjeta', 'Identificador',
            'Tipo Cuota', 'Monto Original Venta', 'Código Autorización Venta',
            'Nº Cuota', 'Monto Para Abono', 'Comisión e IVA Comisión',
            'Comisión Adicional e IVA Comisión Adicional', 'N° Boleta',
            'Monto Anulación', 'Devolución Comisión e IVA Comisión',
            'Devolución Comisión Adicional e IVA Comisión', 'Monto Retención',
            'Período de Cobro', 'Motivo', 'Detalle de cobros u observación',
            'Monto', 'IVA', 'Fecha Abono', 'Cuenta de Abono', 'Local',
            'Unnamed: 24', 'fecha_formateada', 'es_fin_de_mes'])
        
        #print(self.df_transbank.head())
        
        self.resultado = self.df_transbank
        
        self.btn4 = Button(ventana, text='Guardar resultado como', command=self.guarda_archivo)        
        self.btn4.place(x=350, y=200)
        
    def guarda_archivo(self):
        
        savefile = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
                                                            ("All files", "*.*")))
        
        self.resultado.to_excel(savefile, index=False, engine='openpyxl')
        
        self.t3.configure(text='Procesado con éxito')

ventana=Tk()
miwin=MiVentana(ventana)
ventana.title('Boletafinder')
ventana.geometry("800x300+10+10")
ventana.mainloop()