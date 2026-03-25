'''
Manejo de archivos de texto
Apertura de archivos
    open("archivo.txt", "r")
    
Modos principales:

Modo descripcion
r    Leer
w    Escribir (Sobreescribir)
a    Agregar
x    Crear archivo

***** Lectura de Archivos *****
    *archivo.read()
    *archivo.readline()
    *archivo.readlines()
    
***** Escritura de Archivos *****
    *archivo.write("Texto a Escribir")
    *archivo.writelines(["Linea 1\n", "Linea2\n"]) \n salto de linea
'''

def crear_archivo():
    nombre = input("Nombre del Archivo: ")
    with open(nombre, "w") as archivo: #Mande llamar el archivo cuando abre el archivo y dejas de usarlo lo cierra, with cierra el archivo para quitar el espacio en la ram  
        print ("Archivo creado correctamente")
        
crear_archivo()