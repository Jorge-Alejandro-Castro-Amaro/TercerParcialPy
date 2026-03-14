import os
'''
#***** Crear archivo *****
def crear_archivo():
    nombre = input("Nombre del Archivo: ")
    with open(nombre, "w") as archivo: #Mande llamar el archivo cuando abre el archivo y dejas de usarlo lo cierra, with cierra el archivo para quitar el espacio en la ram  
        print ("Archivo creado correctamente")
        
crear_archivo()

#***** agregar datos al archivo *****
def escribir_archivo():
    nombre = input("Nombre del archivo: ")
    texto = input("Escribe el texto a guardar: ")
    
    with open(nombre, "w") as archivo:
        archivo.write(texto)
        
    print("Texto guardado correctamente")
    
escribir_archivo()

#***** Escribir Archivo *****
def agregar_texto():
    nombre = input("Nombre del archivo: ")
    texto = input("Texto a agregar: ")
    
    with open(nombre, "a") as archivo:
        archivo.write("\n" + texto)
        
    print("Texto agregado correctamente")

agregar_texto()


#***** Leer datos del archivo *****
def leer_datos():
    #nombre = input("Nombre del Archivo")
    nombre = "prueba1.txt"
    
    try:
        with open(nombre, "r") as archivo:
            contenido = archivo.read()
            os.system("cls")
            print("\nContenido del Archivo: ")
            print(contenido)
            print("-------------------------")
            archivo.seek(0) #Donde posicionar para empezar a leer
            contenido = archivo.read()
            print(contenido)
    except FileNotFoundError:
        print("El archivo no existe")
        
leer_datos()
'''
def leer_datos():
    #nombre = input("Nombre del Archivo")
    nombre = "prueba1.txt"
    
    try:
        with open(nombre, "r") as archivo:
            contenido = archivo.readlines()
            os.system("cls")
            print("\nContenido del Archivo: ")
            print(contenido)
            
            for linea in contenido:
                print(linea.strip())
                
    except FileNotFoundError:
        print("El archivo no existe")
        
leer_datos()