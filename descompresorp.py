import Node
import sys
import re
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def claves_menores(diccionario,k):
    valores_mas_pequenos = Node.heapq.nsmallest(k, diccionario.items(), key=lambda x: x[1])
    return valores_mas_pequenos

def separador(oracion,palabras):
    partes = re.split(f'({"|".join(map(re.escape, palabras))})', oracion)
    partes_limpio = [parte.strip() for parte in partes if parte.strip()]
    return partes_limpio

def obtener_columna(lista, indice_columna):
    columna = []
    for fila in lista:
        if indice_columna < len(fila):
            #print(fila[indice_columna])
            columna.append(fila[indice_columna])
    return columna

if(rank==0):

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
    huffmanEncoding = Node.CalculateCodes(the_nodes[0])
    #print(the_symbols)
    min_values=claves_menores(the_symbols,size-1)
    print(min_values)
    columna = obtener_columna(min_values, 0)
    listtemp = []
    for item in columna:
        if (item in huffmanEncoding):
            print(item)
            listtemp.append(huffmanEncoding[item])
    print(listtemp)
    resultado=separador(huffman_encoding,listtemp)
    #for parte in resultado:
    #    print(parte)
    j=0
    b={}
    for a in range(1,size-1):
        comm.send(the_nodes[0],dest=a,tag=0)
        comm.send(resultado[j],dest=a,tag=j)
        j=j+1
    while(j<len(resultado)):
        status = MPI.Status()
        message_exists = comm.Iprobe(source=MPI.ANY_SOURCE, status=status)
        if(message_exists):
            source=status.Get_source()
            data=comm.recv(source=source)
            b[status.Get_tag()]=data
            comm.send(resultado[j],dest=status.Get_source(),tag=status.Get_tag())
            j=j+1
    for a in range(1,size-1):        
        comm.send('end',dest=a,tag=-1)
    diccionario_ordenado = dict(sorted(b.items(), key=lambda x: x[0]))
    cadena = ''.join([f" {valor}" for clave, valor in diccionario_ordenado.items()] )
    print(cadena)

else:
    
    tabla=comm.recv(source=0,tag=0)
    status = MPI.Status()
    message_exists = comm.Iprobe(source=MPI.ANY_SOURCE, status=status)
    if(message_exists):
        source=status.Get_source()
        tag=status.Get_tag()
        while(tag!=-1):
            if(tag!=0):
                if(message_exists):
                    source=status.Get_source()
                    tag=status.Get_tag()
                    data=comm.recv(source=0)
                    decoded_output = Node.HuffmanDecoding(data, tabla)
                    fragmentos=[]
                    for i in range(0, len(decoded_output), 3):
                        fragmento = decoded_output[i:i+3]
                        hex_num = format((int(fragmento)),'x')
                        hex_num=hex_num.zfill(2)  
                        fragmentos.append(hex_num)
                    string = ''.join([fragmento for fragmento in fragmentos])
                    bytes_data = bytes.fromhex(string)
                    comm.send(bytes_data, dest=0,tag=tag)
                        


