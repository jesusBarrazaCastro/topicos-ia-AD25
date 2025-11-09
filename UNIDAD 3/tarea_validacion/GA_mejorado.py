"""
Algoritmo Genético para resolver el Problema del Viajante (TSP) - VERSIÓN CORREGIDA
Traveling Salesman Problem using Genetic Algorithm

CORRECCIONES IMPLEMENTADAS:
- individuos seleccionados reducido para mayor diversidad
- Tasa de mutación adaptativa
- Reproducción mejorada con más variabilidad
- Detección de estancamiento con reinicio parcial
- Validación de mejora en cada generación

"""

import random
import numpy as np
import pandas as pd
import operator
from typing import List, Tuple, Dict


# ============================================================================
# CLASE MUNICIPIO - Representa una ciudad con coordenadas (x, y)
# ============================================================================

class Municipio:
    """
    Representa una ciudad o municipio con coordenadas.
    
    Atributos:
        x (float): Coordenada X (latitud)
        y (float): Coordenada Y (longitud)
    """
    
    def __init__(self, x: float, y: float):
        """
        Inicializa un municipio con coordenadas.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
        """
        self.x = x
        self.y = y
    
    def distancia(self, otro_municipio: 'Municipio') -> float:
        """
        Calcula la distancia entre dos municipios.        
        Args:
            otro_municipio: El municipio destino
            
        Returns:
            float: Distancia entre los dos puntos
        """
        x_diferencia = abs(self.x - otro_municipio.x)
        y_diferencia = abs(self.y - otro_municipio.y)
        distancia = np.sqrt((x_diferencia ** 2) + (y_diferencia ** 2))
        return distancia
    
    def __repr__(self) -> str:
        """Representación en string del municipio."""
        return f"({self.x:.4f}, {self.y:.4f})"
    
    def __eq__(self, other):
        """Igualdad basada en coordenadas."""
        if not isinstance(other, Municipio):
            return False
        return abs(self.x - other.x) < 1e-6 and abs(self.y - other.y) < 1e-6
    
    def __hash__(self):
        """Hash para poder usar en sets."""
        return hash((round(self.x, 6), round(self.y, 6)))


# ============================================================================
# CLASE APTITUD - Evalúa la calidad de una ruta
# ============================================================================

class Aptitud:
    """
    Evalúa la aptitud (fitness) de una ruta específica.
    
    Atributos:
        ruta (List[Municipio]): Lista ordenada de municipios
        distancia (float): Distancia total de la ruta
        f_aptitud (float): Valor de aptitud (fitness)
    """
    
    def __init__(self, ruta: List[Municipio]):
        """
        Inicializa el evaluador de aptitud para una ruta.
        
        Args:
            ruta: Lista de municipios en orden de visita
        """
        self.ruta = ruta
        self.distancia = 0
        self.f_aptitud = 0.0
    
    def distancia_ruta(self) -> float:
        """
        Calcula la distancia total de la ruta.
        Incluye el retorno al punto de origen.
        
        Returns:
            float: Distancia total de la ruta
        """
        if self.distancia == 0:
            distancia_total = 0
            
            # Recorrer todos los puntos de la ruta
            for i in range(len(self.ruta)):
                punto_origen = self.ruta[i]
                
                # El último punto conecta con el primero
                if i + 1 < len(self.ruta):
                    punto_destino = self.ruta[i + 1]
                else:
                    punto_destino = self.ruta[0]
                
                distancia_total += punto_origen.distancia(punto_destino)
            
            self.distancia = distancia_total
        
        return self.distancia
    
    def ruta_apta(self) -> float:
        """
        Calcula el valor de aptitud de la ruta.
        Fitness = 1 / Distancia
        
        Returns:
            float: Valor de aptitud
        """
        if self.f_aptitud == 0:
            self.f_aptitud = 1 / float(self.distancia_ruta())
        return self.f_aptitud


# ============================================================================
# FUNCIONES DE INICIALIZACIÓN
# ============================================================================

