"""
test.py
=======
1) Pruebas unitarias: el Quadtree debe dar los mismos resultados que la
   fuerza bruta.
2) Visualizaciones (se guardan en la carpeta graficas/).
3) Análisis de las pruebas (se imprime al final).

Uso:  python test.py
"""

import os
import random
import unittest

import matplotlib
matplotlib.use("Agg")          # guarda las imágenes sin abrir ventanas
import matplotlib.pyplot as plt

from Quadtreetree import (
    medir_capacidad, buscar_radio, fuerza_bruta_radio,
    buscar_k_cercanos, fuerza_bruta_k_cercanos,
    generar_puntos
)

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficas")

TAMANO = 10000        # la ciudad mide 10.000 x 10.000 metros
RADIO = 500           # radio del enunciado: 500 metros
CANTIDAD = 10000      # puntos de entrega del enunciado


def contar_puntos(nodo):
    """Cuenta los puntos guardados en las hojas del árbol."""
    if nodo["hijos"] is None:
        return len(nodo["puntos"])
    return sum(contar_puntos(hijo) for hijo in nodo["hijos"])


def consultas_aleatorias(cantidad, semilla):
    random.seed(semilla)
    return [(random.uniform(0, TAMANO), random.uniform(0, TAMANO))
            for i in range(cantidad)]


# 1. PRUEBAS UNITARIAS

