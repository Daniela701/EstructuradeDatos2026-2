"""
Quadtree en 2D

Funciones:
  1-3. distribucion, hijos, medir_capacidad : construir el arbol
  4.   distancia_rectangulo                 : distancia minima a un cuadrante
  5-6. buscar_radio / fuerza_bruta_radio    : puntos dentro de un radio
  7-8. buscar_k_cercanos / fuerza_bruta_k_cercanos : los k puntos mas cercanos
       (con k = 1 es el punto de entrega mas cercano)
  9.   generar_puntos                       : los puntos de entrega

UNIDADES: coordenadas, radio y distancias en METROS (la ciudad mide
10.000 x 10.000 m). Las distancias internas van al cuadrado (sin raiz).

Un nodo es un diccionario: {"limites": (x_min, x_max, y_min, y_max),
                            "puntos": [...], "hijos": None o lista de 4 nodos}
"""

import random
import heapq

# 1. DISTRIBUIR LOS PUNTOS EN LOS CUATRO CUADRANTES

def distribucion(arbol, puntos, x_medio, y_medio):

    for x, y in puntos:

        # Cuadrante 1: superior izquierdo
        if x < x_medio and y >= y_medio:
            arbol[0].append((x, y))

        # Cuadrante 2: superior derecho
        elif x >= x_medio and y >= y_medio:
            arbol[1].append((x, y))

        # Cuadrante 3: inferior izquierdo
        elif x < x_medio and y < y_medio:
            arbol[2].append((x, y))

        # Cuadrante 4: inferior derecho
        else:
            arbol[3].append((x, y))


# 2. CREAR LOS CUATRO HIJOS DE UN NODO

def hijos(puntos, x_min, x_max, y_min, y_max,
          capacidad, profundidad):

    cuadrante = [[], [], [], []]

    x_medio = (x_min + x_max) / 2
    y_medio = (y_min + y_max) / 2

    distribucion(cuadrante, puntos, x_medio, y_medio)

    limites = [
        (x_min, x_medio, y_medio, y_max),
        (x_medio, x_max, y_medio, y_max),
        (x_min, x_medio, y_min, y_medio),
        (x_medio, x_max, y_min, y_medio)
    ]

    resultado = []

    for i in range(4):

        nodo = medir_capacidad(
            cuadrante[i], *limites[i],
            capacidad, profundidad + 1
        )

        resultado.append(nodo)

    return resultado


# 3. CONTROLAR LA CAPACIDAD DEL QUADTREE

def medir_capacidad(puntos, x_min, x_max, y_min, y_max,
                    capacidad=8, profundidad=0):

    nodo = {
        "limites": (x_min, x_max, y_min, y_max),
        "puntos": [],
        "hijos": None
    }

    if len(puntos) > capacidad and profundidad < 10:

        nodo["hijos"] = hijos(
            puntos, x_min, x_max, y_min, y_max,
            capacidad, profundidad
        )

    else:
        nodo["puntos"] = puntos

    return nodo


# 4. CALCULAR LA DISTANCIA MÍNIMA A UN RECTÁNGULO

def distancia_rectangulo(x, y, limites):

    x_min, x_max, y_min, y_max = limites

    dx = 0
    dy = 0

    if x < x_min:
        dx = x_min - x

    elif x > x_max:
        dx = x - x_max

    if y < y_min:
        dy = y_min - y

    elif y > y_max:
        dy = y - y_max

    return dx**2 + dy**2


# 5. BÚSQUEDA DE PUNTOS DENTRO DE UN RADIO

def buscar_radio(nodo, x, y, radio, vecinos):

    # Descartar cuadrantes fuera del radio
    if distancia_rectangulo(x, y, nodo["limites"]) > radio**2:
        return vecinos

    # Si es una hoja, revisar sus puntos
    if nodo["hijos"] is None:

        for px, py in nodo["puntos"]:

            distancia = (px - x)**2 + (py - y)**2

            if distancia <= radio**2:
                vecinos.append((px, py))

    # Si tiene hijos, revisar sus cuadrantes
    else:

        for hijo in nodo["hijos"]:
            buscar_radio(hijo, x, y, radio, vecinos)

    return vecinos


# 6. BÚSQUEDA POR RADIO CON FUERZA BRUTA

def fuerza_bruta_radio(puntos, x, y, radio):

    vecinos = []

    for px, py in puntos:

        distancia = (px - x)**2 + (py - y)**2

        if distancia <= radio**2:
            vecinos.append((px, py))

    return vecinos


# 7. BUSCAR LOS K PUNTOS MÁS CERCANOS CON QUADTREE (K = 1: EL MÁS CERCANO)

def buscar_k_cercanos(nodo, x, y, k, mejores):

    distancia = distancia_rectangulo(x, y, nodo["limites"])

    # Si ya hay k candidatos y este cuadrante no puede mejorar al peor, se descarta
    if len(mejores) == k and distancia > mejores[-1][0]:
        return mejores

    # Si es una hoja, probar sus puntos y quedarse con los k mejores
    if nodo["hijos"] is None:

        for px, py in nodo["puntos"]:

            distancia_punto = (px - x)**2 + (py - y)**2

            mejores.append((distancia_punto, (px, py)))

        mejores.sort()
        del mejores[k:]

    # Si tiene hijos, visitar primero el cuadrante más cercano a la ubicación
    else:

        hijos_ordenados = sorted(
            nodo["hijos"],
            key=lambda hijo: distancia_rectangulo(x, y, hijo["limites"])
        )

        for hijo in hijos_ordenados:
            buscar_k_cercanos(hijo, x, y, k, mejores)

    return mejores


# 8. BUSCAR LOS K PUNTOS MÁS CERCANOS CON FUERZA BRUTA

def fuerza_bruta_k_cercanos(puntos, x, y, k):

    distancias = []

    for px, py in puntos:

        distancia = (px - x)**2 + (py - y)**2

        distancias.append((distancia, (px, py)))

    return heapq.nsmallest(k, distancias)


# 9. GENERAR LOS PUNTOS DE ENTREGA

def generar_puntos(cantidad, tamano=10000, semilla=42):

    random.seed(semilla)

    puntos = []

    for i in range(cantidad):

        x = random.uniform(0, tamano)
        y = random.uniform(0, tamano)

        puntos.append((x, y))

    return puntos