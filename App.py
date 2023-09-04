from fileinput import fileno
from inspect import getfile
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Tk, Label, Button, Frame,  messagebox, filedialog, ttk, Scrollbar, VERTICAL, HORIZONTAL
from PIL import ImageTk
import pandas as pd
from predict import doPredict

# VARIABLES GLOBALES
csvFile = ''
predictWindow = None

# FUNCIONES
#   Abrir la ventana de predicciones
def predictWindow():
    global predictWindow
    
    try:
        if predictWindow.state() == 'normal': predictWindow.focus()
    except:
        root.iconify()
        predictWindow = Toplevel(root)
        predictWindow.title('ReVin - Predicciones')
        predictWindow.geometry('600x300')
        predictWindow.resizable(0, 0)
        predictWindow.config(bg='lightblue')
        predictWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(predictWindow))
        predictWindow.iconbitmap('Images/appWindowIcon.ico')
        
        # CREACION DE ELEMENTOS - VENTANA PREDICCIONES
        #   Imagen logo de la aplicacion
        appLabel_pred = Label(predictWindow, image=appImage, bg='lightblue')
        appLabel_pred.place(x=300, y=30, anchor='n')
        
        #   Texto de instrucciones de la ventana
        instText = Label(predictWindow, text='Seleccione el archivo .csv de registros a predecir', font=('Javanese Text', 11), bg='lightblue')
        instText.place(x=300, y=115, anchor='n')
        
        #   Etiqueta con el nombre del archivo seleccionado
        fileNameLabel = Label(predictWindow, font=('Javanese Text', 9), bg='#D1FFBD')
        
        #   Boton para iniciar la prediccion
        predictBtn = Button(predictWindow, text='Predecir registros', font=('Javanese Text', 9, 'bold'), bg='green', fg='white', width=15, height=1, bd=4, command=resWindow)
        
        #   Boton para seleccionar el archivo de datos
        openFileBtn = Button(predictWindow, text='Abrir', font=('Javanese Text', 9, 'bold'), bg='darkblue', fg='white', width=10, height=1, bd=4, command=lambda: openFile(fileNameLabel, predictBtn))
        openFileBtn.place(x=200, y=160, anchor='n')
        
#   Ventana de Resultados
def resWindow():
    global resWindow

    try:
        if resWindow.state() == 'normal': resWindow.focus()
    except:
        root.iconify()
        resWindow = Toplevel(root)
        resWindow.title('ReVin - Resultados')
        resWindow.geometry('600x400')
        resWindow.config(bg='lightblue')
        resWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(resWindow))
        resWindow.iconbitmap('Images/appWindowIcon.ico')
        
        # CREACION DE ELEMENTOS - VENTANA RESULTADOS
        # CONFIGURACIONES
        resWindow.columnconfigure(0, weight = 25)
        resWindow.rowconfigure(0, weight= 25)
        resWindow.columnconfigure(0, weight = 1)
        resWindow.rowconfigure(1, weight= 1)
        
        # ELEMENTOS
        frame1 = Frame(resWindow, bg='lightblue')
        frame1.grid(column=0,row=0,sticky='nsew')
        frame2 = Frame(resWindow, bg='lightblue')
        frame2.grid(column=0,row=1,sticky='nsew')
        
        frame1.columnconfigure(0, weight = 1)
        frame1.rowconfigure(0, weight= 1)
        
        frame2.columnconfigure(0, weight = 1)
        frame2.rowconfigure(0, weight= 1)
        frame2.columnconfigure(1, weight = 1)
        frame2.rowconfigure(0, weight= 1)
        
        frame2.columnconfigure(2, weight = 1)
        frame2.rowconfigure(0, weight= 1)
        
        frame2.columnconfigure(3, weight = 2)
        frame2.rowconfigure(0, weight= 1)

        def abrir_archivo():
            archivo = './predicted.csv'
            # archivo = filedialog.askopenfilename(initialdir ='/', 
			# 								title='Selecione archivo', 
			# 								filetype=((' files', '*.csv*'),('All files', '*.*')))
            indica['text'] = archivo

        def datos_excel():
            
            datos_obtenidos = indica['text']
            try:
                archivocsv = r'{}'.format(datos_obtenidos)
                df = pd.read_csv(archivocsv)

            except ValueError:
                messagebox.showerror('Informacion','Formato incorrecto')
                return None

            except FileNotFoundError:
                messagebox.showerror('Informacion','El archivo está \n malogrado')
                return None

            Limpiar()

            tabla['column'] = list(df.columns)
            tabla['show'] = "headings"

            for columna in tabla['column']:
                tabla.heading(columna, text= columna)

            df_fila = df.to_numpy().tolist()
            for fila in df_fila:
                tabla.insert('','end',values =fila)

        def Limpiar():
            tabla.delete(*tabla.get_children())

        tabla = ttk.Treeview(frame1 , height=10)
        tabla.grid(column=0, row=0, sticky='nsew')
        
        ladox = Scrollbar(frame1, orient = HORIZONTAL, command= tabla.xview)
        ladox.grid(column=0, row = 1, sticky='ew') 
        
        ladoy = Scrollbar(frame1, orient =VERTICAL, command = tabla.yview)
        ladoy.grid(column = 1, row = 0, sticky='ns')
        
        tabla.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
        
        estilo = ttk.Style(frame1)
        estilo.theme_use('clam') #  ('clam', 'alt', 'default', 'classic')
        estilo.configure(".",font= ('Arial', 14), foreground='black')
        estilo.configure("Treeview", font= ('Javanese Text', 12), foreground='black',  background='white')
        estilo.map('Treeview',background=[('selected', 'green2')], foreground=[('selected','black')] )
        
        
        boton1 = Button(frame2, text= 'Abrir', bg='green2', command= abrir_archivo)
        boton1.grid(column = 0, row = 0, sticky='nsew', padx=10, pady=10)
        
        boton2 = Button(frame2, text= 'Mostrar', bg='springgreen', command= datos_excel)
        boton2.grid(column = 1, row = 0, sticky='nsew', padx=10, pady=10)
        
        #boton3 = Button(frame2, text= 'Limpiar', bg='red', command= Limpiar)
        #boton3.grid(column = 2, row = 0, sticky='nsew', padx=10, pady=10)
        
        
        indica = Label(frame2, fg= 'white', bg='lightblue', text= 'Ubicación del archivo', font= ('Javanese Text',10,'bold') )
        indica.grid(column=3, row = 0)