class TestQuadtree(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.puntos = generar_puntos(CANTIDAD, TAMANO, semilla=1)
        cls.arbol = medir_capacidad(cls.puntos, 0, TAMANO, 0, TAMANO, capacidad=8)

    def test_no_se_pierde_ningun_punto(self):
        self.assertEqual(contar_puntos(self.arbol), CANTIDAD)

    def test_radio_igual_a_fuerza_bruta(self):
        for x, y in consultas_aleatorias(100, 10):
            quadtree = buscar_radio(self.arbol, x, y, RADIO, [])
            bruta = fuerza_bruta_radio(self.puntos, x, y, RADIO)
            self.assertEqual(sorted(quadtree), sorted(bruta))

    def test_puntos_dentro_del_radio(self):
        x, y = 5000, 5000
        for px, py in buscar_radio(self.arbol, x, y, RADIO, []):
            self.assertLessEqual((px - x)**2 + (py - y)**2, RADIO**2)

    def test_punto_mas_cercano_igual_a_fuerza_bruta(self):
        # El punto más cercano es el caso k = 1
        for x, y in consultas_aleatorias(100, 11):
            quadtree = buscar_k_cercanos(self.arbol, x, y, 1, [])
            bruta = fuerza_bruta_k_cercanos(self.puntos, x, y, 1)
            self.assertEqual(len(quadtree), 1)
            self.assertEqual(quadtree, bruta)

    def test_k_cercanos_igual_a_fuerza_bruta(self):
        for k in (1, 3, 5, 10):
            for x, y in consultas_aleatorias(50, 12):
                quadtree = buscar_k_cercanos(self.arbol, x, y, k, [])
                bruta = fuerza_bruta_k_cercanos(self.puntos, x, y, k)
                self.assertEqual(quadtree, bruta)

    def test_k_cercanos_ordenados_por_distancia(self):
        vecinos = buscar_k_cercanos(self.arbol, 3000, 7000, 10, [])
        distancias = [v[0] for v in vecinos]
        self.assertEqual(distancias, sorted(distancias))

    def test_ubicacion_fuera_de_la_ciudad(self):
        x, y = -3000, 14000
        self.assertEqual(buscar_radio(self.arbol, x, y, RADIO, []), [])
        self.assertEqual(
            buscar_k_cercanos(self.arbol, x, y, 1, []),
            fuerza_bruta_k_cercanos(self.puntos, x, y, 1))

    def test_radio_cero_encuentra_el_punto_exacto(self):
        px, py = self.puntos[123]
        self.assertIn((px, py), buscar_radio(self.arbol, px, py, 0, []))

    def test_puntos_en_los_bordes_de_los_cuadrantes(self):
        # Malla de puntos: caen justo en las líneas que dividen los cuadrantes
        puntos = [(i * 500, j * 500) for i in range(21) for j in range(21)]
        arbol = medir_capacidad(puntos, 0, TAMANO, 0, TAMANO, capacidad=2)
        self.assertEqual(contar_puntos(arbol), len(puntos))
        self.assertEqual(
            sorted(buscar_radio(arbol, 5000, 5000, 1000, [])),
            sorted(fuerza_bruta_radio(puntos, 5000, 5000, 1000)))

    def test_puntos_repetidos(self):
        puntos = [(5.0, 5.0)] * 100 + [(1.0, 1.0), (9.0, 9.0)]
        arbol = medir_capacidad(puntos, 0, 10, 0, 10, capacidad=4)   # no se cuelga
        self.assertEqual(len(buscar_radio(arbol, 5, 5, 0.1, [])), 100)

    def test_k_mayor_que_la_cantidad_de_puntos(self):
        puntos = [(1, 1), (2, 2), (3, 3)]
        arbol = medir_capacidad(puntos, 0, 10, 0, 10)
        self.assertEqual(len(buscar_k_cercanos(arbol, 0, 0, 10, [])), 3)


# 2. VISUALIZACIONES

def grafica_radio(puntos, arbol, ubicacion, radio, archivo):
    """Círculo de búsqueda y puntos encontrados (vista general y zoom)."""
    encontrados = buscar_radio(arbol, ubicacion[0], ubicacion[1], radio, [])

    plt.figure(figsize=(14, 7))

    for numero, zoom in ((1, False), (2, True)):

        plt.subplot(1, 2, numero)

        plt.scatter([p[0] for p in puntos], [p[1] for p in puntos],
                    color="lightgray", s=5, label="Entregas")

        plt.scatter([p[0] for p in encontrados], [p[1] for p in encontrados],
                    color="green", s=15,
                    label="Puntos encontrados (%d)" % len(encontrados))

        plt.scatter(ubicacion[0], ubicacion[1], color="red", marker="x",
                    s=80, label="Ubicación de consulta")

        circulo = plt.Circle(ubicacion, radio, fill=False, color="blue",
                             linewidth=2, label="Radio de %d metros" % radio)
        plt.gca().add_patch(circulo)

        if zoom:
            margen = radio * 1.5
            plt.xlim(ubicacion[0] - margen, ubicacion[0] + margen)
            plt.ylim(ubicacion[1] - margen, ubicacion[1] + margen)
            plt.title("Zoom")
        else:
            plt.title("Búsqueda de puntos de entrega por radio")
            plt.legend(loc="upper right", fontsize=8)

        plt.xlabel("Coordenada X (metros)")
        plt.ylabel("Coordenada Y (metros)")
        plt.gca().set_aspect("equal")
        plt.grid()

    plt.savefig(os.path.join(CARPETA, archivo), dpi=120)
    plt.close()
    return encontrados


def grafica_cercanos(puntos, ubicacion, vecinos, titulo, archivo):
    """Ubicación y sus vecinos más cercanos (vista general y zoom).

    vecinos es una lista de (distancia_al_cuadrado, (x, y)).
    """
    plt.figure(figsize=(14, 7))

    for numero, zoom in ((1, False), (2, True)):

        plt.subplot(1, 2, numero)

        plt.scatter([p[0] for p in puntos], [p[1] for p in puntos],
                    color="lightgray", s=5, label="Entregas")

        for posicion, (d2, punto) in enumerate(vecinos, start=1):

            plt.plot([ubicacion[0], punto[0]], [ubicacion[1], punto[1]],
                     color="blue", linestyle="--", linewidth=1)

            plt.scatter(punto[0], punto[1], color="green", s=50, zorder=4)

            if zoom:
                plt.annotate("%d (%.0f m)" % (posicion, d2**0.5), punto,
                             textcoords="offset points", xytext=(5, 5),
                             fontsize=8)

        plt.scatter(ubicacion[0], ubicacion[1], color="red", marker="x",
                    s=100, zorder=5, label="Ubicación de consulta")

        # Solo para la leyenda
        plt.scatter([], [], color="green", s=50, label="Vecinos más cercanos")

        if zoom:
            margen = vecinos[-1][0] ** 0.5 * 2
            plt.xlim(ubicacion[0] - margen, ubicacion[0] + margen)
            plt.ylim(ubicacion[1] - margen, ubicacion[1] + margen)
            plt.title("Zoom")
        else:
            plt.title(titulo)
            plt.legend(loc="upper right", fontsize=8)

        plt.xlabel("Coordenada X (metros)")
        plt.ylabel("Coordenada Y (metros)")
        plt.gca().set_aspect("equal")
        plt.grid()

    plt.savefig(os.path.join(CARPETA, archivo), dpi=120)
    plt.close()


# 3. EJECUCIÓN: PRUEBAS + GRÁFICAS + ANÁLISIS

if __name__ == "__main__":

    os.makedirs(CARPETA, exist_ok=True)

    resultado = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestQuadtree))

    puntos = generar_puntos(CANTIDAD, TAMANO, semilla=42)
    arbol = medir_capacidad(puntos, 0, TAMANO, 0, TAMANO, capacidad=8)
    ubicacion = (5000, 5000)

    # --- Búsqueda por radio ---
    encontrados = grafica_radio(puntos, arbol, ubicacion, RADIO, "range_search.png")
    bruta_radio = fuerza_bruta_radio(puntos, ubicacion[0], ubicacion[1], RADIO)

    # --- Punto más cercano ---
    cercano = buscar_k_cercanos(arbol, ubicacion[0], ubicacion[1], 1, [])
    cercano_bruta = fuerza_bruta_k_cercanos(puntos, ubicacion[0], ubicacion[1], 1)
    grafica_cercanos(puntos, ubicacion, cercano,
                     "Punto de entrega más cercano", "punto_mas_cercano.png")

    # --- k vecinos más cercanos ---
    k = 5
    vecinos = buscar_k_cercanos(arbol, ubicacion[0], ubicacion[1], k, [])
    vecinos_bruta = fuerza_bruta_k_cercanos(puntos, ubicacion[0], ubicacion[1], k)
    grafica_cercanos(puntos, ubicacion, vecinos,
                     "%d puntos de entrega más cercanos" % k,
                     "vecinos_cercanos.png")

    texto = "\n".join([
        "",
        "ANÁLISIS DE LAS PRUEBAS",
        "-----------------------",
        "Pruebas ejecutadas: %d -> %s" % (
            resultado.testsRun,
            "todas pasan" if resultado.wasSuccessful() else "HAY FALLAS"),
        "El Quadtree devuelve lo mismo que la fuerza bruta (100 consultas "
        "aleatorias por prueba).",
        "Casos borde probados: puntos sobre las líneas de división, puntos "
        "repetidos, ubicación fuera de la ciudad, radio 0 y k mayor que n.",
        "",
        "Ejemplo con ubicación (%d, %d) metros:" % ubicacion,
        "- Radio de %d m: %d puntos (Quadtree) y %d (fuerza bruta) -> %s"
        % (RADIO, len(encontrados), len(bruta_radio),
           "coinciden" if sorted(encontrados) == sorted(bruta_radio)
           else "NO coinciden"),
        "- Punto más cercano a %.1f m -> %s"
        % (cercano[0][0] ** 0.5,
           "coincide con fuerza bruta" if cercano == cercano_bruta
           else "NO coincide"),
        "- %d vecinos más cercanos: el último está a %.1f m -> %s"
        % (k, vecinos[-1][0] ** 0.5,
           "coinciden con fuerza bruta" if vecinos == vecinos_bruta
           else "NO coinciden"),
        "",
        "Gráficas guardadas en graficas/: range_search.png, "
        "punto_mas_cercano.png, vecinos_cercanos.png",
    ])

    print(texto)

    with open(os.path.join(CARPETA, "analisis_pruebas.txt"), "w",
              encoding="utf-8") as archivo:
        archivo.write(texto + "\n")