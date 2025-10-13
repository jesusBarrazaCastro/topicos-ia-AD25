# routing_sa_FINAL.py
"""
Versión final del script de optimización.
Utiliza un enfoque de clustering para asignar tiendas al Centro de Distribución más cercano
y optimiza el conjunto completo de rutas.
"""

import math
import random
import time
import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# 1. PARÁMETROS DE CONFIGURACIÓN
# -----------------------------------------------------------------------------
ARCHIVO_UBICACIONES = 'Datos/datos_distribucion_tiendas.csv'
ARCHIVO_COSTOS_COMBUSTIBLE = 'Datos/matriz_costos_combustible.csv'
ARCHIVO_DISTANCIAS = 'Datos/matriz_distancias.csv'

# Parámetros del Algoritmo de Recocido Simulado
TEMPERATURA_INICIAL = 1000.0
TASA_ENFRIAMIENTO = 0.995
ITERACIONES_POR_TEMPERATURA = 300
TEMPERATURA_MINIMA = 0.1
SEMILLA_ALEATORIA = 42
ARCHIVO_SALIDA_RUTAS = 'rutas_optimizadas.csv'
ARCHIVO_SALIDA_RESUMEN = 'resumen_optimizacion.csv'

# -----------------------------------------------------------------------------
# 2. FUNCIONES UTILITARIAS Y DE CARGA DE DATOS
# -----------------------------------------------------------------------------
def cargar_datos(path_ubicaciones, path_costos, path_distancias):
    print("Cargando datos...")
    try:
        df_ubicaciones = pd.read_csv(path_ubicaciones, encoding='latin1')
        indices_depots = list(df_ubicaciones[df_ubicaciones['Tipo'] == 'Centro de Distribución'].index)
        matriz_costos = pd.read_csv(path_costos, header=0).to_numpy()
        matriz_distancias = pd.read_csv(path_distancias, header=0).to_numpy()
        print(f"Datos cargados: {len(df_ubicaciones)} ubicaciones encontradas.")
        print(f"{len(indices_depots)} Centros de Distribución identificados en los índices: {indices_depots}")
        return df_ubicaciones, matriz_costos, matriz_distancias, indices_depots
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo {e.filename}.")
        print("Asegúrate de que la carpeta 'Datos' esté en el mismo directorio que el script.")
        exit()

# -----------------------------------------------------------------------------
# 3. CREACIÓN DE LA SOLUCIÓN INICIAL (MÉTODO POR CLUSTER)
# -----------------------------------------------------------------------------

def crear_solucion_inicial_por_cluster(df_ubicaciones, depots, matriz_distancias):
    print("Creando solución inicial por clúster...")
    # Identifica los índices de las tiendas (nodos que no son CD)
    indices_tiendas = list(set(df_ubicaciones.index) - set(depots))
    clusters = {depot_idx: [] for depot_idx in depots}
    # Asigna cada tienda al CD con la distancia mínima
    for tienda_idx in indices_tiendas:
        distancias_a_depots = matriz_distancias[tienda_idx, depots] # Distancias de la tienda a todos los CD
        depot_mas_cercano_idx_en_lista = np.argmin(distancias_a_depots) # Encuentra el índice del CD más cercano en la lista 'depots'
        depot_real_idx = depots[depot_mas_cercano_idx_en_lista]# Obtiene el índice real del CD
        clusters[depot_real_idx].append(tienda_idx)# Agrupa la tienda al CD más cercano
        
    solucion_inicial = []
    
    # Construye las rutas para cada clúster (CD)
    for depot_idx, tiendas_asignadas in clusters.items():
        if tiendas_asignadas:
            
            # Ordena las tiendas asignadas por su distancia al CD (del más cercano al más lejano)
            tiendas_ordenadas_por_distancia = sorted(
                tiendas_asignadas,
                key=lambda tienda: matriz_distancias[depot_idx, tienda] 
            )
            
            # Formato de la ruta: [CD, Tienda_1, ..., Tienda_N, CD]
            ruta = [depot_idx] + tiendas_ordenadas_por_distancia + [depot_idx]
            solucion_inicial.append(ruta)
            
    return solucion_inicial

# -----------------------------------------------------------------------------
# 4. FUNCIÓN OBJETIVO Y MOVIMIENTOS DE VECINDARIO
# -----------------------------------------------------------------------------
def calcular_metrica_ruta(ruta, matriz):
    total = 0.0
    for i in range(len(ruta) - 1):
        total += matriz[ruta[i], ruta[i+1]]
    return total

def calcular_metrica_total(rutas, matriz):
    return sum(calcular_metrica_ruta(r, matriz) for r in rutas)