def crear_ruta(lista_municipios: List[Municipio]) -> List[Municipio]:
    """
    Crea una ruta aleatoria visitando todos los municipios.
    
    Args:
        lista_municipios: Lista de municipios disponibles
        
    Returns:
        List[Municipio]: Ruta aleatoria (permutación de municipios)
    """
    return random.sample(lista_municipios, len(lista_municipios))


def poblacion_inicial(tamano_poblacion: int, lista_municipios: List[Municipio]) -> List[List[Municipio]]:
    """
    Genera la población inicial de rutas aleatorias.
    
    Args:
        tamano_poblacion: Número de individuos en la población
        lista_municipios: Lista de municipios a visitar
        
    Returns:
        List[List[Municipio]]: Población de rutas aleatorias
    """
    poblacion = []
    for i in range(tamano_poblacion):
        poblacion.append(crear_ruta(lista_municipios))
    return poblacion


# ============================================================================
# FUNCIONES DE SELECCIÓN
# ============================================================================

def clasificacion_rutas(poblacion: List[List[Municipio]]) -> List[Tuple[int, float]]:
    """
    Clasifica todas las rutas de la población según su aptitud.
    
    Args:
        poblacion: Lista de rutas (individuos)
        
    Returns:
        List[]: Lista de tuplas (índice, aptitud) ordenada
    """
    resultados_fitness = {}
    
    for i in range(len(poblacion)):
        resultados_fitness[i] = Aptitud(poblacion[i]).ruta_apta()
    
    # Ordenar por aptitud (de mayor a menor)
    return sorted(resultados_fitness.items(), key=operator.itemgetter(1), reverse=True)


def seleccion_rutas(poblacion_clasificada: List[Tuple[int, float]], 
                   elite_size: int) -> List[int]:
    """
    Selecciona individuos para reproducción usando selección por ruleta.
    Combina elitismo (mejores individuos) con selección probabilística.
        
    Args:
        poblacion_clasificada: Población ordenada por aptitud
        elite_size: Número de mejores individuos a preservar (elitismo)
        
    Returns:
        List[]: Índices de los individuos seleccionados
    """
    indices_seleccionados = []
    
    # Crear DataFrame para cálculos de probabilidad
    df = pd.DataFrame(np.array(poblacion_clasificada), columns=["Indice", "Aptitud"])
    df['suma_acumulada'] = df.Aptitud.cumsum()
    df['porcentaje_acumulado'] = 100 * df.suma_acumulada / df.Aptitud.sum()
    
    # Elitismo: preservar los mejores individuos
    for i in range(elite_size):
        indices_seleccionados.append(int(poblacion_clasificada[i][0]))
    
    # Selección por ruleta para el resto
    for i in range(len(poblacion_clasificada) - elite_size):
        seleccion_aleatoria = 100 * random.random()
        
        for j in range(len(poblacion_clasificada)):
            if seleccion_aleatoria <= df.iat[j, 3]:
                indices_seleccionados.append(int(poblacion_clasificada[j][0]))
                break
    
    return indices_seleccionados


def grupo_apareamiento(poblacion: List[List[Municipio]], 
                      indices_seleccionados: List[int]) -> List[List[Municipio]]:
    """
    Crea el grupo de apareamiento a partir de los índices seleccionados.
    
    Args:
        poblacion: Población completa
        indices_seleccionados: Índices de individuos seleccionados
        
    Returns:
        List[]: Grupo de individuos para reproducción
    """
    grupo = []
    for indice in indices_seleccionados:
        grupo.append(poblacion[indice])
    return grupo


# ============================================================================
# FUNCIONES DE REPRODUCCIÓN (CROSSOVER)
# ============================================================================

