"""
experimento.py


Ejecuta el experimento definitivo utilizando tres estructuras:

    1. Lista
    2. ABB
    3. B+

Se estudian dos órdenes de inserción:

    - aleatorio
    - ordenado

Para cada combinación de:
    orden de inserción + N + estructura

se realizan 5 repeticiones.

Los valores de M utilizados para las búsquedas fueron seleccionados
previamente mediante una etapa de calibración.

Operaciones medidas:
    - inserción
    - búsqueda de M estudiantes
    - listado ordenado

Los resultados se guardan en:

    resultados/resultados_experimento.csv

También se guarda información del entorno utilizado para ejecutar
el experimento.
"""

import csv
import gc
import os
import platform
import random
import sys
import time

from estructuras import ListaEstudiantes, ABB, ArbolBPlus


# ============================================================
# CONFIGURACIÓN
# ============================================================

# El archivo siempre trabaja desde su propia carpeta.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CARPETA_RESULTADOS = "resultados"

REPETICIONES = 5

SEMILLA_BASE = 2026

# Tiempo mínimo utilizado para repetir inserción/listado.
# El profesor indicó que las mediciones deben ser, en su mayoría,
# superiores a 1 segundo.
TIEMPO_MIN = 1.0


# ------------------------------------------------------------
# PARÁMETROS DEFINITIVOS
# ------------------------------------------------------------
#
# Estos valores fueron seleccionados a partir de la calibración
# preliminar.
#
# No se busca que todos los tiempos sean idénticos ni que todas
# las estructuras superen obligatoriamente 1 s.
#
# En algunos casos B+ puede quedar por debajo de 1 s porque
# aumentar M produciría tiempos excesivos en Lista o ABB.
#

PARAMETROS = {
    "aleatorio": {
        10: 10_000_000,
        50: 10_000_000,
        100: 10_000_000,
        500: 5_000_000,
        1000: 5_000_000,
        2500: 5_000_000,
        5000: 5_000_000,
        10000: 2_000_000,
    },

    "ordenado": {
        10: 10_000_000,
        50: 10_000_000,
        100: 10_000_000,
        500: 10_000_000,
        1000: 5_000_000,
        2500: 20_000,
        5000: 10_000,
        10000: 5_000,
    }
}


# Las tres estructuras utilizan la misma interfaz.
ESTRUCTURAS = {
    "Lista": ListaEstudiantes,
    "ABB": ABB,
    "B+": lambda: ArbolBPlus(orden=32),
}


# ============================================================
# GENERACIÓN DE DATOS
# ============================================================

def generar_estudiantes(n, rng):
    """
    Genera n estudiantes con IDs únicos.

    Los IDs se seleccionan aleatoriamente del intervalo 1..10N.

    Retorna un diccionario:
        ID -> estudiante
    """

    ids = rng.sample(range(1, 10 * n + 1), n)

    estudiantes = {}

    for estudiante_id in ids:
        estudiantes[estudiante_id] = {
            "id": estudiante_id,
            "nombre": f"Estudiante_{estudiante_id}",
            "edad": rng.randint(17, 30),
            "promedio": round(rng.uniform(2.5, 5.0), 2)
        }

    return estudiantes


# ============================================================
# MEDICIÓN DE TIEMPOS
# ============================================================

def medir_una_vez(funcion):
    """
    Ejecuta una operación una sola vez.

    Retorna:
        tiempo_total
    """

    gc.collect()
    gc.disable()

    inicio = time.perf_counter()

    funcion()

    tiempo_total = time.perf_counter() - inicio

    gc.enable()

    return tiempo_total


def medir_hasta_un_segundo(funcion):
    """
    Repite una operación hasta acumular al menos 1 segundo.

    Esto se utiliza para inserción y listado, donde no tiene
    sentido utilizar M porque la operación trabaja sobre N
    estudiantes.

    Retorna:
        tiempo_total
        numero_de_ejecuciones
    """

    gc.collect()
    gc.disable()

    inicio = time.perf_counter()
    ejecuciones = 0

    while True:

        funcion()
        ejecuciones += 1

        tiempo_total = time.perf_counter() - inicio

        if tiempo_total >= TIEMPO_MIN:
            break

    gc.enable()

    return tiempo_total, ejecuciones


