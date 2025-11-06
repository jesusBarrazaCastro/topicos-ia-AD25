# 🌾 Optimización de Riego con Enjambre de Partículas 💧


## 👨‍💻 Autores
Proyecto desarrollado por **Jesús Alberto Barraza Castro y Jesús Guadalupe Wong Camacho**  
TecNM Campus Culiacán — Ingeniería en Tecnologías de la Información y Comunicaciones  
2025


## 📘 Resumen del Proyecto

Este proyecto aplica el algoritmo **Particle Swarm Optimization (PSO)** para optimizar la **colocación de sensores de humedad en campos agrícolas**, tomando como caso de estudio la región de **Guasave, Sinaloa**.  
El objetivo es encontrar las **mejores ubicaciones posibles para los sensores**, considerando factores como la **topografía**, **tipo de cultivo** y **salinidad del suelo**, con el fin de **mejorar la eficiencia del riego y el uso del agua**.

---

## 🎯 Objetivos

### 🧭 Objetivo General
Optimizar la colocación de sensores de humedad en campos agrícolas mediante el uso del algoritmo **Particle Swarm Optimization (PSO)**, mejorando la gestión hídrica y la precisión del monitoreo.

### 🎯 Objetivos Específicos
- 🌌 Modelar el problema de colocación de sensores como un **espacio de búsqueda multidimensional**.  
- 🌾 Implementar el algoritmo **PSO** para encontrar configuraciones óptimas de sensores considerando topografía, cultivos y suelo.  
- 📊 Evaluar el rendimiento del algoritmo mediante **simulaciones y análisis de eficiencia hídrica**.

---

## 🧩 Descripción del Problema

En sistemas de riego extensos, colocar sensores de humedad de forma aleatoria o uniforme no garantiza una medición representativa.  
Zonas con diferentes **tipos de cultivo**, **alturas**, o **niveles de salinidad** pueden requerir más monitoreo.  
Por tanto, el reto consiste en **determinar posiciones óptimas** para `K` sensores, maximizando la cobertura efectiva del terreno.

El **algoritmo PSO** ofrece una solución metaheurística capaz de explorar eficientemente el espacio de posibles ubicaciones, encontrando una configuración que **minimiza la distancia ponderada entre los sensores y los puntos críticos del terreno**.

---

## ⚙️ Estructura del Proyecto

| Archivo | Descripción |
|----------|--------------|
| `PSO_optimizacion_riego.ipynb` | Notebook principal (implementación completa y pruebas funcionales) |
| `README.md` | Documentacion del proyecto (este archivo) |

---

## 🧠 ¿Cómo Funciona?

### 1️⃣ Generación de Datos Simulados
Se genera un conjunto de puntos `(x, y)` representando posiciones en el terreno con atributos:
- **Cultivo:** Maíz 🌽, Tomate 🍅 o Chile 🌶️  
- **Elevación:** simulada entre 10 y 50 metros.  
- **Salinidad:** 0.5–4 dS/m, mayor en zonas específicas.  
- **Humedad:** derivada de cultivo y elevación.

👉 Esto permite simular condiciones realistas sin necesidad de datos reales.

---

### 2️⃣ Interpolación de Propiedades (KNN)
Se entrenan modelos **K-Nearest Neighbors (KNN)** para estimar, a partir de coordenadas `(x, y)`:
- Humedad 🌊  
- Elevación 🏔️  
- Salinidad 🧂  
- Tipo de cultivo 🌱  

Esto permite evaluar cualquier punto del terreno, incluso fuera de los muestreados originalmente.

---

### 3️⃣ Definición de la Función de Costo 💰

La función de costo mide **qué tan buena es una configuración de sensores**.  
Cada partícula (solución candidata) representa las coordenadas de los sensores:  
`[x₁, y₁, x₂, y₂, ..., xₖ, yₖ]`.

El costo combina:
- Distancia a los puntos más cercanos del terreno.  
- Peso por **tipo de cultivo** (prioriza cultivos sensibles).  
- Peso por **salinidad** (zonas más salinas → más prioridad).  
- Peso por **elevación** (pendientes pueden afectar drenaje y humedad).

📉 **Objetivo:** minimizar el promedio de distancia ponderada.

---

### 4️⃣ Implementación Propia del Algoritmo PSO 🐦

El **PSO clásico (Global Best)** se implementó desde cero, con:
- **Partículas:** posibles configuraciones de sensores.  
- **Velocidad e inercia:** definen movimiento en el espacio de búsqueda.  
- **Componentes cognitivo y social:** permiten explorar y explotar la búsqueda.  

Ecuación de actualización:
```
v = w*v + c1*r1*(pbest - pos) + c2*r2*(gbest - pos)
pos = pos + v
```

Cada iteración ajusta las posiciones hacia las mejores soluciones encontradas individual y colectivamente.

---

### 5️⃣ Pruebas Funcionales 🧪

Se probaron múltiples configuraciones:
- 🌊 Terreno plano con baja salinidad.  
- 🏔️ Terreno con pendiente variable.  
- 🧂 Terreno con alta salinidad en zonas concretas.  

Cada escenario:
- Genera nuevos datos simulados.  
- Ejecuta el PSO con parámetros específicos (`n_particles`, `max_iter`).  
- Muestra:
  - 📍 Posiciones óptimas de sensores en el mapa.  
  - 📈 Curva de convergencia (costo vs iteraciones).  

Estas pruebas demuestran que el algoritmo se adapta correctamente a diferentes condiciones del terreno.

---

## 🔍 Resultados

| Escenario | Nº de Sensores | Mejor Costo | Observaciones |
|------------|----------------|--------------|----------------|
| Base | 4 | 0.024 | Cobertura uniforme en todo el campo |
| Alta Salinidad | 4 | 0.018 | Sensores concentrados en zonas salinas |
| Pendiente Alta | 4 | 0.021 | Sensores distribuidos según la elevación |

**Conclusión:** el PSO converge de forma estable y genera configuraciones con sentido agronómico.

---

## 💡 Cómo Esto Soluciona el Problema

✅ **Optimización multidimensional:**  
Cada sensor añade dos dimensiones (x, y), formando un espacio de búsqueda de `2K` dimensiones.

✅ **Criterio realista:**  
La función de costo incluye factores de cultivo, salinidad y elevación.

✅ **Eficiencia en el riego:**  
Los sensores se ubican donde más influyen las condiciones del suelo y la humedad, permitiendo decisiones de riego más precisas.

✅ **Adaptabilidad:**  
Puede aplicarse a terrenos reales si se reemplazan los datos simulados por datos GIS o de campo.

---

## 🚀 Ejecución del Notebook

### 🧰 Requisitos
```
pip install numpy pandas scikit-learn matplotlib seaborn scipy
```

### ▶️ Pasos
1. Abrir el notebook `PSO_optimizacion_riego.ipynb` en Jupyter o Google Colab.  
2. Ejecutar todas las celdas en orden.  
3. Ajustar parámetros:
   - `K`: número de sensores.
   - `n_particles`, `max_iter`: tamaño del enjambre y número de iteraciones.
4. Visualizar los resultados:
   - Mapas con los sensores óptimos.
   - Curvas de convergencia.

---
