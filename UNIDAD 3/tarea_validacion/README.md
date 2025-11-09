# 🧬 Algoritmo Genético para el Problema TSP

Implementación completa de un **Algoritmo Genético** para resolver el **Problema del agente viajero** utilizando Python.

---

## 👨‍💻 Autores
Proyecto desarrollado por **Jesús Alberto Barraza Castro y Jesús Guadalupe Wong Camacho**  
TecNM Campus Culiacán — Ingeniería en Tecnologías de la Información y Comunicaciones  
2025

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Problema Resuelto](#-problema-resuelto)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Documentación Técnica](#-documentación-técnica)
- [Parámetros y Configuración](#-parámetros-y-configuración)
- [Correcciones Implementadas](#-correcciones-implementadas)
- [Resultados](#-resultados)

---

## 🎯 Descripción

El **Problema del agente viajero (TSP)** es un problema clásico de optimización combinatoria que busca encontrar la ruta más corta que visite todas las ciudades exactamente una vez y regrese al punto de origen.

Este proyecto implementa un **algoritmo genético** con las siguientes mejoras clave:

✅ **Detección de estancamiento**
✅ **Tasa de mutación adaptativa**
✅ **Reproducción mejorada** con mayor variabilidad genética  

---

## ✨ Características

### Componentes Principales

| Componente | Descripción | Estado |
|------------|-------------|--------|
| **Inicialización** | Generación de población aleatoria | ✅ |
| **Función de Aptitud** | Evaluación basada en distancia euclidiana | ✅ |
| **Selección** | Ruleta ponderada + Elitismo | ✅ |
| **Cruce (Crossover)** | Ordered Crossover (OX) | ✅ |
| **Mutación** | Swap Mutation adaptativa | ✅ |
| **Anti-estancamiento** | Reinicio parcial automático | ✅ |

---

## 🗺️ Problema Resuelto

### ¿Qué es el TSP?

Dado un conjunto de ciudades con sus coordenadas:
- Visitar cada ciudad **exactamente una vez**
- Regresar a la ciudad de origen
- **Minimizar** la distancia total recorrida

### Complejidad

Para `n` ciudades, existen `(n-1)!/2` rutas posibles:

| Ciudades | Rutas Posibles | Tiempo (fuerza bruta) |
|----------|----------------|----------------------|
| 5 | 12 | < 1 segundo |
| 10 | 181,440 | ~1 segundo |
| 15 | 43.5 mil millones | ~13 horas |
| 20 | 60.8 cuatrillones | ~1.9 millones de años |

Por esto, **los algoritmos heurísticos** como los genéticos son necesarios para problemas grandes.

---

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias

```bash
numpy>=1.21.0
pandas>=1.3.0
```

### Instalación Rápida

Clonar el repositorio e Instalar dependencias

---

## 💻 Uso Rápido

### Ejemplo Básico

```python
from tsp_genetico import Municipio, algoritmo_genetico

# Definir ciudades (latitud, longitud)
ciudades = [
    Municipio(40.4168, -3.7038),    # Madrid
    Municipio(41.3784, 2.1925),     # Barcelona
    Municipio(39.4699, -0.3763),    # Valencia
    Municipio(37.3891, -5.9845),    # Sevilla
]

# Ejecutar algoritmo
mejor_ruta, distancia = algoritmo_genetico(
    lista_ciudades=ciudades,
    tamano_poblacion=100,
    elite_size=10,
    tasa_mutacion=0.05,
    num_generaciones=500,
    verbose=True
)

print(f"Mejor distancia encontrada: {distancia:.2f}")
```

### Salida

```
============================================================
🧬 ALGORITMO GENÉTICO - PROBLEMA DEL VIAJANTE (TSP)
============================================================
Número de ciudades: 4
Tamaño de población: 100
Tamaño de élite: 10
Tasa de mutación inicial: 5.0%
Generaciones: 500
============================================================
Distancia inicial: 15.23
Generación   50: Distancia = 14.87 (Mejora: 2.36%)
Generación  100: Distancia = 14.52 (Mejora: 4.66%)
Generación  150: Distancia = 14.35 (Mejora: 5.78%)
...
============================================================
RESULTADO FINAL
Distancia final: 14.12
Mejora total: 7.29%
============================================================
```

---

## 📖 Documentación Técnica

### Clase `Municipio`

Representa una ciudad con coordenadas.

```python
class Municipio:
    def __init__(self, x: float, y: float)
    def distancia(self, otro_municipio: Municipio) -> float
```

**Ejemplo:**
```python
madrid = Municipio(40.4168, -3.7038)
barcelona = Municipio(41.3784, 2.1925)
dist = madrid.distancia(barcelona)  # Calcula distancia euclidiana
```

### Clase `Aptitud`

Evalúa la calidad de una ruta.

```python
class Aptitud:
    def distancia_ruta(self) -> float      # Distancia total
    def ruta_apta(self) -> float           # Fitness = 1/distancia
```


### Funciones Principales

#### 1. Inicialización

```python
crear_ruta(lista_municipios) -> List[Municipio]
poblacion_inicial(tamano, lista_municipios) -> List[List[Municipio]]
```

#### 2. Selección

```python
clasificacion_rutas(poblacion) -> List[Tuple[int, float]]
seleccion_rutas(poblacion_clasificada, elite_size) -> List[int]
```

**Método:** Ruleta ponderada + Elitismo

#### 3. Reproducción (Crossover)

```python
reproduccion(padre1, padre2) -> List[Municipio]
```

**Método:** Ordered Crossover (OX)

**Proceso:**
1. Seleccionar segmento aleatorio del Padre 1
2. Copiar segmento al hijo
3. Llenar con genes del Padre 2 (sin duplicados)

#### 4. Mutación

```python
mutacion(individuo, tasa_mutacion) -> List[Municipio]
```

**Método:** Swap Mutation (intercambio)

**Proceso:**
- Para cada gen, con probabilidad `tasa_mutacion`:
  - Intercambiar con otro gen aleatorio

#### 5. Algoritmo Principal

```python
algoritmo_genetico(
    lista_ciudades: List[Municipio],
    tamano_poblacion: int = 100,
    elite_size: int = 10,
    tasa_mutacion: float = 0.05,
    num_generaciones: int = 500,
    verbose: bool = True
) -> Tuple[List[Municipio], float]
```

---

## ⚙️ Parámetros y Configuración

### Guía de Parámetros

| Parámetro | Descripción | Rango | Recomendado |
|-----------|-------------|-------|-------------|
| `tamano_poblacion` | Número de individuos | 50-500 | 100 |
| `elite_size` | Mejores individuos preservados | 5-15% población | 10 |
| `tasa_mutacion` | Probabilidad de mutación | 0.01-0.10 | 0.05 |
| `num_generaciones` | Iteraciones del algoritmo | 100-2000 | 500 |

### Configuraciones Recomendadas por Tamaño

#### Problema Pequeño (5-10 ciudades)
```python
tamano_poblacion = 100
elite_size = 10
tasa_mutacion = 0.05
num_generaciones = 500
```

#### Problema Mediano (11-30 ciudades)
```python
tamano_poblacion = 150
elite_size = 15
tasa_mutacion = 0.04
num_generaciones = 1000
```

#### Problema Grande (31-100 ciudades)
```python
tamano_poblacion = 200
elite_size = 20
tasa_mutacion = 0.03
num_generaciones = 2000
```
---

## 🔧 Correcciones Implementadas

### Problema Original: Estancamiento Completo

**Síntoma observado:**
```
Distancia inicial: 21.99
Generación 500: 21.99 (Mejora: 0.0%)
```

### Causas Identificadas

#### 1. Elite Demasiado Grande ❌

**Antes:**
```python
elite_size = 20  # 20% de población
```

**Problema:** 
- 20 individuos nunca mutaban
- 80% de descendencia heredaba de los mismos 20
- Pérdida rápida de diversidad

**Después:** ✅
```python
elite_size = 10  # 10% de población
```

#### 2. Mutación muy baja ❌

**Antes:**
```python
tasa_mutacion = 0.01  # 1%
```

**Problema:**
- Probabilidad de NO mutar: (1-0.01)^6 = 94%
- Solo ~6% de individuos mutaban

**Después:** ✅
```python
tasa_mutacion = 0.05  # 5%
```

#### 3. Reproducción con Poca Variabilidad ❌

**Antes:**
```python
pool = random.sample(grupo, len(grupo))
hijo = reproduccion(pool[i], pool[len(grupo)-i-1])
```

**Problema:** Emparejamientos predecibles

**Después:** ✅
```python
pool_padres = random.sample(grupo, len(grupo))
pool_madres = random.sample(grupo, len(grupo))
hijo = reproduccion(pool_padres[i], pool_madres[(i+1) % len(grupo)])
```

#### 4. Mutación Adaptativa ✅

```python
if generaciones_sin_mejora > 50:
    tasa_mutacion_actual = min(tasa_mutacion * 3, 0.15)
```

**Beneficio:** Aumenta exploración automáticamente cuando hay estancamiento

#### 5. Reinicio Parcial ✅

```python
if generaciones_sin_mejora > 100:
    # Mantener élite + regenerar 50% aleatorio
    poblacion = mejores + nuevos_aleatorios
```

**Beneficio:** Restaura diversidad sin perder mejores soluciones

### Comparación de Resultados

| Métrica | Versión Original | Versión Corregida |
|---------|-----------------|-------------------|
| Mejora típica | 0-1% | 5-10% |
| Estancamiento | Gen 1-10 | Gen 300-400 |
| Diversidad final | Muy baja | Media-Alta |
| Robustez | Baja | Alta |

---

## 📊 Resultados

### Caso de Estudio: 15 Ciudades Europeas

**Ciudades:**
```python
# Crear lista de ciudades
    lista_ciudades = [
        Municipio(40.4168, -3.7038),    # Madrid, España
        Municipio(48.8566, 2.3522),     # París, Francia
        Municipio(41.9028, 12.4964),    # Roma, Italia
        Municipio(52.5200, 13.4050),    # Berlín, Alemania
        Municipio(51.5074, -0.1278),    # Londres, Reino Unido
        Municipio(40.6401, 22.9444),    # Tesalónica, Grecia
        Municipio(52.2297, 21.0122),    # Varsovia, Polonia
        Municipio(59.3293, 18.0686),    # Estocolmo, Suecia
        Municipio(48.2082, 16.3738),    # Viena, Austria
        Municipio(50.0755, 14.4378),    # Praga, República Checa
        Municipio(45.4642, 9.1900),     # Milán, Italia
        Municipio(53.3498, -6.2603),    # Dublín, Irlanda
        Municipio(60.1699, 24.9384),    # Helsinki, Finlandia
        Municipio(47.4979, 19.0402),    # Budapest, Hungría
        Municipio(37.9838, 23.7275),    # Atenas, Grecia
    ]
```

**Configuración:**
```python
tamano_poblacion = 100
elite_size = 10
tasa_mutacion = 0.05
num_generaciones = 500
```

**Resultados:**

| Métrica | Valor |
|---------|-------|
| Distancia inicial | 181.07 |
| Distancia final | 161.3755 |
| Mejora total | 10.88% |
| Generaciones sin mejora (máx) | 55 |

---
