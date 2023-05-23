import sys


def compare_files(file1, file2):
    with open(file1, 'rb') as a1, open(file2, 'rb') as a2:
        c1 = a1.read()
        c2 = a2.read()
    if c1 == c2:
        print("ok")
    else:
        print("nok")

if len(sys.argv) > 2:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    compare_files(file1, file2)
else:
    print('Debe proporcionar dos filepaths como argumentos.')
    sys.exit(1)
