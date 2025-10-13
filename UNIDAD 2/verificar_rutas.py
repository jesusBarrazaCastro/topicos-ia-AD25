# verificar_rutas.py
import pandas as pd

# Nombre del archivo que vamos a verificar
ARCHIVO_RUTAS = 'rutas_optimizadas.csv'

print(f"--- Verificando el archivo: {ARCHIVO_RUTAS} ---")

try:
    df_rutas = pd.read_csv(ARCHIVO_RUTAS)
    
    num_rutas = len(df_rutas)
    print(f"\nResultado: Se encontraron {num_rutas} rutas en el archivo.")
    
    if num_rutas > 0:
        print("\nAnálisis de cada ruta encontrada:")
        for index, row in df_rutas.iterrows():
            id_ruta = row['id_ruta']
            nodos = row['nodos'].split(';')
            nodo_inicio = nodos[0]
            print(f"  - Ruta #{id_ruta}: Inicia en el Centro de Distribución con ID '{nodo_inicio}'")
    
    print("\n--- Verificación Terminada ---")

except FileNotFoundError:
    print(f"\nERROR: No se encontró el archivo '{ARCHIVO_RUTAS}'.")
    print("Asegúrate de que este script esté en la misma carpeta que 'rutas_optimizadas.csv'.")
except Exception as e:
    print(f"\nOcurrió un error inesperado al leer el archivo: {e}")