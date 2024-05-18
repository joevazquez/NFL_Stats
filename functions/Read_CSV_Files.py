import functions.Config as Config
import pandas as pd
import os

 # Ruta al archivo CSV en la carpeta 'data'
csv_file_path = os.path.join('Datasets', Config.BasicStats)
    
# Leer el archivo CSV usando pandas
df = pd.read_csv(csv_file_path)
print()
print("Muestra de la Data básica de la NFL:")
print(df)

