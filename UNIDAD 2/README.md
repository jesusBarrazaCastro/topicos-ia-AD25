# 🧠 Sistema de Enrutamiento para Tiendas de Autoservicio 🚚🛒  
### Módulo II — Algoritmos Heurísticos  
**Trabajo de:** Wong Camacho Jesus Guadalupe, Barraza Castro Jesus Alberto  
**Fecha:** 12 de octubre de 2025

---

## 📘 Descripción general
Este proyecto implementa una **solución computacional para optimizar las rutas de distribución** de productos desde los **Centros de Distribución (CD)** hacia diversas **tiendas de autoservicio** ubicadas en Culiacán, Sinaloa.  

El enfoque utiliza un **algoritmo heurístico de Recocido Simulado (Simulated Annealing)** para minimizar el **costo total de combustible** y la **distancia recorrida**, mejorando la eficiencia logística y reduciendo los costos operativos de la cadena de tiendas.

---

## 🎯 Objetivo general
Optimizar la asignación de rutas de transporte entre los Centros de Distribución y las tiendas, reduciendo los costos de recorrido mediante un enfoque heurístico.

---

## 🧩 Modelado del problema

### Entradas
- **Tabla de ubicaciones:** lista de tiendas y centros de distribución.  
- **Matriz de distancias:** distancias en kilómetros entre cada par de ubicaciones.  
- **Matriz de costos de combustible:** costo asociado a recorrer cada tramo.  

### Resultados
- Rutas optimizadas por cada vehículo, indicando las tiendas que atiende y su costo total.  
- Resumen con la distancia y costo global.  

### Restricciones y supuestos
- Cada tienda se asigna inicialmente al CD más cercano.  
- Cada ruta inicia y termina en su Centro de Distribución.  
- Se asume disponibilidad suficiente de vehículos.

---

## ⚙️ Algoritmo seleccionado: Recocido Simulado 

El **Recocido Simulado** es un método heurístico inspirado en la **metalurgia**, donde un material se calienta y luego enfría lentamente para alcanzar un estado de mínima energía.

En este contexto:
- Cada **solución** representa un conjunto de rutas posibles.
- Los **movimientos** modifican la solución (intercambios, reubicaciones, inversiones de segmentos).
- Se acepta una solución peor con cierta probabilidad que disminuye con la temperatura, para evitar mínimos locales.

### Parámetros utilizados

| Parámetro | Valor | Descripción |
|------------|--------|-------------|
| Temperatura inicial | 1000.0 | Nivel inicial de exploración |
| Tasa de enfriamiento | 0.995 | Reduce gradualmente la temperatura |
| Iteraciones por temperatura | 300 | Intentos por nivel de temperatura |
| Temperatura mínima | 0.1 | Condición de parada |
| Semilla aleatoria | 42 | Reproducibilidad |

---

## 🧠 Estructura del código (`routing_sa_FINAL.py`)

| Sección | Descripción |
|----------|--------------|
| **1. Configuración de parámetros** | Define rutas de archivos y constantes del algoritmo. |
| **2. Carga de datos** | Lee CSV de ubicaciones, distancias y costos de combustible. |
| **3. Solución inicial por clúster** | Asigna cada tienda al CD más cercano. |
| **4. Funciones de evaluación** | Calculan el costo y distancia total de cada ruta. |
| **5. Movimientos de vecindario** | Aplica operaciones `swap`, `2-opt` y `relocate` para explorar soluciones vecinas. |
| **6. Algoritmo principal** | Ejecuta el recocido simulado, guarda las rutas y genera resumen final. |

---

## 🧾 Flujo de ejecución

1. Carga los datos desde la carpeta `/Datos/`.
2. Crea una solución inicial agrupando tiendas por su CD más cercano.
3. Calcula el costo y la distancia inicial total.
4. Inicia el proceso de recocido:
   - Genera vecinos aleatorios.
   - Evalúa si se aceptan según la temperatura.
   - Actualiza la mejor solución encontrada.
5. Exporta los resultados en formato `.csv`.

---

## 📊 Resultados obtenidos

Tras ejecutar el script, se obtienen los siguientes indicadores:

| Métrica | Antes de la optimización | Después de la optimización |
|----------|--------------------------|-----------------------------|
| Costo total de combustible | _(variable según datos)_ | _(menor que el inicial)_ |
| Distancia total | _(variable según datos)_ | _(menor que el inicial)_ |
| Número de rutas | Según CDs | Igual o menor |

Los resultados se guardan automáticamente en:

- `rutas_optimizadas.csv`  
- `resumen_optimizacion.csv`

Cada archivo contiene:

- **rutas_optimizadas.csv:** listado de rutas, nodos, costos y distancias.  
- **resumen_optimizacion.csv:** costo total, distancia total y número de vehículos.

---

## 🗺️ Visualización del mapa
(En esta sección se incluirá el script de visualización. Este mapa mostrará las rutas optimizadas sobre un mapa de Culiacán, utilizando `matplotlib` o `folium`.  
Cada Centro de Distribución se marcará con un color distinto y las rutas se dibujarán conectando las tiendas asignadas.)

---

## 💬 Conclusiones

- El algoritmo de **Recocido Simulado** permitió obtener rutas más eficientes en comparación con la asignación inicial por clúster.  
- Se logró reducir significativamente el **costo total de combustible**, manteniendo una distribución equilibrada de las tiendas entre los centros.  
- La estrategia de vecindarios combinados (`swap`, `2-opt`, `relocate`) resultó clave para evitar estancamientos locales.  
- Este enfoque puede escalarse fácilmente para otros escenarios logísticos o cadenas de distribución reales.

---