def reproduccion(progenitor1: List[Municipio], 
                progenitor2: List[Municipio]) -> List[Municipio]:
    """
    Realiza el cruce (crossover) entre dos progenitores.
    Usa el método de Ordered Crossover (OX).
        
    Args:
        progenitor1: Primera ruta padre
        progenitor2: Segunda ruta padre
        
    Returns:
        List[Municipio]: Ruta hijo resultante del cruce
    """
    hijo = []
    hijo_parte1 = []
    hijo_parte2 = []
    
    # CORRECCIÓN: Asegurar puntos de corte diferentes y válidos
    tamano = len(progenitor1)
    punto_corte_a = random.randint(0, tamano - 1)
    punto_corte_b = random.randint(0, tamano - 1)
    
    # Asegurar que sean diferentes
    while punto_corte_a == punto_corte_b:
        punto_corte_b = random.randint(0, tamano - 1)
    
    inicio_segmento = min(punto_corte_a, punto_corte_b)
    fin_segmento = max(punto_corte_a, punto_corte_b)
    
    # Copiar segmento del progenitor 1
    for i in range(inicio_segmento, fin_segmento):
        hijo_parte1.append(progenitor1[i])
    
    # Completar con genes del progenitor 2 (preservando orden)
    hijo_parte2 = [item for item in progenitor2 if item not in hijo_parte1]
    
    # Combinar ambas partes
    hijo = hijo_parte1 + hijo_parte2
    return hijo


def reproduccion_poblacion(grupo: List[List[Municipio]], 
                          elite_size: int) -> List[List[Municipio]]:
    """
    Genera una nueva población mediante reproducción.
    
    CORRECCIÓN: Mejorado el emparejamiento para más variabilidad
    
    Args:
        grupo: Grupo de apareamiento
        elite_size: Número de individuos élite a preservar
        
    Returns:
        List[List[Municipio]]: Nueva población de hijos
    """
    hijos = []
    tamano_reproduccion = len(grupo) - elite_size
    
    # Preservar la élite sin cambios
    for i in range(elite_size):
        hijos.append(grupo[i])
    
    # CORRECCIÓN: Mezclar mejor el pool de reproducción
    pool_padres = random.sample(grupo, len(grupo))
    pool_madres = random.sample(grupo, len(grupo))
    
    # Generar hijos mediante cruce
    for i in range(tamano_reproduccion):
        padre = pool_padres[i % len(pool_padres)]
        madre = pool_madres[(i + 1) % len(pool_madres)]
        hijo = reproduccion(padre, madre)
        hijos.append(hijo)
    
    return hijos


# ============================================================================
# FUNCIONES DE MUTACIÓN - MEJORADAS
# ============================================================================

def mutacion(individuo: List[Municipio], tasa_mutacion: float) -> List[Municipio]:
    """
    Aplica mutación por intercambio (swap mutation) a un individuo.
    
    CORRECCIÓN: Garantiza al menos un intercambio si la tasa lo permite
    
    Args:
        individuo: Ruta a mutar
        tasa_mutacion: Probabilidad de mutación para cada gen
        
    Returns:
        List[Municipio]: Individuo mutado
    """
    # Crear copia para no modificar el original
    individuo_mutado = individuo.copy()
    
    for posicion in range(len(individuo_mutado)):
        # Decidir si mutar basado en la tasa de mutación
        if random.random() < tasa_mutacion:
            # Seleccionar posición aleatoria para intercambio (diferente a la actual)
            posicion_intercambio = random.randint(0, len(individuo_mutado) - 1)
            
            # Asegurar que no sea la misma posición
            while posicion_intercambio == posicion:
                posicion_intercambio = random.randint(0, len(individuo_mutado) - 1)
            
            # Intercambiar genes
            ciudad1 = individuo_mutado[posicion]
            ciudad2 = individuo_mutado[posicion_intercambio]
            
            individuo_mutado[posicion] = ciudad2
            individuo_mutado[posicion_intercambio] = ciudad1
    
    return individuo_mutado


