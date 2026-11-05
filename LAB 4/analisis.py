"""
analisis.py
===========
Compara el Quadtree con la fuerza bruta (listas) y responde:
¿a partir de qué tamaño de datos el Quadtree es más rápido?

Uso:  python analisis.py     (tarda ~1-2 minutos; guarda graficas/analisis.png)
"""

import os
import random
import time
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from Quadtreetree import (
    medir_capacidad, buscar_radio, fuerza_bruta_radio,
    buscar_k_cercanos, fuerza_bruta_k_cercanos,
    generar_puntos
)

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficas")

TAMANO = 10000     # metros
RADIO = 500        # metros
K = 5              # vecinos más cercanos
TAMANOS = [
    5, 8, 10, 12, 15, 20, 25, 30, 40, 50,
    75, 100, 150, 200, 500, 1000, 2000,
    5000, 10000, 20000, 50000
]


def tiempo(funcion):
    tiempos = []

    for i in range(5):
        inicio = time.perf_counter()
        funcion()
        duracion = time.perf_counter() - inicio
        tiempos.append(duracion)

    return statistics.median(tiempos)


# 1. MEDIR TIEMPOS PARA CADA TAMAÑO DE DATOS

resultados = []   # (n, construir, radio_bruta, radio_arbol, cerc_bruta, cerc_arbol, k_bruta, k_arbol)

