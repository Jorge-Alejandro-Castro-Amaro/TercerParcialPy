import customtkinter as ctk
from tkinter import messagebox, simpledialog
import tkinter as tk
from PIL import Image
import os

# Configuración de apariencia
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

class MaquinaRefrescos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Máquina de Refrescos ITI705")
        self.geometry("450x650")

        # --- VARIABLES DE ESTADO ---
        self.precio_global = 5.0
        self.saldo_ingresado = 0.0
        self.inventario = {
            "Coca": 5, "Fanta": 5, "Sprite": 5,
            "Aga": 5, "Jarrito": 5, "Mundet": 5
        }
        self.monedas_aceptadas = [0.5, 1.0, 2.0, 5.0, 10.0]

        # --- INTERFAZ ---
        self.configurar_menu()
        self.setup_ui()
        self.actualizar_estado_opciones()

    def configurar_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        menu_surtir = tk.Menu(self.menubar, tearoff=0)
        for refresco in self.inventario.keys():
            menu_surtir.add_command(label=refresco, command=lambda r=refresco: self.abrir_ventana_surtir(r))
        self.menubar.add_cascade(label="Surtir", menu=menu_surtir)

        self.menubar.add_command(label="Cambiar Precio", command=self.abrir_ventana_precio)

    def setup_ui(self):
        # Sección Superior: Dinero
        ctk.CTkLabel(self, text="0.5, 1, 2, 5, 10", font=("Arial", 14, "bold")).place(x=20, y=20)
        self.ent_dinero = ctk.CTkEntry(self, width=100, placeholder_text="Monto")
        self.ent_dinero.place(x=150, y=20)
        
        self.lbl_saldo_display = ctk.CTkLabel(self, text="$ 0.0", font=("Arial", 16, "bold"), text_color="blue")
        self.lbl_saldo_display.place(x=270, y=20)

        self.btn_ingresar = ctk.CTkButton(self, text="Ingresar", width=100, command=self.validar_ingreso)
        self.btn_ingresar.place(x=40, y=60)

        self.lbl_precio_actual = ctk.CTkLabel(self, text=f"Precio: $ {self.precio_global}", font=("Arial", 14, "bold"))
        self.lbl_precio_actual.place(x=230, y=80)

        self.lbl_cambio = ctk.CTkLabel(self, text="Cambio: $ 0.0", font=("Arial", 14, "bold"), text_color="green")
        self.lbl_cambio.place(x=100, y=110)

        # --- SECCIÓN CENTRAL: REFRESCOS ---
        ctk.CTkLabel(self, text="Refrescos", font=("Arial", 16, "bold")).place(x=20, y=140)
        
        self.var_seleccion = ctk.StringVar(value="")
        self.radio_buttons = {}
        
        y_pos = 180
        for nombre in self.inventario.keys():
            rb = ctk.CTkRadioButton(self, text=f"{nombre}   {self.inventario[nombre]}", 
                                     variable=self.var_seleccion, value=nombre,
                                     command=self.cargar_imagen_inteligente)
            rb.place(x=40, y=y_pos)
            self.radio_buttons[nombre] = rb
            y_pos += 40

        # Visualizador de Imagen
        self.lbl_img = ctk.CTkLabel(self, text="Imagen\nRefresco", fg_color="gray90", 
                                     width=160, height=220, corner_radius=10)
        self.lbl_img.place(x=220, y=180)

        # Botón para comprar
        self.btn_tomar = ctk.CTkButton(self, text="Tomar Refresco", state="disabled", 
                                       fg_color="#1e7c1e", command=self.procesar_venta)
        self.btn_tomar.place(x=100, y=520)

    def cargar_imagen_inteligente(self):
        nombre = self.var_seleccion.get().lower()
        extensiones = [".png", ".jpg", ".jpeg"]
        ruta_final = None

        for ext in extensiones:
            if os.path.exists(f"{nombre}{ext}"):
                ruta_final = f"{nombre}{ext}"
                break

        if ruta_final:
            try:
                img_pil = Image.open(ruta_final)
                foto = ctk.CTkImage(light_image=img_pil, size=(140, 200))
                self.lbl_img.configure(image=foto, text="")
            except:
                self.lbl_img.configure(image=None, text="Error al abrir\nla imagen")
        else:
            self.lbl_img.configure(image=None, text=f"No se encontró\n{nombre}.png/jpg")
        
        self.actualizar_estado_opciones()

    def validar_ingreso(self):
        try:
            monto = float(self.ent_dinero.get())
            if monto in self.monedas_aceptadas:
                self.saldo_ingresado += monto
                self.lbl_saldo_display.configure(text=f"$ {self.saldo_ingresado}")
                self.ent_dinero.delete(0, 'end')
                self.actualizar_estado_opciones()
            else:
                messagebox.showwarning("Moneda No Válida", f"Solo se aceptan: {self.monedas_aceptadas}")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número")

    def actualizar_estado_opciones(self):
        puedo_comprar = self.saldo_ingresado >= self.precio_global
        estado = "normal" if puedo_comprar else "disabled"
        
        for nombre, rb in self.radio_buttons.items():
            if self.inventario[nombre] <= 0:
                rb.configure(state="disabled", text=f"{nombre} (AGOTADO)")
            else:
                rb.configure(state=estado, text=f"{nombre}   {self.inventario[nombre]}")
        
        if puedo_comprar and self.var_seleccion.get():
            self.btn_tomar.configure(state="normal")
        else:
            self.btn_tomar.configure(state="disabled")

    def procesar_venta(self):
        seleccion = self.var_seleccion.get()
        if not seleccion: return

        cambio = self.saldo_ingresado - self.precio_global
        self.inventario[seleccion] -= 1
        
        messagebox.showinfo("Venta Exitosa", f"Entregando {seleccion}.\nSu cambio es: ${cambio:.2f}")
        
        # --- RESET DE VALORES (SIN QUITAR LA IMAGEN) ---
        self.saldo_ingresado = 0.0
        self.lbl_saldo_display.configure(text="$ 0.0")
        self.lbl_cambio.configure(text=f"Cambio: $ {cambio:.2f}")
        
        # Deseleccionamos el radio button para obligar a elegir de nuevo
        self.var_seleccion.set("") 
        
        # Actualizamos textos de inventario y desactivamos botones
        self.actualizar_estado_opciones()

    def abrir_ventana_surtir(self, producto):
        cantidad = simpledialog.askinteger("Surtir", f"¿Cuántos {producto} agregar?", minvalue=0)
        if cantidad is not None:
            self.inventario[producto] += cantidad
            self.actualizar_estado_opciones()

    def abrir_ventana_precio(self):
        nuevo = simpledialog.askfloat("Configuración", "Nuevo precio:", minvalue=0.1)
        if nuevo is not None:
            self.precio_global = nuevo
            self.lbl_precio_actual.configure(text=f"Precio: $ {self.precio_global}")
            self.actualizar_estado_opciones()

if __name__ == "__main__":
    app = MaquinaRefrescos()
    app.mainloop()