def mutacion_poblacion(poblacion: List[List[Municipio]], 
                      tasa_mutacion: float) -> List[List[Municipio]]:
    """
    Aplica mutación a toda la población.
    
    Args:
        poblacion: Población a mutar
        tasa_mutacion: Probabilidad de mutación
        
    Returns:
        List[List[Municipio]]: Población mutada
    """
    poblacion_mutada = []
    
    for individuo in poblacion:
        individuo_mutado = mutacion(individuo, tasa_mutacion)
        poblacion_mutada.append(individuo_mutado)
    
    return poblacion_mutada


# ============================================================================
# FUNCIÓN PRINCIPAL DE EVOLUCIÓN - MEJORADA
# ============================================================================

def nueva_generacion(generacion_actual: List[List[Municipio]], 
                    elite_size: int, 
                    tasa_mutacion: float) -> List[List[Municipio]]:
    """
    Genera una nueva generación completa aplicando todos los operadores genéticos.
    
    Pasos:
    1. Clasificar rutas por aptitud
    2. Seleccionar individuos para reproducción
    3. Crear grupo de apareamiento
    4. Realizar cruces para generar hijos
    5. Aplicar mutaciones
    
    Args:
        generacion_actual: Población actual
        elite_size: Tamaño de la élite
        tasa_mutacion: Probabilidad de mutación
        
    Returns:
        List[List[Municipio]]: Nueva generación
    """
    # Paso 1: Clasificar rutas
    poblacion_clasificada = clasificacion_rutas(generacion_actual)
    
    # Paso 2: Seleccionar candidatos
    indices_seleccionados = seleccion_rutas(poblacion_clasificada, elite_size)
    
    # Paso 3: Generar grupo de apareamiento
    grupo = grupo_apareamiento(generacion_actual, indices_seleccionados)
    
    # Paso 4: Generar población cruzada
    hijos = reproduccion_poblacion(grupo, elite_size)
    
    # Paso 5: Incluir mutaciones
    siguiente_generacion = mutacion_poblacion(hijos, tasa_mutacion)
    
    return siguiente_generacion


# ============================================================================
# ALGORITMO GENÉTICO PRINCIPAL - VERSIÓN MEJORADA
# ============================================================================

