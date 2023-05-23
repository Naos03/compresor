import os

def compare_files(archivo1, archivo2):
    tamano_archivo1 = os.path.getsize(archivo1)
    tamano_archivo2 = os.path.getsize(archivo2)

    if tamano_archivo1 < tamano_archivo2:
        print(f"El archivo '{archivo1}' es más pequeño que el archivo '{archivo2}'")
    elif tamano_archivo1 > tamano_archivo2:
        print(f"El archivo '{archivo1}' es más grande que el archivo '{archivo2}'")
    else:
        print(f"El archivo '{archivo1}' tiene el mismo tamaño que el archivo '{archivo2}'")

# Ejemplo de uso
comparar_tamano_archivos("archivo1.txt", "archivo2.txt")
