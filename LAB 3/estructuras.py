"""
estructuras.py
Tres estrategias de almacenamiento y búsqueda de estudiantes:
  1. ListaEstudiantes  -> lista de Python + búsqueda lineal
  2. ABB               -> árbol binario de búsqueda (sin balanceo)
  3. ArbolBPlus        -> árbol B+ (datos solo en hojas, hojas enlazadas)

Cada estudiante es un diccionario: {"id", "nombre", "edad", "promedio"}.
Las tres clases ofrecen la misma interfaz:
  insertar(estudiante), buscar(id), listar_ordenado()
"""
from bisect import bisect_left, bisect_right


# 1. LISTA
class ListaEstudiantes:
    def __init__(self):
        self.estudiantes = []

    def insertar(self, estudiante):          # O(1) amortizado
        self.estudiantes.append(estudiante)

    def buscar(self, id_buscado):            # O(n): recorre uno a uno
        for e in self.estudiantes:
            if e["id"] == id_buscado:
                return e
        return None

    def listar_ordenado(self):               # O(n log n): hay que ordenar
        return sorted(self.estudiantes, key=lambda e: e["id"])

    def altura(self):                        # no aplica a una lista
        return None


# 2. ABB
class NodoABB:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izquierda = None
        self.derecha = None


class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):          # O(h): h = altura
        nuevo = NodoABB(estudiante)
        if self.raiz is None:
            self.raiz = nuevo
            return
        actual = self.raiz
        while True:
            if estudiante["id"] < actual.estudiante["id"]:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    return
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    return
                actual = actual.derecha

    def buscar(self, id_buscado):            # O(h)
        actual = self.raiz
        while actual is not None:
            if id_buscado == actual.estudiante["id"]:
                return actual.estudiante
            elif id_buscado < actual.estudiante["id"]:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return None

    def listar_ordenado(self):               # O(n): recorrido inorden iterativo
        resultado, pila, actual = [], [], self.raiz
        while pila or actual:
            while actual:
                pila.append(actual)
                actual = actual.izquierda
            actual = pila.pop()
            resultado.append(actual.estudiante)
            actual = actual.derecha
        return resultado

    def altura(self):
        """Altura = número de niveles (recorrido por niveles, sin recursión)."""
        if self.raiz is None:
            return 0
        nivel, h = [self.raiz], 0
        while nivel:
            h += 1
            siguiente = []
            for nodo in nivel:
                if nodo.izquierda:
                    siguiente.append(nodo.izquierda)
                if nodo.derecha:
                    siguiente.append(nodo.derecha)
            nivel = siguiente
        return h


# 3. B+
class NodoBPlus:
    def __init__(self, hoja=False):
        self.hoja = hoja
        self.claves = []      # IDs
        self.valores = []     # estudiantes (solo en hojas)
        self.hijos = []       # hijos (solo en nodos internos)
        self.siguiente = None  # siguiente hoja (solo en hojas)


class ArbolBPlus:
    def __init__(self, orden=32):
        self.orden = orden
        self.raiz = NodoBPlus(hoja=True)

    def buscar(self, id_buscado):            # O(log n)
        actual = self.raiz
        while not actual.hoja:
            actual = actual.hijos[bisect_right(actual.claves, id_buscado)]
        pos = bisect_left(actual.claves, id_buscado)
        if pos < len(actual.claves) and actual.claves[pos] == id_buscado:
            return actual.valores[pos]
        return None

    def insertar(self, estudiante):          # O(log n)
        id_est = estudiante["id"]
        actual, camino = self.raiz, []
        while not actual.hoja:
            camino.append(actual)
            actual = actual.hijos[bisect_right(actual.claves, id_est)]

        pos = bisect_left(actual.claves, id_est)
        actual.claves.insert(pos, id_est)
        actual.valores.insert(pos, estudiante)

        if len(actual.claves) < self.orden:
            return

        # Dividir hoja llena en dos
        nueva = NodoBPlus(hoja=True)
        mitad = len(actual.claves) // 2
        nueva.claves = actual.claves[mitad:]
        nueva.valores = actual.valores[mitad:]
        actual.claves = actual.claves[:mitad]
        actual.valores = actual.valores[:mitad]
        nueva.siguiente = actual.siguiente
        actual.siguiente = nueva
        self._insertar_en_padre(camino, actual, nueva.claves[0], nueva)

    def _insertar_en_padre(self, camino, izquierda, clave, derecha):
        if not camino:                       # no hay padre: nueva raíz
            raiz = NodoBPlus()
            raiz.claves = [clave]
            raiz.hijos = [izquierda, derecha]
            self.raiz = raiz
            return

        padre = camino.pop()
        pos = bisect_left(padre.claves, clave)
        padre.claves.insert(pos, clave)
        padre.hijos.insert(pos + 1, derecha)

        if len(padre.hijos) <= self.orden:
            return

        # Dividir nodo interno
        mitad = len(padre.claves) // 2
        promovida = padre.claves[mitad]
        nuevo = NodoBPlus()
        nuevo.claves = padre.claves[mitad + 1:]
        nuevo.hijos = padre.hijos[mitad + 1:]
        padre.claves = padre.claves[:mitad]
        padre.hijos = padre.hijos[:mitad + 1]
        self._insertar_en_padre(camino, padre, promovida, nuevo)

    def listar_ordenado(self):               # O(n): recorre hojas enlazadas
        resultado, actual = [], self.raiz
        while not actual.hoja:
            actual = actual.hijos[0]
        while actual is not None:
            resultado.extend(actual.valores)
            actual = actual.siguiente
        return resultado

    def altura(self):
        h, actual = 1, self.raiz
        while not actual.hoja:
            actual = actual.hijos[0]
            h += 1
        return h