for n in TAMANOS:

    puntos = generar_puntos(n, TAMANO, semilla=n)

    random.seed(1)
    cantidad = max(20, min(100, 200000 // n))          # número de consultas
    consultas = [(random.uniform(0, TAMANO), random.uniform(0, TAMANO))
                 for i in range(cantidad)]

    construir = tiempo(
        lambda: medir_capacidad(puntos, 0, TAMANO, 0, TAMANO, capacidad=8))
    arbol = medir_capacidad(puntos, 0, TAMANO, 0, TAMANO, capacidad=8)

    # Tiempo PROMEDIO por consulta, en microsegundos
    radio_bruta = tiempo(lambda: [fuerza_bruta_radio(puntos, x, y, RADIO)
                                  for x, y in consultas]) / cantidad * 1e6
    radio_arbol = tiempo(lambda: [buscar_radio(arbol, x, y, RADIO, [])
                                  for x, y in consultas]) / cantidad * 1e6

    cerc_bruta = tiempo(lambda: [fuerza_bruta_k_cercanos(puntos, x, y, 1)
                                 for x, y in consultas]) / cantidad * 1e6
    cerc_arbol = tiempo(lambda: [buscar_k_cercanos(arbol, x, y, 1, [])
                                 for x, y in consultas]) / cantidad * 1e6

    k_bruta = tiempo(lambda: [fuerza_bruta_k_cercanos(puntos, x, y, K)
                              for x, y in consultas]) / cantidad * 1e6
    k_arbol = tiempo(lambda: [buscar_k_cercanos(arbol, x, y, K, [])
                              for x, y in consultas]) / cantidad * 1e6

    resultados.append((n, construir * 1e3, radio_bruta, radio_arbol,
                       cerc_bruta, cerc_arbol, k_bruta, k_arbol))


# 2. TABLA DE RESULTADOS

lineas = [
    "RESULTADOS (tiempo por consulta en microsegundos, radio = %d m, k = %d)"
    % (RADIO, K),
    "%7s %10s | %10s %10s | %10s %10s | %10s %10s" % (
        "n", "construir", "radio brut", "radio arb",
        "1-NN brut", "1-NN arb", "k-NN brut", "k-NN arb"),
]

for fila in resultados:
    lineas.append("%7d %9.2fms | %10.1f %10.1f | %10.1f %10.1f | %10.1f %10.1f"
                  % fila)


def cruce(columna_bruta, columna_arbol):
    """Primer n a partir del cual el árbol es siempre más rápido."""
    for i in range(len(resultados)):
        if all(f[columna_arbol] < f[columna_bruta] for f in resultados[i:]):
            return resultados[i][0]


fila = [f for f in resultados if f[0] == 10000][0]

lineas += [
    "",
    "El Quadtree es más rápido desde:",
    "- n = %s puntos en búsqueda por radio" % cruce(2, 3),
    "- n = %s puntos en punto más cercano" % cruce(4, 5),
    "- n = %s puntos en %d vecinos más cercanos" % (cruce(6, 7), K),
    "",
    "Con n = 10.000 (el caso del enunciado):",
    "- Radio:    %.0f us (bruta) vs %.0f us (árbol) -> %.0f veces más rápido"
    % (fila[2], fila[3], fila[2] / fila[3]),
    "- 1-NN:     %.0f us (bruta) vs %.0f us (árbol) -> %.0f veces más rápido"
    % (fila[4], fila[5], fila[4] / fila[5]),
    "- %d-NN:     %.0f us (bruta) vs %.0f us (árbol) -> %.0f veces más rápido"
    % (K, fila[6], fila[7], fila[6] / fila[7]),
    "- Construir el árbol tarda %.1f ms: se compensa tras unas %.0f consultas"
    " de radio." % (fila[1], fila[1] * 1e3 / (fila[2] - fila[3])),
    "",
    "DISCUSIÓN",
    "- La fuerza bruta revisa los n puntos en cada consulta: su tiempo crece",
    "  de forma lineal con n. El Quadtree descarta cuadrantes enteros, así que",
    "  su tiempo crece mucho más despacio.",
    "- Con muy pocos puntos (n <= 8, la capacidad de una hoja) el árbol es una",
    "  sola hoja, o sea fuerza bruta: ahí no hay ventaja y las diferencias son",
    "  ruido. Con decenas de puntos (radio) o alrededor de 100 (vecinos más",
    "  cercanos) el árbol ya gana y la diferencia aumenta con n.",
    "- buscar_k_cercanos visita primero el cuadrante más cercano a la",
    "  ubicación: así encuentra buenos candidatos pronto y puede descartar el",
    "  resto de cuadrantes. Con k = 1 es el punto más cercano.",
    "- El árbol se construye una sola vez. Como los datos son estáticos y se",
    "  hacen muchas consultas, ese costo se recupera rápido.",
    "- Si el radio fuera enorme (cubre casi toda la ciudad), el árbol tendría",
    "  que visitar casi todos los cuadrantes y perdería su ventaja.",
    "- Los tiempos exactos dependen de la máquina (ambos métodos están en",
    "  Python puro); lo que no cambia es la tendencia: lineal (bruta) frente",
    "  a casi plana (árbol).",
]

texto = "\n".join(lineas)
print(texto)

os.makedirs(CARPETA, exist_ok=True)
with open(os.path.join(CARPETA, "analisis_resultados.txt"), "w",
          encoding="utf-8") as archivo:
    archivo.write(texto + "\n")


# 3. GRÁFICA

ns = [f[0] for f in resultados]

plt.figure(figsize=(17, 5))

consultas_graficas = [
    (1, "Búsqueda por radio (%d m)" % RADIO, 2, 3),
    (2, "Punto más cercano", 4, 5),
    (3, "%d puntos más cercanos" % K, 6, 7),
]

for posicion, titulo, col_bruta, col_arbol in consultas_graficas:

    plt.subplot(1, 3, posicion)
    plt.loglog(ns, [f[col_bruta] for f in resultados], "o-", label="Fuerza bruta")
    plt.loglog(ns, [f[col_arbol] for f in resultados], "s-", label="Quadtree")
    plt.title(titulo)
    plt.xlabel("n (número de puntos)")
    plt.ylabel("tiempo por consulta (us)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()

plt.savefig(os.path.join(CARPETA, "analisis.png"), dpi=120)
plt.close()