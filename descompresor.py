import Node
import time

start_time = time.time()
Node.descompresor('comprimido.elmejorprofesor')
end_time = time.time()

elapsed_time = end_time - start_time

print(f"El tiempo de ejecución fue de {elapsed_time:.6f} segundos")