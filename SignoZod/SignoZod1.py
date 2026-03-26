import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import date

ventana = tk.Tk()
ventana.title("Signo Zodiacal Chino")
ventana.geometry("600x600")

signos_chinos = {
    "Rata": "rata.jpeg",
    "Buey": "buey.jpeg",
    "Tigre": "tigre.jpeg",
    "Conejo": "conejo.jpeg",
    "Dragón": "dragon.jpeg",
    "Serpiente": "serpiente.jpeg",
    "Caballo": "caballo.jpeg",
    "Cabra": "cabra.jpeg",
    "Mono": "mono.jpeg",
    "Gallo": "gallo.jpeg",
    "Perro": "perro.jpeg",
    "Cerdo": "cerdo.jpeg"
}

def signo_chino():
    try:
        dia = int(Dia.get())
        mes = int(Mes.get())
        año = int(Año.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa números válidos en día, mes y año")
        return

    # Cálculo del signo chino
    animales = list(signos_chinos.keys())
    indice = (año - 1900) % 12
    signo = animales[indice]

    nombre = Nombre.get()
    apellido1 = ApellidoP.get()
    apellido2 = ApellidoM.get()

    sexo_valor = opcion.get()
    if sexo_valor == 1:
        sexo = "Masculino"
    elif sexo_valor == 2:
        sexo = "Femenino"
    else:
        sexo = "No especificado"

    # Calcular edad
    hoy = date.today()
    edad = hoy.year - año - ((hoy.month, hoy.day) < (mes, dia))

    texto = (
        f"Nombre: {nombre} {apellido1} {apellido2}\n"
        f"Fecha de nacimiento: {dia}/{mes}/{año}\n"
        f"Sexo: {sexo}\n"
        f"Edad: {edad} años\n"
        f"Signo Chino: {signo}"
    )
    lbl_texto.config(text=texto)

    # Mostrar imagen en la ventana
    img_path = signos_chinos[signo]
    try:
        img = Image.open(img_path)
        img = img.resize((120, 120))
        img_tk = ImageTk.PhotoImage(img)
        lbl_img.config(image=img_tk)
        lbl_img.image = img_tk
    except:
        lbl_img.config(text="Imagen no encontrada")

# Etiquetas y entradas
tk.Label(ventana, text="Datos Personales").place(x=250, y=90)

tk.Label(ventana, text="Nombre").place(x=215, y=125)
Nombre = tk.Entry(ventana)
Nombre.place(x=280, y=125)

tk.Label(ventana, text="A.Paterno").place(x=215, y=150)
ApellidoP = tk.Entry(ventana)
ApellidoP.place(x=280, y=150)

tk.Label(ventana, text="A.Materno").place(x=215, y=175)
ApellidoM = tk.Entry(ventana)
ApellidoM.place(x=280, y=175)

tk.Label(ventana, text="Día").place(x=150, y=210)
Dia = tk.Entry(ventana)
Dia.place(x=100, y=230)

tk.Label(ventana, text="Mes").place(x=300, y=210)
Mes = tk.Entry(ventana)
Mes.place(x=250, y=230)

tk.Label(ventana, text="Año").place(x=450, y=210)
Año = tk.Entry(ventana)
Año.place(x=400, y=230)

# Género
opcion = tk.IntVar()
tk.Label(ventana, text="Sexo").place(x=225, y=265)
tk.Radiobutton(ventana, text="Masculino", variable=opcion, value=1).place(x=225, y=280)
tk.Radiobutton(ventana, text="Femenino", variable=opcion, value=2).place(x=225, y=300)

# Botón
tk.Button(ventana, text="Imprimir", command=signo_chino).place(x=290, y=350)

# Labels para mostrar resultado
lbl_texto = tk.Label(ventana, text="", font=("Arial", 12))
lbl_texto.place(x=150, y=380)

lbl_img = tk.Label(ventana)
lbl_img.place(x=400, y=420)

ventana.mainloop()