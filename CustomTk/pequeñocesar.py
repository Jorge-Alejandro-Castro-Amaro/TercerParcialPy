import customtkinter as ctk
from tkinter import ttk, messagebox
import os
from datetime import datetime

# Configuración de apariencia
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class AppPizzeriaModerna(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Pedidos - Pizzería 'Pequeño Cesar'")
        self.geometry("1100x750")
        
        # Archivos para datos
        self.archivo_temporal = "pedido_actual.csv"
        self.archivo_historico = "ventas_historicas.csv"
        self.inicializar_archivos()

        # --- PRECIOS ---
        self.precios_base = {"Chica": 40, "Mediana": 80, "Grande": 120}
        self.precios_ingredientes = {"Jamón": 10, "Piña": 10, "Champiñones": 10}

        self.configurar_estilos_treeview()
        self.setup_ui()
        self.actualizar_ventas_historicas()

    def inicializar_archivos(self):
        # Limpiar pedido pendiente al iniciar
        if os.path.exists(self.archivo_temporal):
            os.remove(self.archivo_temporal)
        # Crear histórico si no existe
        if not os.path.exists(self.archivo_historico):
            with open(self.archivo_historico, "w", encoding='utf-8') as f:
                f.write("Cliente|Fecha|Total\n")

    def configurar_estilos_treeview(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", 
                             background="#2b2b2b", 
                             foreground="white", 
                             fieldbackground="#2b2b2b", 
                             rowheight=35, 
                             font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        self.style.map("Treeview", background=[("selected", "#1f538d")])
        
    def setup_ui(self):
        self.lbl_titulo = ctk.CTkLabel(self, text="REGISTRO DE PEDIDOS", font=("Segoe UI", 24, "bold"))
        self.lbl_titulo.pack(pady=15)

        self.main_frame = ctk.CTkScrollableFrame(self, width=1050, height=650)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # --- SECCIÓN 1: DATOS CLIENTE ---
        self.frame_cliente = ctk.CTkFrame(self.main_frame)
        self.frame_cliente.pack(pady=10, padx=15, fill="x")

        ctk.CTkLabel(self.frame_cliente, text="Datos del Cliente", font=("Segoe UI", 14, "bold")).pack(pady=5, padx=15, anchor="w")

        self.grid_cliente = ctk.CTkFrame(self.frame_cliente, fg_color="transparent")
        self.grid_cliente.pack(pady=5, padx=15, fill="x")
        
        self.ent_nombre = ctk.CTkEntry(self.grid_cliente, placeholder_text="Nombre", width=250)
        self.ent_nombre.grid(row=0, column=0, padx=5, pady=10)
        
        self.ent_direccion = ctk.CTkEntry(self.grid_cliente, placeholder_text="Dirección", width=250)
        self.ent_direccion.grid(row=0, column=1, padx=5, pady=10)

        self.ent_telefono = ctk.CTkEntry(self.grid_cliente, placeholder_text="Teléfono", width=150)
        self.ent_telefono.grid(row=0, column=2, padx=5, pady=10)

        self.ent_fecha = ctk.CTkEntry(self.grid_cliente, placeholder_text="Fecha", width=120)
        self.ent_fecha.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.ent_fecha.grid(row=0, column=3, padx=5, pady=10)

        # --- SECCIÓN 2: PIZZA ---
        self.frame_pizza = ctk.CTkFrame(self.main_frame)
        self.frame_pizza.pack(pady=10, padx=15, fill="x")

        # Tamaños
        self.frame_tams = ctk.CTkFrame(self.frame_pizza, fg_color="transparent")
        self.frame_tams.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(self.frame_tams, text="Tamaño:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        
        self.var_tamano = ctk.StringVar(value="Chica")
        for tam, precio in self.precios_base.items():
            rb = ctk.CTkRadioButton(self.frame_tams, text=f"{tam} ${precio}", variable=self.var_tamano, value=tam)
            rb.pack(anchor="w", pady=2)

        # Ingredientes
        self.frame_ings = ctk.CTkFrame(self.frame_pizza, fg_color="transparent")
        self.frame_ings.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(self.frame_ings, text="Ingredientes (+$10 c/u):", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        
        self.check_vars = {}
        for ing in self.precios_ingredientes.keys():
            self.check_vars[ing] = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.frame_ings, text=ing, variable=self.check_vars[ing])
            cb.pack(anchor="w", pady=2)

        # Cantidad y Botón Agregar
        self.frame_add = ctk.CTkFrame(self.frame_pizza, fg_color="transparent")
        self.frame_add.pack(side="right", padx=20)
        
        ctk.CTkLabel(self.frame_add, text="Num. Pizzas:").pack()
        self.ent_cant = ctk.CTkEntry(self.frame_add, width=60)
        self.ent_cant.insert(0, "1")
        self.ent_cant.pack(pady=5)
        
        self.btn_agregar = ctk.CTkButton(self.frame_add, text="Agregar", command=self.agregar_pizza)
        self.btn_agregar.pack(pady=5)

        # --- SECCIÓN 3: TABLA Y HISTÓRICO ---
        self.frame_inferior = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_inferior.pack(pady=10, padx=15, fill="both", expand=True)

        # Tabla
        self.tabla = ttk.Treeview(self.frame_inferior, columns=("T", "I", "C", "S"), show="headings", height=8)
        self.tabla.heading("T", text="Tamaño")
        self.tabla.heading("I", text="Ingredientes")
        self.tabla.heading("C", text="Cant.")
        self.tabla.heading("S", text="Subtotal")
        self.tabla.column("T", width=100)
        self.tabla.column("I", width=250)
        self.tabla.column("C", width=80, anchor="center")
        self.tabla.column("S", width=100, anchor="e")
        self.tabla.pack(side="left", fill="both", expand=True)

        # Panel Ventas del Día
        self.frame_ventas = ctk.CTkFrame(self.frame_inferior, width=300, fg_color="#1a1a1a")
        self.frame_ventas.pack(side="right", padx=(15, 0), fill="both")
        
        ctk.CTkLabel(self.frame_ventas, text="Ventas del día", font=("Segoe UI", 14, "bold"), text_color="orange").pack(pady=10)
        
        self.txt_ventas = ctk.CTkTextbox(self.frame_ventas, width=250, height=200, border_width=0, fg_color="#1a1a1a")
        self.txt_ventas.pack(padx=10, pady=5)
        self.txt_ventas.configure(state="disabled")

        self.lbl_total_dia = ctk.CTkLabel(self.frame_ventas, text="Total: $0.00", font=("Segoe UI", 14, "bold"), text_color="green")
        self.lbl_total_dia.pack(pady=10)

        # Botones finales
        self.frame_btns = ctk.CTkFrame(self)
        self.frame_btns.pack(fill="x", padx=35, pady=10)
        
        ctk.CTkButton(self.frame_btns, text="Quitar Pizza", fg_color="#7c1e1e", command=self.quitar_pizza).pack(side="left", padx=10)
        ctk.CTkButton(self.frame_btns, text="Terminar Pedido", fg_color="#1e7c1e", command=self.terminar_pedido).pack(side="right", padx=10)

    # --- LÓGICA ---
    def agregar_pizza(self):
        tam = self.var_tamano.get()
        ings = [ing for ing, var in self.check_vars.items() if var.get()]
        ings_str = ", ".join(ings) if ings else "Sencilla"
        
        try:
            cant = int(self.ent_cant.get())
            subtotal = (self.precios_base[tam] + (len(ings) * 10)) * cant
            
            with open(self.archivo_temporal, "a", encoding='utf-8') as f:
                f.write(f"{tam}|{ings_str}|{cant}|{subtotal}\n")
            
            self.actualizar_tabla()
        except:
            messagebox.showerror("Error", "Cantidad inválida")

    def actualizar_tabla(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        if os.path.exists(self.archivo_temporal):
            with open(self.archivo_temporal, "r", encoding='utf-8') as f:
                for line in f:
                    self.tabla.insert("", "end", values=line.strip().split("|"))

    def quitar_pizza(self):
        sel = self.tabla.selection()
        if not sel: return
        val = self.tabla.item(sel)['values']
        lineas = []
        with open(self.archivo_temporal, "r", encoding='utf-8') as f:
            for l in f:
                if f"{val[0]}|{val[1]}|{val[2]}|{val[3]}" not in l: lineas.append(l)
        with open(self.archivo_temporal, "w", encoding='utf-8') as f:
            f.writelines(lineas)
        self.actualizar_tabla()

    def terminar_pedido(self):
        nombre = self.ent_nombre.get()
        direccion = self.ent_direccion.get()
        telefono = self.ent_telefono.get()
        fecha = self.ent_fecha.get()

        if not nombre or not os.path.exists(self.archivo_temporal):
            messagebox.showwarning("Error", "Faltan datos del cliente o no hay pizzas en el pedido")
            return
        
        # 1. Calcular total y leer pizzas para el ticket
        lineas_ticket = []
        total = 0
        with open(self.archivo_temporal, "r", encoding='utf-8') as f:
            for l in f:
                datos = l.strip().split("|")
                # Estructura: Tamaño | Ingredientes | Cant | Subtotal
                lineas_ticket.append(f"{datos[2]}x {datos[0]} ({datos[1]}) - ${datos[3]}")
                total += float(datos[3])
            
        # 2. Generar el archivo de texto (.txt) como ticket
        nombre_archivo_txt = f"Ticket_{nombre.replace(' ', '_')}_{fecha}.txt"
        with open(nombre_archivo_txt, "w", encoding='utf-8') as f_txt:
            f_txt.write("==========================================\n")
            f_txt.write("         PIZZERÍA 'PEQUEÑO CESAR'         \n")
            f_txt.write("==========================================\n")
            f_txt.write(f"Fecha: {fecha}\n")
            f_txt.write(f"Cliente: {nombre}\n")
            f_txt.write(f"Dirección: {direccion}\n")
            f_txt.write(f"Teléfono: {telefono}\n")
            f_txt.write("------------------------------------------\n")
            f_txt.write("DETALLE DEL PEDIDO:\n")
            for item in lineas_ticket:
                f_txt.write(f"- {item}\n")
            f_txt.write("------------------------------------------\n")
            f_txt.write(f"TOTAL A PAGAR: ${total:.2f}\n")
            f_txt.write("==========================================\n")
            f_txt.write("      ¡Gracias por su preferencia!        \n")

        # 3. Guardar en el histórico (CSV) para las estadísticas del programa
        with open(self.archivo_historico, "a", encoding='utf-8') as f_hist:
            f_hist.write(f"{nombre}|{fecha}|{total}\n")
            
        # 4. Limpiar UI y archivos temporales
        os.remove(self.archivo_temporal)
        self.actualizar_tabla()
        self.actualizar_ventas_historicas()
        
        messagebox.showinfo("Éxito", f"Pedido registrado y Ticket generado:\n{nombre_archivo_txt}")

    def actualizar_ventas_historicas(self):
        self.txt_ventas.configure(state="normal")
        self.txt_ventas.delete("1.0", "end")
        total_d = 0
        with open(self.archivo_historico, "r", encoding='utf-8') as f:
            next(f) # Saltar encabezado
            for l in f:
                d = l.strip().split("|")
                self.txt_ventas.insert("end", f"{d[0]}: ${d[2]}\n")
                total_d += float(d[2])
        self.txt_ventas.configure(state="disabled")
        self.lbl_total_dia.configure(text=f"Total: ${total_d:.2f}")

if __name__ == "__main__":
    app = AppPizzeriaModerna()
    app.mainloop()