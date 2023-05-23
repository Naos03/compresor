import Node
import sys
from mpi4py import MPI
import time
start_time = time.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

import math

def dividir_bytes(datos, partes):
    longitud = len(datos)
    tamano_parte = math.ceil(longitud / partes)  # Calcula el tamaño de cada parte redondeando hacia arriba

    resultado = []
    inicio = 0
    fin = tamano_parte

    for i in range(partes):
        parte = datos[inicio:fin]  # Obtiene el segmento correspondiente de bytes
        resultado.append(parte)
        inicio = fin
        fin += tamano_parte

    return resultado

def combinar_diccionarios(diccionarios):
    resultado = {}

    for diccionario in diccionarios:
        for clave, valor in diccionario.items():
            if clave in resultado:
                resultado[clave] += valor
            else:
                resultado[clave] = valor
    return resultado

# Leer argumento
if len(sys.argv) > 1:
    file = (sys.argv[1])
else:
    print('Debe proporcionar un filepath como argumento.')
    sys.exit(1)

if rank == 0:
    #este es el proceso maestro
    with open(file,mode='rb') as f:
        the_data = f.read()
    f.close()
    the_data=dividir_bytes(the_data,size-1)
    symbols=[]
    for i in range(1,size):
        comm.ssend(the_data[i-1], dest=i,tag=1)
    for i in range(1,size):
        symbols.append(comm.recv(source=i,tag=2))
    global the_symbols
    the_symbols=combinar_diccionarios(symbols)
    the_nodes=Node.HuffmanEncoding(the_symbols)
    huffmanEncoding = Node.CalculateCodes(the_nodes)
    encodedOutput=[]
    for i in range(1,size):
        comm.ssend(huffmanEncoding, dest=i,tag=3)
    my_dict_str = str(the_symbols)
    my_dict_str=my_dict_str.replace(" ", "")    
    for i in range(1,size):
        encodedOutput.append(comm.recv(source=i,tag=4))
    encodedOutput=''.join(encodedOutput)  
    Node.writeInBinaryP(encodedOutput, my_dict_str)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)    
else:
    #este es el proceso esclavo
    the_data = comm.recv(source=0,tag=1)
    #print(the_data)
    nod=Node.CalculateFrequencies(the_data)
    comm.send(nod, dest=0,tag=2)
    huffmanEncoding=comm.recv(source=0,tag=3)
    no=Node.OutputEncoded(the_data,huffmanEncoding)
    comm.send(no, dest=0,tag=4)



