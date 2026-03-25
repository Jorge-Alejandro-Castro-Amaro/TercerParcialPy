import tkinter as tk
from tkinter import messagebox
    
ventana = tk.Tk()
ventana.title("Traductor")
ventana.geometry("600x400")

diccionario = {}

def guardar_palabra():
    palabra_ing = Ingl.get()
    palabra_esp = Esp.get()
    if palabra_ing and palabra_esp:
        diccionario[palabra_ing] = palabra_esp
        messagebox.showinfo("Info", "Diccionario Actualizado")
    else:
        messagebox.showerror("Error", "Porfavor Ingresa Ambas Palabras")

def buscar_palabra():
    palabra = Palabra.get()
    if not palabra:
        messagebox.showerror("Error", "Porfavor Ingresa una palabra")
        return

#------------------------------------------------------------------------------------------
    
    if opcion.get() == 1:
        
        for ing, esp in diccionario.items():
            if esp == palabra:
                messagebox.showinfo("Traducción", f"{palabra} → {ing}")
                return
        messagebox.showwarning("Aviso", "Palabra no encontrada en el diccionario")
    
#------------------------------------------------------------------------------------------

    elif opcion.get() == 2:  # Inglés -> Español
        if palabra in diccionario:
            messagebox.showinfo("Traducción", f"{palabra} → {diccionario[palabra]}")
        else:
            messagebox.showwarning("Aviso", "Palabra no encontrada en el diccionario")
    else:
        messagebox.showerror("Error", "Selecciona una opción de traducción")
        
#Botones
opcion = tk.IntVar()

Palabra = tk.Label(ventana, text="Ingrese la palabra a Traducir:").place(x=150, y=50)
Palabra = tk.Entry()
Palabra.place(x=315, y=50)

tk.Label(ventana, text="Selecciona la opcion:").place(x=240, y=70)

tk.Radiobutton(ventana, text="Español - Ingles", variable = opcion, value=1).place(x=240, y=100)
tk.Radiobutton(ventana, text="Ingles - Español", variable = opcion, value=2).place(x=240, y=125)

tk.Button(ventana, text = "Traducir", command = buscar_palabra).place(x=265, y=160)


tk.Label(ventana, text="Agregar nueva palabra").place(x=240, y=200)

tk.Label(ventana, text = "Ingles").place(x=225, y=225)
Ingl = tk.Entry()
Ingl.place(x=280, y=225)

tk.Label(ventana, text = "Español").place(x=225, y=250)
Esp = tk.Entry()
Esp.place(x=280, y=250)

tk.Button(ventana, text = "Agregar", command = guardar_palabra).place(x=265, y=280)


ventana.mainloop()