import json
import os

import os
from tqdm import tqdm

# Especificar el tamaño de fragmento deseado (número de líneas por fragmento)
chunk_size = 500000
file2 = 'yelp_dataset/yelp_academic_dataset_user.json'
file = 'yelp_dataset/yelp_academic_dataset_review.json'




num_lines = 100000

# abrir archivo de entrada
with open(file, "r") as in_file:
    # leer todas las líneas
    lines = in_file.readlines()
    # obtener el número total de líneas
    total_lines = len(lines)
    # calcular el número de partes necesarias
    num_parts = (total_lines // num_lines) + 1
    # crear un directorio para guardar las partes
    output_dir = f"{os.path.splitext(file)[0]}_parts"
    os.makedirs(output_dir, exist_ok=True)
    # dividir el archivo en partes
    for i in tqdm(range(num_parts), desc="Dividiendo archivo"):
        # obtener el rango de líneas para la parte actual
        start = i * num_lines
        end = min(start + num_lines, total_lines)
        # crear el nombre del archivo de salida
        output_path = os.path.join(output_dir, f"{os.path.basename('yelp_dataset/yelp_academic_dataset_review')}_parte{i}.json")
        # escribir las líneas correspondientes en el archivo de salida
        with open(output_path, "w") as out_file:
            out_file.writelines(lines[start:end])