# ============================================================
# CONSTRUCCIÓN DE UNA ESTRUCTURA
# ============================================================

def construir_estructura(fabrica, estudiantes):
    """
    Construye una estructura e inserta todos los estudiantes.

    No se utiliza para medir directamente.
    """

    estructura = fabrica()

    for estudiante in estudiantes:
        estructura.insertar(estudiante)

    return estructura


# ============================================================
# INFORMACIÓN DEL ENTORNO
# ============================================================

def guardar_entorno():
    """
    Guarda información del hardware/software utilizado.
    """

    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    ruta = os.path.join(
        CARPETA_RESULTADOS,
        "entorno_experimento.txt"
    )

    with open(ruta, "w", encoding="utf-8") as archivo:

        archivo.write("LABORATORIO 3 - ENTORNO DEL EXPERIMENTO\n")
        archivo.write("=" * 60 + "\n\n")

        archivo.write(
            f"Sistema operativo: {platform.platform()}\n"
        )

        archivo.write(
            f"Procesador reportado por Python: "
            f"{platform.processor()}\n"
        )

        archivo.write(
            f"Núcleos lógicos: {os.cpu_count()}\n"
        )

        archivo.write(
            f"Python: {sys.version}\n"
        )

        archivo.write(
            f"Repeticiones: {REPETICIONES}\n"
        )

        archivo.write(
            f"Semilla base: {SEMILLA_BASE}\n"
        )

        archivo.write(
            f"Tiempo mínimo para inserción/listado: "
            f"{TIEMPO_MIN} s\n"
        )

        archivo.write(
            "Orden del árbol B+: 32\n\n"
        )

        archivo.write("PARÁMETROS DE BÚSQUEDA\n")
        archivo.write("-" * 60 + "\n")

        for orden, valores in PARAMETROS.items():

            archivo.write(
                f"\nOrden de inserción: {orden}\n"
            )

            for n, m in valores.items():

                archivo.write(
                    f"N = {n:6d} | M = {m:,}\n"
                    .replace(",", ".")
                )


# ============================================================
# VERIFICACIÓN DE CORRECTITUD
# ============================================================

def verificar_correctitud(
    estructura,
    estudiantes,
    ids_busqueda,
    ids_ordenados,
    nombre_estructura
):
    """
    Verifica:

        1. El listado contiene todos los estudiantes.
        2. El listado está ordenado por ID.
        3. Las búsquedas devuelven el estudiante correcto.
        4. Una búsqueda inexistente devuelve None.
    """

    listado = estructura.listar_ordenado()

    ids_listados = [
        estudiante["id"]
        for estudiante in listado
    ]

    assert ids_listados == ids_ordenados, (
        f"Listado incorrecto en {nombre_estructura}"
    )

    # Verificamos una muestra de búsquedas.
    muestra = ids_busqueda[:200]

    for estudiante_id in muestra:

        resultado = estructura.buscar(estudiante_id)

        assert resultado is estudiantes[estudiante_id], (
            f"Búsqueda incorrecta en {nombre_estructura} "
            f"para ID={estudiante_id}"
        )

    # ID que sabemos que no existe.
    assert estructura.buscar(-1) is None, (
        f"La búsqueda de un ID inexistente falló "
        f"en {nombre_estructura}"
    )


# ============================================================
# EXPERIMENTO PRINCIPAL
# ============================================================

