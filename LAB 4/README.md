# Quadtree 2D para logística de entregas

Sistema que responde dos preguntas sobre 10.000 puntos de entrega con coordenadas
`(x, y)` en **metros** (datos estáticos, generados aleatoriamente en una ciudad de 10 × 10 km):

1. ¿Qué puntos de entrega están a un radio de **500 m** de un punto dado?
2. ¿Cuál es el punto de entrega **más cercano** a una ubicación? (y los k más cercanos)

El Quadtree está implementado desde cero (sin `scipy` ni árboles ya hechos) y se compara con fuerza bruta usando listas.

## Estructura

| Archivo | Contenido |
|---|---|
| `Quadtreetree.py` | Quadtree 2D, búsquedas por radio y por cercanía, fuerza bruta y generador de puntos |
| `test.py` | Pruebas unitarias, visualizaciones y análisis de las pruebas |
| `analisis.py` | Métricas de rendimiento y discusión de resultados |
| `graficas/` | Gráficas y resultados generados |

## Uso

```bash
pip install matplotlib
python test.py        # pruebas + gráficas de verificación visual
python analisis.py    # comparación Quadtree vs fuerza bruta (~2 minutos)
```

```python
from Quadtreetree import medir_capacidad, buscar_radio, buscar_k_cercanos, generar_puntos

puntos = generar_puntos(10000)                                  # metros
arbol = medir_capacidad(puntos, 0, 10000, 0, 10000, capacidad=8)

buscar_radio(arbol, 5000, 5000, 500, [])        # puntos a 500 m o menos
buscar_k_cercanos(arbol, 5000, 5000, 1, [])     # el punto más cercano: [(distancia^2, (x, y))]
buscar_k_cercanos(arbol, 5000, 5000, 5, [])     # los 5 más cercanos
```

## Cómo funciona

- Cada nodo es un diccionario con sus `limites`, sus `puntos` y sus `hijos`.
- **Construcción** (`medir_capacidad`): si un cuadrante tiene más de 8 puntos se divide en 4 (superior izquierdo, superior derecho, inferior izquierdo, inferior derecho) y reparte sus puntos. La profundidad máxima es 10 para que los puntos repetidos no causen un bucle infinito.
- **Búsqueda por radio** (`buscar_radio`): se descarta todo cuadrante cuyo rectángulo queda a más de 500 m de la ubicación (`distancia_rectangulo`); solo se revisan los puntos de los cuadrantes restantes.
- **Punto más cercano y k más cercanos** (`buscar_k_cercanos`; con `k = 1` es el punto más cercano): se visita primero el cuadrante más cercano a la ubicación y se descartan los cuadrantes que no pueden mejorar al peor de los k candidatos actuales.
- **Unidades**: coordenadas, radio y distancias en metros. Las distancias internas se calculan al cuadrado para no usar raíz.

## Verificación

- 11 pruebas unitarias: el árbol devuelve lo mismo que la fuerza bruta (100 consultas aleatorias por prueba), incluyendo casos borde (puntos sobre las líneas de división, repetidos, ubicación fuera de la ciudad, radio 0, k mayor que n).
- Gráficas en `graficas/`:
  - `range_search.png`: círculo de 500 m y puntos encontrados (vista general y zoom).
  - `punto_mas_cercano.png`: ubicación y punto más cercano.
  - `vecinos_cercanos.png`: los 5 puntos más cercanos con su distancia en metros.
  - `analisis.png`: tiempos del árbol frente a fuerza bruta.

## Análisis comparativo

> **¿Para qué tamaño de datos el Quadtree comienza a ser más rápido que la fuerza bruta?**

Medido en Python (ambos métodos), tiempo promedio por consulta. Los valores exactos cambian de una ejecución a otra y según la máquina; los completos están en `graficas/analisis_resultados.txt`:

- **Búsqueda por radio**: el árbol gana desde unos **20 puntos**.
- **Punto más cercano**: desde unos **50 puntos**. **5 más cercanos**: desde unos **100 puntos**.
- Con n ≤ 8 el árbol es una sola hoja y equivale a fuerza bruta.
- Con **n = 10.000**: la búsqueda por radio es unas 30 veces más rápida, el punto más cercano unas 250 veces y los 5 más cercanos unas 200 veces.
- Construir el árbol con 10.000 puntos tarda ≈ 11–15 ms; se compensa tras unas 8 consultas de radio.
- La fuerza bruta crece linealmente con n; el árbol crece mucho más despacio.
