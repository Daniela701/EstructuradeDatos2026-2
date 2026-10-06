"""
calibrar.py

Objetivo:
    Determinar un valor de M (número de búsquedas) apropiado para cada
    combinación de:

        - orden de inserción: aleatorio / ordenado
        - tamaño N
        - N representa el número de estudiantes.
        - M representa el número de búsquedas.

El resultado se guarda en:

    resultados/calibracion.csv

"""

import csv
import os
import random
import time

from estructuras import ListaEstudiantes, ABB, ArbolBPlus


# ============================================================
# CONFIGURACIÓN
# ============================================================

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CARPETA_RESULTADOS = "resultados"
ARCHIVO_SALIDA = os.path.join(
    CARPETA_RESULTADOS,
    "calibracion.csv"
)

# Tamaños de entrada.
# Incluimos tamaños pequeños para estudiar costos constantes.
N_VALORES = [
    10,
    50,
    100,
    500,
    1000,
    2500,
    5000,
    10000
]

# Valores candidatos de M.
# Se prueban de menor a mayor hasta encontrar uno adecuado.
M_CANDIDATOS = [
    1_000,
    5_000,
    10_000,
    20_000,
    50_000,
    100_000,
    500_000,
    1_000_000,
    2_000_000,
    5_000_000,
    10_000_000,
    20_000_000
]

# El profesor indicó que la mayoría de los tiempos deben estar
# alrededor de 1 segundo o más.
TIEMPO_MINIMO = 1.0

# No queremos generar experimentos excesivamente largos.
TIEMPO_MAXIMO = 300.0

# Número de búsquedas utilizadas para estimar el costo de una búsqueda.
MUESTRA_CALIBRACION = 2_000

SEMILLA = 2026

ORDENES = (
    "aleatorio",
    "ordenado"
)

ESTRUCTURAS = {
    "Lista": ListaEstudiantes,
    "ABB": ABB,
    "B+": lambda: ArbolBPlus(orden=32)
}


# ============================================================
# GENERACIÓN DE DATOS
# ============================================================

def generar_estudiantes(n, rng):
    """
    Genera n estudiantes con IDs únicos.

    Los IDs se toman aleatoriamente del rango 1..10N.

    Retorna:
        diccionario {id: estudiante}
    """

    ids = rng.sample(
        range(1, 10 * n + 1),
        n
    )

    estudiantes = {}

    for estudiante_id in ids:
        estudiantes[estudiante_id] = {
            "id": estudiante_id,
            "nombre": f"Estudiante_{estudiante_id}",
            "edad": rng.randint(17, 30),
            "promedio": round(
                rng.uniform(2.5, 5.0),
                2
            )
        }

    return estudiantes


def preparar_datos(n, orden, semilla):
    """
    Genera los datos y determina el orden de inserción.

    Importante:
        Los mismos estudiantes se utilizan en ambos experimentos.
        Solo cambia el orden en que se insertan.
    """

    rng = random.Random(semilla)

    estudiantes = generar_estudiantes(n, rng)

    ids = list(estudiantes.keys())

    if orden == "ordenado":
        ids.sort()
    else:
        # Para el caso aleatorio dejamos el orden generado.
        pass

    datos = [
        estudiantes[i]
        for i in ids
    ]

    return estudiantes, ids, datos


# ============================================================
# CONSTRUCCIÓN DE ESTRUCTURAS
# ============================================================

def construir_estructura(fabrica, datos):
    """
    Construye una estructura insertando todos los estudiantes.
    """

    estructura = fabrica()

    for estudiante in datos:
        estructura.insertar(estudiante)

    return estructura


# ============================================================
# MEDICIÓN
# ============================================================

def medir_busquedas(estructura, ids_busqueda):
    """
    Mide el tiempo total de realizar todas las búsquedas.
    """

    inicio = time.perf_counter()

    for estudiante_id in ids_busqueda:
        estructura.buscar(estudiante_id)

    return time.perf_counter() - inicio


def costo_por_busqueda(estructura, ids_busqueda):
    """
    Calcula el costo promedio de una búsqueda.
    """

    tiempo_total = medir_busquedas(
        estructura,
        ids_busqueda
    )

    return tiempo_total / len(ids_busqueda)


# ============================================================
# ELECCIÓN DE M
# ============================================================