def ejecutar_experimento():

    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    guardar_entorno()

    ruta_csv = os.path.join(
        CARPETA_RESULTADOS,
        "resultados_experimento.csv"
    )

    with open(
        ruta_csv,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow([
            "estructura",
            "orden_insercion",
            "N",
            "M",
            "repeticion",
            "operacion",
            "tiempo_total_s",
            "tiempo_promedio_us",
            "ejecuciones",
            "altura"
        ])

        # ----------------------------------------------------
        # Orden de inserción
        # ----------------------------------------------------

        for orden, parametros_n in PARAMETROS.items():

            print("\n")
            print("=" * 70)
            print(
                f"ORDEN DE INSERCIÓN: {orden.upper()}"
            )
            print("=" * 70)

            # ------------------------------------------------
            # Tamaño N
            # ------------------------------------------------

            for n, m in parametros_n.items():

                print(
                    f"\nN = {n:,} | M = {m:,}"
                    .replace(",", ".")
                )

                # --------------------------------------------
                # Repeticiones
                # --------------------------------------------

                for repeticion in range(REPETICIONES):

                    print(
                        f"\n  Repetición "
                        f"{repeticion + 1}/{REPETICIONES}"
                    )

                    # Semilla diferente por N y repetición,
                    # pero reproducible.
                    semilla = (
                        SEMILLA_BASE
                        + 1000 * n
                        + repeticion
                    )

                    rng = random.Random(semilla)

                    # ----------------------------------------
                    # Generar datos
                    # ----------------------------------------

                    estudiantes = generar_estudiantes(
                        n,
                        rng
                    )

                    ids = list(estudiantes.keys())

                    ids_ordenados = sorted(ids)

                    # Orden de inserción.
                    if orden == "aleatorio":

                        ids_insercion = ids.copy()

                    else:

                        ids_insercion = ids_ordenados.copy()

                    estudiantes_insercion = [
                        estudiantes[i]
                        for i in ids_insercion
                    ]

                    # ----------------------------------------
                    # Generar búsquedas
                    # ----------------------------------------
                    #
                    # Se generan exactamente las mismas
                    # búsquedas para las tres estructuras.
                    #

                    ids_busqueda = rng.choices(
                        ids,
                        k=m
                    )

                    # ----------------------------------------
                    # ESTRUCTURAS
                    # ----------------------------------------

                    for nombre, fabrica in ESTRUCTURAS.items():

                        print(
                            f"    {nombre}"
                        )

                        # ====================================
                        # INSERCIÓN
                        # ====================================

                        estructura = None

                        def construir():

                            nonlocal estructura

                            estructura = fabrica()

                            for estudiante in estudiantes_insercion:
                                estructura.insertar(estudiante)

                        tiempo_insercion, ejecuciones = (
                            medir_hasta_un_segundo(
                                construir
                            )
                        )

                        altura = estructura.altura()

                        escritor.writerow([
                            nombre,
                            orden,
                            n,
                            "",
                            repeticion + 1,
                            "insercion",
                            f"{tiempo_insercion:.9f}",
                            "",
                            ejecuciones,
                            altura if altura is not None else ""
                        ])

                        # ====================================
                        # BÚSQUEDA
                        # ====================================

                        def buscar_todos():

                            for estudiante_id in ids_busqueda:
                                estructura.buscar(
                                    estudiante_id
                                )

                        tiempo_busqueda = medir_una_vez(
                            buscar_todos
                        )

                        tiempo_por_busqueda_us = (
                            tiempo_busqueda / m
                        ) * 1_000_000

                        escritor.writerow([
                            nombre,
                            orden,
                            n,
                            m,
                            repeticion + 1,
                            "busqueda",
                            f"{tiempo_busqueda:.9f}",
                            f"{tiempo_por_busqueda_us:.6f}",
                            1,
                            altura if altura is not None else ""
                        ])

                        # ====================================
                        # LISTADO
                        # ====================================

                        resultado_listado = None

                        def listar():

                            nonlocal resultado_listado

                            resultado_listado = (
                                estructura.listar_ordenado()
                            )

                        tiempo_listado, ejecuciones = (
                            medir_hasta_un_segundo(
                                listar
                            )
                        )

                        escritor.writerow([
                            nombre,
                            orden,
                            n,
                            "",
                            repeticion + 1,
                            "listado",
                            f"{tiempo_listado:.9f}",
                            "",
                            ejecuciones,
                            altura if altura is not None else ""
                        ])

                        # ====================================
                        # VERIFICACIÓN
                        # ====================================

                        verificar_correctitud(
                            estructura,
                            estudiantes,
                            ids_busqueda,
                            ids_ordenados,
                            nombre
                        )

                print(
                    f"\n  N={n:,} terminado."
                    .replace(",", ".")
                )

    print("\n")
    print("=" * 70)
    print("EXPERIMENTO TERMINADO")
    print("=" * 70)
    print(
        f"Resultados guardados en: {ruta_csv}"
    )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    ejecutar_experimento()