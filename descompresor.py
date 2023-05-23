import Node
import sys
import time

start_time = time.time()
# Leer argumento
if len(sys.argv) > 1:
    file = (sys.argv[1])
else:
    print('Debe proporcionar un filepath como argumento.')
    sys.exit(1)

Node.descompresor(file)
end_time = time.time()

elapsed_time = end_time - start_time

print(elapsed_time)