#   Confirmacion de cierre de ventana
def on_closing(window):
    if messagebox.askokcancel("Salir", "¿Desea salir de la ventana actual?"):
        if window.title() != 'ReVin':
            root.deiconify()
        window.destroy()

#   Obtener el nombre del archivo seleccionado
def getFileName():
    global csvFile
    fileName = ''
    for i in reversed(range(len(csvFile))):
        if csvFile[i] == '/':
            break
        else:
            fileName = csvFile[i] + fileName
    return fileName

#   Obtener un archivo de la computadora
def openFile(label, predictBtn):
    global csvFile 
    try:
        predictBtn.place_forget()
        label.config(text='')
        label.place_forget()
    except:
        pass
    csvFile = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    data_to_predict = pd.read_csv(csvFile, sep=';')
      
    label.config(text=getFileName())
    label.place(x = 400, y = 170, anchor='n')
    predictBtn.place(x=300, y=230, anchor='n')

    doPredict(data_to_predict)

# CREACION DE ELEMENTOS - VENTANA PRINCIPAL
#   Ventana principal
root = Tk()
root.title('ReVin')
root.geometry('600x300')
root.resizable(0, 0)
root.config(bg='lightblue')
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
root.iconbitmap('Images/appWindowIcon.ico')

#   Imagen del escudo del Ecuador
ecImage = ImageTk.PhotoImage(file='Images/Ecuador.png')
ecLabel = Label(root, image=ecImage, bg='lightblue')
ecLabel.place(x=60, y=10, anchor='nw')

#    Imagen logo del INEC
inecImage = ImageTk.PhotoImage(file='Images/INEC.png')
inecLabel = Label(root, image=inecImage, bg='lightblue')
inecLabel.place(x=450, y=40, anchor='nw')

#    Imagen logo de la aplicacion
appImage = ImageTk.PhotoImage(file='Images/appIcon.png')
appLabel = Label(root, image=appImage, bg='lightblue')
appLabel.place(x=300, y=50, anchor='n')

#   Titulo app y descripcion
appTitle = Label(root, text='ReVin', font=('Javanese Text', 25, 'bold'), bg='lightblue', fg='darkblue')
appTitle.place(x=300, y=120, anchor='n')
appDescrip = Label(root, text='Sistema predictor de selectividad para participación de reos en ejes de vinculación', font=('Javanese Text', 11), bg='lightblue')
appDescrip.place(x=300, y=170, anchor='n')

#   Boton para iniciar la aplicacion
startBtn = Button(root, text='Iniciar', font=('Javanese Text', 9, 'bold'), bg='darkblue', fg='white', width=10, height=1, bd=4, command=predictWindow)
startBtn.place(x=300, y=220, anchor='n')

root.mainloop()