def elegir_m(tiempos_por_estructura):
    """
    Escoge el primer M cuyo tiempo máximo esté dentro del intervalo
    [1 s, 300 s].

    Usamos el máximo entre estructuras porque necesitamos que la
    estructura más lenta también tenga una medición suficientemente
    grande para ser visible.

    Si no existe un M perfecto:
        - preferimos uno >= 1 s
        - pero evitamos superar 300 s.
    """

    # Primero intentamos encontrar un M completamente adecuado.
    for m, tiempos in tiempos_por_estructura:
        minimo = min(tiempos)
        maximo = max(tiempos)

        if minimo >= TIEMPO_MINIMO and maximo <= TIEMPO_MAXIMO:
            return m, "ok"

    # Si no existe, buscamos uno donde al menos la estructura más lenta
    # supere 1 segundo sin superar 300 s.
    for m, tiempos in tiempos_por_estructura:
        maximo = max(tiempos)

        if maximo >= TIEMPO_MINIMO and maximo <= TIEMPO_MAXIMO:
            return m, "aceptable"

    # Si todos quedan por debajo de 1 s, elegimos el mayor M disponible.
    ultimo_m, ultimo_tiempos = tiempos_por_estructura[-1]

    if max(ultimo_tiempos) < TIEMPO_MINIMO:
        return ultimo_m, "menor_a_1s"

    # Si todos superan 300 s, elegimos el menor.
    return tiempos_por_estructura[0][0], "mayor_a_300s"


# ============================================================
# CALIBRACIÓN DE UNA COMBINACIÓN
# ============================================================

def calibrar_n_orden(n, orden):
    """
    Calibra un valor M para una combinación específica de N y orden.
    """

    semilla = SEMILLA + 1000 * n

    estudiantes, ids, datos = preparar_datos(
        n,
        orden,
        semilla
    )

    # Generamos una muestra fija de búsquedas.
    rng_busqueda = random.Random(
        SEMILLA + 5000 * n + (1 if orden == "aleatorio" else 2)
    )

    ids_busqueda = [
        rng_busqueda.choice(ids)
        for _ in range(MUESTRA_CALIBRACION)
    ]

    costos = {}

    print(
        f"\nN={n:>6} | orden={orden}",
        flush=True
    )

    # Construimos cada estructura una sola vez.
    for nombre, fabrica in ESTRUCTURAS.items():

        print(
            f"    Calibrando {nombre}...",
            flush=True
        )

        estructura = construir_estructura(
            fabrica,
            datos
        )

        costo = costo_por_busqueda(
            estructura,
            ids_busqueda
        )

        costos[nombre] = costo

        print(
            f"      {costo * 1e6:.4f} µs/búsqueda",
            flush=True
        )

    # Predecimos el tiempo para cada M candidato.
    candidatos = []

    for m in M_CANDIDATOS:

        tiempos = [
            costos[nombre] * m
            for nombre in ESTRUCTURAS
        ]

        candidatos.append(
            (m, tiempos)
        )

    m_elegido, estado = elegir_m(
        candidatos
    )

    tiempos_finales = {
        nombre: costos[nombre] * m_elegido
        for nombre in ESTRUCTURAS
    }

    print(
        f"    -> M elegido = {m_elegido:,}".replace(",", ".")
    )

    for nombre, tiempo in tiempos_finales.items():

        if tiempo < TIEMPO_MINIMO:
            marca = "<1s"
        elif tiempo > TIEMPO_MAXIMO:
            marca = ">5min"
        else:
            marca = "ok"

        print(
            f"       {nombre:<5}: "
            f"{tiempo:8.3f} s {marca}"
        )

    return {
        "orden_insercion": orden,
        "N": n,
        "M": m_elegido,
        "estado": estado,
        "tiempo_lista_s": tiempos_finales["Lista"],
        "tiempo_abb_s": tiempos_finales["ABB"],
        "tiempo_bplus_s": tiempos_finales["B+"]
    }


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    os.makedirs(
        CARPETA_RESULTADOS,
        exist_ok=True
    )

    print("=" * 70)
    print("LABORATORIO 3 - CALIBRACIÓN")
    print("=" * 70)

    resultados = []

    for orden in ORDENES:

        print("\n" + "=" * 70)
        print(
            f"ORDEN DE INSERCIÓN: {orden.upper()}"
        )
        print("=" * 70)

        for n in N_VALORES:

            resultado = calibrar_n_orden(
                n,
                orden
            )

            resultados.append(
                resultado
            )

    # --------------------------------------------------------
    # Guardar CSV
    # --------------------------------------------------------

    with open(
        ARCHIVO_SALIDA,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        campos = [
            "orden_insercion",
            "N",
            "M",
            "estado",
            "tiempo_lista_s",
            "tiempo_abb_s",
            "tiempo_bplus_s"
        ]

        writer = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        writer.writeheader()

        writer.writerows(
            resultados
        )

    print("\n" + "=" * 70)
    print("CALIBRACIÓN TERMINADA")
    print("=" * 70)

    print(
        f"\nArchivo generado:\n"
        f"    {ARCHIVO_SALIDA}"
    )

    print(
        "\nEste archivo debe conservarse en el repositorio."
    )


if __name__ == "__main__":
    main()