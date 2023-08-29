from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk

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
        predictBtn = Button(predictWindow, text='Predecir registros', font=('Javanese Text', 9, 'bold'), bg='green', fg='white', width=15, height=1, bd=4)
        
        #   Boton para seleccionar el archivo de datos
        openFileBtn = Button(predictWindow, text='Abrir', font=('Javanese Text', 9, 'bold'), bg='darkblue', fg='white', width=10, height=1, bd=4, command=lambda: openFile(fileNameLabel, predictBtn))
        openFileBtn.place(x=200, y=160, anchor='n')
        

#   Confirmacion de cierre de ventana
def on_closing(window):
    if messagebox.askokcancel("Salir", "¿Desea salir de la ventana actual?"):
        if window.title() != 'ReVin':
            root.deiconify()
        window.destroy()

#   Verificar archivo seleccionado
def checkFile():
    global csvFile
    if csvFile == '':
        messagebox.showerror('Error', 'No se ha seleccionado un archivo de datos')
        return FALSE
    elif csvFile[-3:] != 'csv':
        messagebox.showerror('Error', 'El archivo seleccionado no es un archivo .csv')
        return FALSE
    return TRUE

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
    csvFile = filedialog.askopenfilename()
    if checkFile():        
        label.config(text=getFileName())
        label.place(x = 400, y = 170, anchor='n')
        predictBtn.place(x=300, y=230, anchor='n')

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