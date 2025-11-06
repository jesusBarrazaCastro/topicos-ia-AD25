# 🧭 Informe: Solución del problema del vendedor ambulante (TSP) utilizando algoritmos genéticos

## 📖 Introducción

El **Problema del Vendedor Viajero (TSP, por sus siglas en inglés)** es uno de los desafíos más clásicos en el campo de la optimización combinatoria.  
Consiste en encontrar la ruta más corta posible que permita a un vendedor visitar una serie de ciudades **una sola vez cada una** y regresar al punto de partida.  

Matemáticamente, este problema pertenece a la categoría **NP-difícil**, lo que significa que la cantidad de posibles rutas crece factorialmente con el número de ciudades. Por ello, resolverlo mediante métodos exhaustivos resulta inviable para instancias de tamaño medio o grande.  

Ante esta dificultad, se han desarrollado **métodos heurísticos y metaheurísticos**, como los **Algoritmos Genéticos (AG)**, que ofrecen soluciones cercanas al óptimo en un tiempo razonable, aprovechando principios inspirados en la evolución biológica.

---

## 🧬 Enfoque con Algoritmos Genéticos

El enfoque implementado utiliza un **Algoritmo Genético (AG)** diseñado específicamente para el TSP. Este método se basa en una **población de rutas (candidatos)** que evolucionan a través de varias generaciones, aplicando operadores que simulan los procesos de **selección, cruce y mutación**.

### 1. Representación de Individuos
Cada individuo en la población representa una **ruta completa**, codificada como una **permutación de los índices de las ciudades**.  
Por ejemplo, una ruta `[2, 0, 1, 3]` indica que el vendedor visita las ciudades en ese orden y luego regresa al inicio.

### 2. Función de Aptitud
La **aptitud (fitness)** de cada individuo se calcula como la **distancia total del recorrido**.  
Una distancia menor indica una aptitud mejor, ya que el objetivo es **minimizar la longitud de la ruta**.

### 3. Selección (Torneo)
Se utiliza un esquema de **selección por torneo**, donde se eligen aleatoriamente varios individuos y se selecciona el mejor de ellos (el de menor distancia).  
Este método balancea **explotación y exploración**, manteniendo diversidad sin perder calidad.

### 4. Cruce (Ordered Crossover - OX1)
El operador de cruce OX1 combina dos rutas (padres) para crear un nuevo hijo:
- Se copia un segmento del primer padre.
- Se completan los espacios vacíos con las ciudades del segundo padre en el orden en que aparecen, sin repetir ninguna.  
Este enfoque preserva parcialmente el orden y la estructura de los padres, lo cual es ideal para problemas de permutación como el TSP.

### 5. Mutación (Swap Mutation)
La mutación introduce variabilidad intercambiando aleatoriamente **dos ciudades** dentro de la ruta con cierta probabilidad.  
Esto evita la convergencia prematura y ayuda a explorar nuevas regiones del espacio de búsqueda.

### 6. Elitismo
En cada generación, el mejor individuo encontrado hasta el momento se conserva directamente en la nueva población, garantizando que la calidad de las soluciones **no disminuya** con el tiempo.

---

## 📊 Resultados del Algoritmo

El algoritmo se ejecutó con los siguientes parámetros:

| Parámetro | Valor |
|------------|--------|
| Tamaño de población | 100 |
| Generaciones | 500 |
| Tasa de mutación | 0.05 |
| Tamaño del torneo | 5 |

Tras la ejecución, se obtuvo la siguiente solución:

- **Ruta óptima encontrada:**  
  `F -> B -> D -> G -> E -> A -> C -> F`

- **Distancia total mínima:**  
  **≈27.090**

El gráfico generado muestra la **ruta óptima** sobre las coordenadas de las ciudades y una **curva de convergencia** que refleja cómo el algoritmo fue mejorando progresivamente la calidad de las soluciones a lo largo de las generaciones.

📈 **Observación:**  
Durante las primeras generaciones, la mejora en la distancia es rápida, mientras que en etapas posteriores el progreso se vuelve más lento a medida que el algoritmo se aproxima a una solución estable.

---

## ⚙️ Desafíos y Soluciones

Durante el desarrollo del algoritmo, se enfrentaron varios desafíos técnicos y conceptuales:

| Desafío | Solución adoptada |
|----------|------------------|
| **Evitar rutas inválidas (ciudades repetidas o faltantes)** | Se usó el cruce ordenado (OX1), diseñado específicamente para mantener la validez de las permutaciones. |
| **Convergencia prematura** | Se implementó una tasa de mutación moderada (5%) y un esquema de selección por torneo para mantener diversidad genética. |
| **Estabilidad del mejor individuo** | Se incluyó **elitismo**, asegurando que la mejor ruta nunca se pierda. |
| **Visualización de resultados** | Se integraron gráficas de ruta y de convergencia en el notebook, facilitando el análisis visual de los resultados. |

---

## 🧠 Conclusión

El **Algoritmo Genético** resultó ser una herramienta efectiva para abordar el **Problema del Viajero**.  
Aunque no garantiza la solución óptima absoluta, logra obtener rutas de alta calidad en tiempos computacionales razonables.  

Su flexibilidad, capacidad de adaptación y facilidad de implementación lo convierten en una opción robusta para resolver problemas complejos de optimización combinatoria.

---
