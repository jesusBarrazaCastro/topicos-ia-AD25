# crear_mapa_con_capas.py
"""
Este script genera un mapa interactivo con las rutas optimizadas,
agrupando cada ruta en una capa individual para mejor visualización.
"""

import pandas as pd
import folium
import random

print("Iniciando la creación del mapa con rutas en capas separadas...")

# --- 1. CONFIGURACIÓN DE ARCHIVOS ---
ARCHIVO_UBICACIONES = 'Datos/datos_distribucion_tiendas.csv'
ARCHIVO_RUTAS_OPTIMIZADAS = 'rutas_optimizadas.csv'
ARCHIVO_SALIDA_MAPA = 'mapa_con_rutas_interactivo.html' # Nuevo nombre para no sobreescribir el anterior

# --- 2. CARGAR LOS DATOS ---
try:
    df_ubicaciones = pd.read_csv(ARCHIVO_UBICACIONES, encoding='latin1')
    df_rutas = pd.read_csv(ARCHIVO_RUTAS_OPTIMIZADAS)
except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar el archivo {e.filename}.")
    exit()

# --- 3. CREAR EL MAPA BASE ---
latitud_centro = df_ubicaciones['Latitud_WGS84'].mean()
longitud_centro = df_ubicaciones['Longitud_WGS84'].mean()
mapa = folium.Map(location=[latitud_centro, longitud_centro], zoom_start=12, tiles="cartodbpositron")

# --- 4. AÑADIR MARCADORES (en su propia capa)---
capa_ubicaciones = folium.FeatureGroup(name="Ubicaciones", show=True)
mapa.add_child(capa_ubicaciones)

for idx, fila in df_ubicaciones.iterrows():
    popup_text = f"<b>{fila['Nombre']}</b><br>Tipo: {fila['Tipo']}"
    if fila['Tipo'] == 'Centro de Distribución':
        folium.Marker(
            location=[fila['Latitud_WGS84'], fila['Longitud_WGS84']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color='red', icon='truck', prefix='fa')
        ).add_to(capa_ubicaciones)
    else:
        folium.CircleMarker(
            location=[fila['Latitud_WGS84'], fila['Longitud_WGS84']],
            radius=5, popup=folium.Popup(popup_text, max_width=300),
            color='blue', fill=True, fill_color='blue'
        ).add_to(capa_ubicaciones)

# --- 5. DIBUJAR LAS RUTAS OPTIMIZADAS (CADA UNA EN SU PROPIA CAPA) ---
colores = ['#FF0000', '#0000FF', '#008000', '#FFA500', '#800080', '#00FFFF', '#FF00FF', '#8B4513', '#FA8072', '#4682B4']
while len(colores) < len(df_rutas):
    colores.append('#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))

for idx, fila_ruta in df_rutas.iterrows():
    id_ruta_actual = fila_ruta['id_ruta']
    # Crear una capa para esta ruta específica
    capa_ruta = folium.FeatureGroup(name=f"Ruta #{id_ruta_actual}", show=False) # 'show=False' para que inicien ocultas
    
    nodos_ruta = [int(n) for n in fila_ruta['nodos'].split(';')]
    coordenadas_ruta = []
    for nodo_id in nodos_ruta:
        ubicacion = df_ubicaciones.iloc[nodo_id]
        coordenadas_ruta.append((ubicacion['Latitud_WGS84'], ubicacion['Longitud_WGS84']))
        
    popup_ruta = (f"<b>Ruta #{id_ruta_actual}</b><br>"
                  f"Costo: {fila_ruta['costo_combustible']}<br>"
                  f"Distancia: {fila_ruta['distancia_km']}")
    
    # Dibujar la línea y añadirla a su capa específica
    folium.PolyLine(
        locations=coordenadas_ruta, color=colores[idx % len(colores)],
        weight=3, opacity=0.9, popup=folium.Popup(popup_ruta, max_width=300)
    ).add_to(capa_ruta)
    
    # Añadir la capa de la ruta al mapa
    mapa.add_child(capa_ruta)

# --- 6. AÑADIR EL CONTROL DE CAPAS Y GUARDAR ---
# ¡ESTA LÍNEA ES LA MAGIA! Agrega el menú para activar/desactivar capas
folium.LayerControl(collapsed=False).add_to(mapa)

mapa.save(ARCHIVO_SALIDA_MAPA)

print(f"\n¡Mapa interactivo generado con éxito!")
print(f"Abre el archivo '{ARCHIVO_SALIDA_MAPA}' en tu navegador.")