def generar_vecino(rutas):
    if not rutas or len(rutas) == 0:
        return []
    
    nuevas_rutas = [r.copy() for r in rutas]
    tipo_movimiento = random.choice(['swap', '2opt',])

    if tipo_movimiento == 'swap' and len(nuevas_rutas) > 1:
        idx_ruta1, idx_ruta2 = random.sample(range(len(nuevas_rutas)), 2)
        ruta1, ruta2 = nuevas_rutas[idx_ruta1], nuevas_rutas[idx_ruta2]
        if len(ruta1) > 2 and len(ruta2) > 2:  # Ambas deben tener tiendas
            idx_tienda1 = random.randint(1, len(ruta1) - 2)
            idx_tienda2 = random.randint(1, len(ruta2) - 2)
            ruta1[idx_tienda1], ruta2[idx_tienda2] = ruta2[idx_tienda2], ruta1[idx_tienda1]

    elif tipo_movimiento == '2opt':
        idx_ruta = random.randrange(len(nuevas_rutas))
        ruta = nuevas_rutas[idx_ruta]
        if len(ruta) > 4:  # Necesita al menos 2 tiendas para hacer 2-opt
            i, j = random.sample(range(1, len(ruta) - 1), 2)
            if i > j: i, j = j, i
            ruta[i:j+1] = list(reversed(ruta[i:j+1]))
    
    # SOLUCIÓN CRÍTICA: NO eliminar rutas, mantener todas incluso si solo tienen [depot, depot]
    return nuevas_rutas  # ← CAMBIO CLAVE: quitar el filtro

# -----------------------------------------------------------------------------
# 5. ALGORITMO DE RECOCIDO SIMULADO
# -----------------------------------------------------------------------------
def recocido_simulado(rutas_iniciales, matriz_costos, semilla):
    print("\nIniciando optimización con Recocido Simulado...")
    random.seed(semilla)
    solucion_actual = [r.copy() for r in rutas_iniciales]
    costo_actual = calcular_metrica_total(solucion_actual, matriz_costos)
    mejor_solucion = [r.copy() for r in solucion_actual]
    mejor_costo = costo_actual
    temperatura = TEMPERATURA_INICIAL
    start_time = time.time()
    
    while temperatura > TEMPERATURA_MINIMA:
        for _ in range(ITERACIONES_POR_TEMPERATURA):
            solucion_vecina = generar_vecino(solucion_actual)
            costo_vecino = calcular_metrica_total(solucion_vecina, matriz_costos)
            diferencia_costo = costo_vecino - costo_actual
            if diferencia_costo < 0 or random.random() < math.exp(-diferencia_costo / temperatura):
                solucion_actual = solucion_vecina
                costo_actual = costo_vecino
                if costo_actual < mejor_costo:
                    mejor_solucion = [r.copy() for r in solucion_actual]
                    mejor_costo = costo_actual
        temperatura *= TASA_ENFRIAMIENTO
        print(f"Temperatura: {temperatura:.2f}, Mejor Costo Actual: ${mejor_costo:,.2f}", end="\r")
    
    print("\nOptimización completada en {:.2f} segundos.".format(time.time() - start_time))
    return mejor_solucion, mejor_costo

# -----------------------------------------------------------------------------
# 6. SCRIPT PRINCIPAL
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    df_ubicaciones, matriz_costos, matriz_distancias, depots = cargar_datos(
        ARCHIVO_UBICACIONES, ARCHIVO_COSTOS_COMBUSTIBLE, ARCHIVO_DISTANCIAS
    )
    
    rutas_iniciales = crear_solucion_inicial_por_cluster(df_ubicaciones, depots, matriz_distancias)
    
    costo_inicial = calcular_metrica_total(rutas_iniciales, matriz_costos)
    distancia_inicial = calcular_metrica_total(rutas_iniciales, matriz_distancias)
    
    print("\n--- Solución Inicial (por Clúster) ---")
    print(f"Número de rutas generadas: {len(rutas_iniciales)}")
    print(f"Costo de combustible inicial: ${costo_inicial:,.2f}")
    print(f"Distancia total inicial: {distancia_inicial:,.2f} km")
    
    rutas_optimizadas, costo_optimizado = recocido_simulado(rutas_iniciales, matriz_costos, SEMILLA_ALEATORIA)
    distancia_optimizada = calcular_metrica_total(rutas_optimizadas, matriz_distancias)
    
    print("\n--- Solución Optimizada ---")
    print(f"Número de rutas: {len(rutas_optimizadas)}")
    print(f"Costo de combustible optimizado: ${costo_optimizado:,.2f}")
    print(f"Distancia total optimizada: {distancia_optimizada:,.2f} km")
    
    print("\nGuardando resultados...")
    datos_rutas_salida = []
    for i, ruta in enumerate(rutas_optimizadas):
        costo_ruta = calcular_metrica_ruta(ruta, matriz_costos)
        distancia_ruta = calcular_metrica_ruta(ruta, matriz_distancias)
        nodos_str = ';'.join(map(str, ruta))
        datos_rutas_salida.append({
            'id_ruta': i + 1, 'nodos': nodos_str,
            'costo_combustible': f"${costo_ruta:,.2f}", 'distancia_km': f"{distancia_ruta:,.2f}"
        })
        
    df_rutas = pd.DataFrame(datos_rutas_salida)
    df_rutas.to_csv(ARCHIVO_SALIDA_RUTAS, index=False)
    
    resumen = {
        'costo_total_combustible': f"${costo_optimizado:,.2f}",
        'distancia_total_km': f"{distancia_optimizada:,.2f}", 'numero_vehiculos': len(rutas_optimizadas)
    }
    df_resumen = pd.DataFrame([resumen])
    df_resumen.to_csv(ARCHIVO_SALIDA_RESUMEN, index=False)
    
    print(f"Rutas guardadas en -> {ARCHIVO_SALIDA_RUTAS}")
    print(f"Resumen guardado en -> {ARCHIVO_SALIDA_RESUMEN}")