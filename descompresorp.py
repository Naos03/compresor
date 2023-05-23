import Node
import sys
import re
from mpi4py import MPI
import time
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def claves_menores(diccionario,k):
    valores_mas_pequenos = Node.heapq.nsmallest(k, diccionario.items(), key=lambda x: x[1])
    return valores_mas_pequenos

def separador(text, words,m):
    pattern = r'({})'.format('|'.join(map(re.escape, words)))
    parts = re.split(pattern, text)
    parts_clean = [part.strip() for part in parts if part.strip()]
    pares = []
    for i in range(0, len(parts_clean), 2):
        if i + 1 < len(parts_clean):
            par = parts_clean[i] + parts_clean[i + 1]
            pares.append(par)
        else:
            pares.append(parts_clean[i])
    a=len(pares)//m+1
    grupos = [pares[i:i+a] for i in range(0, len(pares), a)]
    ah=[]
    for grupo in grupos:
        cadena = ''.join(grupo)
        ah.append(cadena)
    return ah

def obtener_columna(lista, indice_columna):
    columna = []
    for fila in lista:
        if indice_columna < len(fila):
            columna.append(fila[indice_columna])
    return columna

if(rank==0):
    start_time = time.time()
    # Leer argumento
    if len(sys.argv) > 1:
        file = (sys.argv[1])
    else:
        print('Debe proporcionar un filepath como argumento.')
        sys.exit(1)

    with open(file, "rb") as file:
        contents = file.read()
    idx  = contents.rfind(b'{')
    if idx == -1:
        print("Could not find '{' character in the file.")
    else:
        huffman_encoding = contents[:idx]
        symbol_dict_str = contents[idx:-1]
        l=(contents[-1])
        l=chr(l)
        l=int(l)
    # Convierte los bytes en una cadena de texto
    symbol_dict_str = symbol_dict_str.decode()

    import ast
    the_symbols = ast.literal_eval(symbol_dict_str)
    huffman_encoding=Node.bytes_to_binary_string(huffman_encoding)
    huffman_encoding=huffman_encoding[l:]
    the_symbols_key=the_symbols.keys()
    # converting symbols and probabilities into huffman tree nodes
    the_nodes = []
    for symbol in the_symbols_key:
        the_nodes.append(Node.Nodes(the_symbols.get(symbol), symbol))

    # Use a heap to store the nodes
    Node.heapq.heapify(the_nodes)

    while len(the_nodes) > 1:
        # picking two smallest nodes
        left = Node.heapq.heappop(the_nodes)
        right = Node.heapq.heappop(the_nodes)
        left.code = 0
        right.code = 1

        # combining the 2 smallest nodes to create new node
        newNode = Node.Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)

        Node.heapq.heappush(the_nodes, newNode)
    he = Node.CalculateCodes(the_nodes[0])
    min_values=claves_menores(the_symbols,size-1)
    columna = obtener_columna(min_values, 0)
    listtemp = []
    for item in columna:
        if (item in he):
            listtemp.append(he[item])
    resultado=separador(huffman_encoding,listtemp,size-1)
    iu=[]

    b={}
    decoded_output=[]

    for i in range(1,size):
        comm.send(the_nodes[0],dest=i,tag=0)
    for i in range (1,size):
        comm.send(resultado[i-1],dest=i,tag=1)
    for i in range(1,size):
        decoded_output.append(comm.recv(source=i,tag=2))
    deco=''.join(decoded_output)
    fragmentos=[]
    for i in range(0, len(deco), 3):
        fragmento = deco[i:i+3]
        hex_num = format((int(fragmento)),'x')
        hex_num=hex_num.zfill(2)  
        fragmentos.append(hex_num)
    string = ''.join([fragmento for fragmento in fragmentos])
    bytes_data = bytes.fromhex(string)
    with open('descomprimidop-elmejorprofesor.txt', mode='wb') as f:
        f.write(bytes_data)
    f.close()
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(elapsed_time)
else:
    tabla=comm.recv(source=0,tag=0)
    data=comm.recv(source=0,tag=1)
    decodif= Node.HuffmanDecoding(data,tabla)
    comm.send(decodif,dest=0,tag=2)
                        


