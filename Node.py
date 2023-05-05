import heapq
class Nodes:  
    the_symbols = dict()
    the_symbols_string  = ""
    
    def __init__(self, probability, symbol, left = None, right = None):  
        # probability of the symbol  
        self.probability = probability  
        # the symbol  
        self.symbol = symbol  
        # the left node  
        self.left = left  
        # the right node  
        self.right = right  
        # the tree direction (0 or 1)  
        self.code = ''
    def __lt__(self, other):
        return self.probability < other.probability

    def __eq__(self, other):
        if isinstance(other, Nodes):
            return self.probability == other.probability
        return False    

"""calculate the Frequencies of symbols in specified data"""        
def CalculateFrequencies(the_data):  
    global the_symbols
    the_symbols = dict()  
    for item in the_data: 
        item=str(item).zfill(3)  
        the_symbols[item]=the_symbols.get(item,0)+1     
    return the_symbols  

""" A supporting function in order to print the codes of symbols by travelling a Huffman Tree """  
def CalculateCodes(node):
    # Diccionario para almacenar los códigos Huffman
    codes = {}
    # Generar códigos Huffman utilizando una función generadora
    def generate_codes(node, code=[]):
        if node.left:
            yield from generate_codes(node.left, code + [0])
        if node.right:
            yield from generate_codes(node.right, code + [1])
        if not node.left and not node.right:
            codes[node.symbol] = ''.join([str(bit) for bit in code])
    # Llamar a la función generadora y devolver el diccionario de códigos
    list(generate_codes(node))
    return codes

#Version Iterativa
def CalculateCodesIterative(root):
    stack = [(root, "")]
    codes = {}

    while stack:
        node, code = stack.pop()

        if not node.left and not node.right:
            codes[node.symbol] = code
            continue

        if node.left:
            stack.append((node.left, code + "0"))

        if node.right:
            stack.append((node.right, code + "1"))

    return codes

""" A supporting function in order to get the encoded result """
def OutputEncoded(the_data, coding):
    # Generar la lista de códigos Huffman para cada símbolo
    
    encoding_output = [coding[str(element).zfill(3)] for element in the_data]

    # Unir los códigos Huffman en una sola cadena de texto
    return ''.join(encoding_output)

def HuffmanEncoding(the_symbols):
    the_symbols_key=the_symbols.keys()
    # converting symbols and probabilities into huffman tree nodes
    the_nodes = []
    for symbol in the_symbols_key:
        the_nodes.append(Nodes(the_symbols.get(symbol), symbol))

    # Use a heap to store the nodes
    heapq.heapify(the_nodes)

    while len(the_nodes) > 1:
        # picking two smallest nodes
        left = heapq.heappop(the_nodes)
        right = heapq.heappop(the_nodes)

        left.code = 0
        right.code = 1

        # combining the 2 smallest nodes to create new node
        newNode = Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)

        heapq.heappush(the_nodes, newNode)

    
    return the_nodes[0]

def compresor(file):
    with open(file,mode='rb') as f:
        the_data = f.read()
    f.close()
    #print(the_data)
    global the_symbols
    the_symbols=CalculateFrequencies(the_data)
    #print(the_symbols)
    the_nodes=HuffmanEncoding(the_symbols)
    huffmanEncoding = CalculateCodes(the_nodes)
    encodedOutput = OutputEncoded(the_data,huffmanEncoding)  
    #print(encodedOutput)
    my_dict_str = str(the_symbols)
    my_dict_str=my_dict_str.replace(" ", "")
    writeInBinary(encodedOutput, my_dict_str)

def writeInBinary(bits,str):
    # Open the file for writing in binary mode
    with open('comprimido.elmejorprofesor', 'wb') as file:
        # Convert the bit string to bytes
        data = int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder='big')
        # Write the bytes to the file
        #print(data)
        file.write(data)
    file.close()
    with open('comprimido.elmejorprofesor', 'a') as file:    
        file.write(str)
    file.close()

def bytes_to_binary_string(byte_string):
    binary_string = bin(int.from_bytes(byte_string, byteorder='big'))[2:]
    return binary_string    

def descompresor(file):
    with open(file, "rb") as file:
        contents = file.read()
    #print(contents)
    idx  = contents.rfind(b'{')
    if idx == -1:
        print("Could not find '{' character in the file.")
    else:
        huffman_encoding = contents[:idx]
        symbol_dict_str = contents[idx:]
        #print(huffman_encoding)
        
    # Convierte los bytes en una cadena de texto
    symbol_dict_str = symbol_dict_str.decode('utf-8')
    import ast
    the_symbols = ast.literal_eval(symbol_dict_str)
    huffman_encoding=bytes_to_binary_string(huffman_encoding)
    #print(huffman_encoding)
    the_symbols_key=the_symbols.keys()
    # converting symbols and probabilities into huffman tree nodes
    the_nodes = []
    for symbol in the_symbols_key:
        the_nodes.append(Nodes(the_symbols.get(symbol), symbol))

    # Use a heap to store the nodes
    heapq.heapify(the_nodes)

    while len(the_nodes) > 1:
        # picking two smallest nodes
        left = heapq.heappop(the_nodes)
        right = heapq.heappop(the_nodes)

        left.code = 0
        right.code = 1

        # combining the 2 smallest nodes to create new node
        newNode = Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)

        heapq.heappush(the_nodes, newNode)
    
    # Reconstruye el árbol de decodificación
    #decoding_tree = huffman_encoding(symbol_dict_str)

    # Decodifica los bits utilizando el árbol de decodificación
    decoded_output = HuffmanDecoding(huffman_encoding, the_nodes[0])
    #print(decoded_output)    
    # Escribe el resultado decodificado en un archivo
    fragmentos=[]
    for i in range(0, len(decoded_output), 3):
        fragmento = decoded_output[i:i+3]
        hex_num = format((int(fragmento)),'x')
        hex_num=hex_num.zfill(2)  
        fragmentos.append(hex_num)
    string = ''.join([fragmento for fragmento in fragmentos])
    bytes_data = bytes.fromhex(string)
        #print(data)
        
    with open('descomprimido-elmejorprofesor.txt', mode='wb') as f:
        f.write(bytes_data)

    #print('Archivo descomprimido exitosamente!')

def HuffmanDecoding(encodedData, huffmanTree):  
    treeHead = huffmanTree  
    decodedOutput = []  
    for x in encodedData:  
        if x == '1':  
            huffmanTree = huffmanTree.right     
        elif x == '0':  
            huffmanTree = huffmanTree.left  
        try:  
            if huffmanTree.left.symbol == None and huffmanTree.right.symbol == None:  
                pass  
        except AttributeError:  
            decodedOutput.append(huffmanTree.symbol)  
            huffmanTree = treeHead  
          
    string = ''.join([str(item) for item in decodedOutput])  
    return string 