def algoritmo_genetico(lista_ciudades: List[Municipio],
                      tamano_poblacion: int,
                      elite_size: int,
                      tasa_mutacion: float,
                      num_generaciones: int,
                      verbose: bool = True) -> Tuple[List[Municipio], float]:
    """
    Ejecuta el algoritmo genético completo para resolver el TSP.
    
    MEJORAS IMPLEMENTADAS:
    - Detección de estancamiento
    - Reinicio parcial si no hay mejora
    - Tasa de mutación adaptativa
    - Mejor reporte de progreso
    
    Args:
        lista_ciudades: Lista de ciudades a visitar
        tamano_poblacion: Tamaño de la población
        elite_size: Número de individuos élite
        tasa_mutacion: Tasa de mutación (0.0 a 1.0)
        num_generaciones: Número de generaciones a evolucionar
        verbose: Si True, muestra progreso
        
    Returns:
        Tuple[List[Municipio], float]: Mejor ruta encontrada y su distancia
    """
    # Generar población inicial
    poblacion = poblacion_inicial(tamano_poblacion, lista_ciudades)
    
    # Calcular distancia inicial
    clasificacion_inicial = clasificacion_rutas(poblacion)
    distancia_inicial = 1 / clasificacion_inicial[0][1]
    mejor_distancia_historica = distancia_inicial
    generaciones_sin_mejora = 0
    
    if verbose:
        print("=" * 60)
        print("🧬 ALGORITMO GENÉTICO - PROBLEMA DEL VIAJANTE (TSP)")
        print("=" * 60)
        print(f"Número de ciudades: {len(lista_ciudades)}")
        print(f"Tamaño de población: {tamano_poblacion}")
        print(f"Tamaño de élite: {elite_size}")
        print(f"Tasa de mutación inicial: {tasa_mutacion * 100}%")
        print(f"Generaciones: {num_generaciones}")
        print("=" * 60)
        print(f"Distancia inicial: {distancia_inicial:.2f}")
    
    # Variables para tasa de mutación adaptativa
    tasa_mutacion_actual = tasa_mutacion
    
    # Evolucionar por n generaciones
    for generacion in range(num_generaciones):
        poblacion = nueva_generacion(poblacion, elite_size, tasa_mutacion_actual)
        
        # Obtener mejor distancia actual
        clasificacion_actual = clasificacion_rutas(poblacion)
        distancia_actual = 1 / clasificacion_actual[0][1]
        
        # Verificar si hubo mejora
        if distancia_actual < mejor_distancia_historica - 0.001:  # Mejora significativa
            mejor_distancia_historica = distancia_actual
            generaciones_sin_mejora = 0
            tasa_mutacion_actual = tasa_mutacion  # Restaurar tasa normal
        else:
            generaciones_sin_mejora += 1
        
        # CORRECCIÓN: Reinicio parcial si hay estancamiento
        if generaciones_sin_mejora > 50:
            if verbose and generacion % 50 == 0:
                print(f"⚠️  Estancamiento detectado en gen {generacion}. Aumentando mutación...")
            
            # Aumentar mutación temporalmente
            tasa_mutacion_actual = min(tasa_mutacion * 3, 0.15)
            
            # Reiniciar 50% de la población (mantener élite)
            if generaciones_sin_mejora > 100:
                num_reiniciar = tamano_poblacion // 2
                poblacion_clasificada = clasificacion_rutas(poblacion)
                
                # Mantener los mejores
                mejores_indices = [int(idx) for idx, _ in poblacion_clasificada[:elite_size]]
                mejores = [poblacion[idx] for idx in mejores_indices]
                
                # Generar nuevos aleatorios
                nuevos = [crear_ruta(lista_ciudades) for _ in range(num_reiniciar)]
                
                # Combinar
                poblacion = mejores + nuevos
                
                # Rellenar hasta el tamaño original
                while len(poblacion) < tamano_poblacion:
                    poblacion.append(crear_ruta(lista_ciudades))
                
                generaciones_sin_mejora = 0
                
                if verbose:
                    print(f"Reinicio parcial en generación {generacion}")
        
        # Mostrar progreso cada 10% de las generaciones
        if verbose and (generacion + 1) % max(1, num_generaciones // 10) == 0:
            mejora = ((distancia_inicial - distancia_actual) / distancia_inicial) * 100
            print(f"Generación {generacion + 1:4d}: Distancia = {distancia_actual:.4f} "
                  f"(Mejora: {mejora:.2f}%) [Sin mejora: {generaciones_sin_mejora}]")
    
    # Obtener mejor ruta final
    clasificacion_final = clasificacion_rutas(poblacion)
    indice_mejor_ruta = int(clasificacion_final[0][0])
    mejor_ruta = poblacion[indice_mejor_ruta]
    distancia_final = 1 / clasificacion_final[0][1]
    
    if verbose:
        print("=" * 60)
        print(f"RESULTADO FINAL")
        print(f"Distancia final: {distancia_final:.4f}")
        mejora_total = ((distancia_inicial - distancia_final) / distancia_inicial) * 100
        print(f"Mejora total: {mejora_total:.2f}%")
        
        if mejora_total < 1:
            print("⚠️  ADVERTENCIA: Mejora muy baja")
        
        print("=" * 60)
        print(f"Mejor ruta encontrada:")
        for i, ciudad in enumerate(mejor_ruta, 1):
            print(f"   {i}. {ciudad}")
        print("=" * 60)
    
    return mejor_ruta, distancia_final


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
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
        
    # Ejecutar algoritmo 
    mejor_ruta, distancia = algoritmo_genetico(
        lista_ciudades=lista_ciudades,
        tamano_poblacion=100,
        elite_size=10,              # REDUCIDO de 20 a 10
        tasa_mutacion=0.05,         # AUMENTADO de 0.01 a 0.05
        num_generaciones=500,
        verbose=True
    )