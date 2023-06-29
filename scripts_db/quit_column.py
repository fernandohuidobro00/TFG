


file = '/home/fernando/Escritorio/TFG/DeepCARSKit/dataset/tripadvisor/tripadvisor.inter'
file2 = '/home/fernando/Escritorio/TFG/DeepCARSKit/dataset/tripadvisor/tripadvisor_modifed.inter'

with open(file, 'r') as f:
    filas = f.readlines()

for i in range(len(filas)):
    filas[i] = filas[i].split(',')

for i in range(len(filas)):
    del filas[i][3]



with open(file2, 'w') as f:
    for fila in filas:
        f.write(','.join(fila))