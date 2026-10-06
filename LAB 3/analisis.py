"""
analisis.py

Analiza los resultados del experimento definitivo.

Entrada:
    resultados/resultados_experimento.csv

Salida:

    resultados/
        resumen_estadistico.csv
        exponentes_empiricos.csv
        resumen_tiempos.txt

    graficas/
        01_busqueda_por_busqueda_aleatorio_lineal.png
        01_busqueda_por_busqueda_aleatorio_logY.png
        01_busqueda_por_busqueda_ordenado_lineal.png
        01_busqueda_por_busqueda_ordenado_logY.png

        02_tiempo_total_busqueda_aleatorio.png
        02_tiempo_total_busqueda_ordenado.png

        03_insercion_aleatorio.png
        03_insercion_ordenado.png

        04_listado_aleatorio.png
        04_listado_ordenado.png

        05_altura_arboles.png
        06_tiempo_vs_altura_ABB.png
        07_razon_lista_aleatorio.png
        07_razon_lista_ordenado.png

La búsqueda se analiza principalmente mediante el tiempo
promedio por búsqueda, porque M cambia entre diferentes valores
de N.

Inserción y listado se repiten k veces hasta acumular >= 1 s; por eso
el tiempo de UNA ejecución es tiempo_total_s / ejecuciones. Los exponentes
log-log se calculan para búsqueda, inserción y listado.
"""

import csv
import os
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# CONFIGURACIÓN
# ============================================================

os.chdir(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RUTA_CSV = (
    "resultados/"
    "resultados_experimento.csv"
)

CARPETA_GRAFICAS = "graficas"

os.makedirs(
    CARPETA_GRAFICAS,
    exist_ok=True
)


ESTRUCTURAS = [
    "Lista",
    "ABB",
    "B+"
]

ORDENES = [
    "aleatorio",
    "ordenado"
]


# ============================================================
# LECTURA DE DATOS
# ============================================================

datos = []

with open(
    RUTA_CSV,
    "r",
    encoding="utf-8"
) as archivo:

    lector = csv.DictReader(archivo)

    for fila in lector:

        fila["N"] = int(fila["N"])

        fila["repeticion"] = int(
            fila["repeticion"]
        )

        fila["tiempo_total_s"] = float(
            fila["tiempo_total_s"]
        )

        if fila["M"]:
            fila["M"] = int(fila["M"])
        else:
            fila["M"] = None

        if fila["tiempo_promedio_us"]:
            fila["tiempo_promedio_us"] = float(
                fila["tiempo_promedio_us"]
            )
        else:
            fila["tiempo_promedio_us"] = None

        if fila["ejecuciones"]:
            fila["ejecuciones"] = int(
                fila["ejecuciones"]
            )
        else:
            fila["ejecuciones"] = None

        if fila["altura"]:
            fila["altura"] = int(
                fila["altura"]
            )
        else:
            fila["altura"] = None

        datos.append(fila)


# ============================================================
# AGRUPACIÓN
# ============================================================

# Para cada combinación guardamos todas las repeticiones.
#
# clave:
# (estructura, orden, operacion, N, M)

tiempos = defaultdict(list)

for fila in datos:

    clave = (
        fila["estructura"],
        fila["orden_insercion"],
        fila["operacion"],
        fila["N"],
        fila["M"]
    )

    # Inserción y listado se repiten k veces hasta acumular >= 1 s:
    # el tiempo de UNA ejecución es tiempo_total_s / ejecuciones.
    # Las búsquedas son una sola ejecución (ejecuciones = 1).
    tiempos[clave].append(
        fila["tiempo_total_s"] / fila["ejecuciones"]
    )


# Alturas.
alturas = defaultdict(list)

for fila in datos:

    if (
        fila["operacion"] == "insercion"
        and fila["altura"] is not None
    ):

        clave = (
            fila["estructura"],
            fila["orden_insercion"],
            fila["N"]
        )

        alturas[clave].append(
            fila["altura"]
        )


# ============================================================
# FUNCIONES ESTADÍSTICAS
# ============================================================

def estadisticas(valores):
    """
    Calcula estadísticas descriptivas.

    Valores atípicos:
        regla del rango intercuartílico (IQR).
    """

    valores = np.asarray(
        valores,
        dtype=float
    )

    q1, q3 = np.percentile(
        valores,
        [25, 75]
    )

    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    mascara_atipicos = (
        (valores < limite_inferior)
        |
        (valores > limite_superior)
    )

    cantidad_atipicos = int(
        np.sum(mascara_atipicos)
    )

    promedio = np.mean(valores)

    desviacion = (
        np.std(valores, ddof=1)
        if len(valores) > 1
        else 0.0
    )

    cv = (
        100 * desviacion / promedio
        if promedio > 0
        else 0.0
    )

    return {
        "repeticiones": len(valores),
        "promedio": promedio,
        "desv_est": desviacion,
        "mediana": np.median(valores),
        "minimo": np.min(valores),
        "maximo": np.max(valores),
        "cv": cv,
        "atipicos": cantidad_atipicos
    }


# ============================================================
# RESUMEN ESTADÍSTICO
# ============================================================

ruta_resumen = (
    "resultados/"
    "resumen_estadistico.csv"
)

with open(
    ruta_resumen,
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    escritor = csv.writer(archivo)

    escritor.writerow([
        "estructura",
        "orden_insercion",
        "operacion",
        "N",
        "M",
        "repeticiones",
        "promedio_s",
        "desv_est_s",
        "mediana_s",
        "minimo_s",
        "maximo_s",
        "cv_porcentaje",
        "atipicos_IQR"
    ])

    for clave in sorted(tiempos):

        estructura, orden, operacion, n, m = clave

        valores = tiempos[clave]

        e = estadisticas(valores)

        escritor.writerow([
            estructura,
            orden,
            operacion,
            n,
            "" if m is None else m,
            e["repeticiones"],
            f"{e['promedio']:.9f}",
            f"{e['desv_est']:.9f}",
            f"{e['mediana']:.9f}",
            f"{e['minimo']:.9f}",
            f"{e['maximo']:.9f}",
            f"{e['cv']:.2f}",
            e["atipicos"]
        ])


# ============================================================
# TIEMPO POR BÚSQUEDA
# ============================================================

busqueda_por_n = defaultdict(list)

for fila in datos:

    if fila["operacion"] != "busqueda":
        continue

    clave = (
        fila["estructura"],
        fila["orden_insercion"],
        fila["N"]
    )

    busqueda_por_n[clave].append(
        fila["tiempo_promedio_us"]
    )


# ============================================================
# RESUMEN DE TIEMPOS DE BÚSQUEDA
# ============================================================

ruta_tiempos = (
    "resultados/"
    "resumen_tiempos.txt"
)

with open(
    ruta_tiempos,
    "w",
    encoding="utf-8"
) as archivo:

    archivo.write(
        "RESUMEN DE TIEMPOS DE BÚSQUEDA\n"
    )

    archivo.write(
        "=" * 70 + "\n\n"
    )

    for orden in ORDENES:

        archivo.write(
            f"ORDEN DE INSERCIÓN: {orden.upper()}\n"
        )

        archivo.write(
            "-" * 70 + "\n"
        )

        for estructura in ESTRUCTURAS:

            claves = [
                clave
                for clave in busqueda_por_n
                if (
                    clave[0] == estructura
                    and clave[1] == orden
                )
            ]

            claves.sort(
                key=lambda x: x[2]
            )

            archivo.write(
                f"\n{estructura}\n"
            )

            for clave in claves:

                valores = (
                    busqueda_por_n[clave]
                )

                e = estadisticas(valores)

                n = clave[2]

                archivo.write(
                    f"N={n:6d} | "
                    f"promedio="
                    f"{e['promedio']:.4f} us | "
                    f"desv="
                    f"{e['desv_est']:.4f} us | "
                    f"CV="
                    f"{e['cv']:.2f}%\n"
                )

        archivo.write("\n")


# ============================================================
# VALIDACIÓN DEL REQUISITO DE 1 SEGUNDO
# ============================================================

busquedas_totales = []

for fila in datos:

    if fila["operacion"] == "busqueda":

        busquedas_totales.append(
            fila["tiempo_total_s"]
        )


cantidad_total = len(
    busquedas_totales
)

cantidad_mayor_1 = sum(
    t >= 1.0
    for t in busquedas_totales
)

cantidad_menor_1 = (
    cantidad_total
    - cantidad_mayor_1
)


with open(
    "resultados/"
    "validacion_tiempos.txt",
    "w",
    encoding="utf-8"
) as archivo:

    archivo.write(
        "VALIDACIÓN DE DURACIÓN DE LAS MEDICIONES\n"
    )

    archivo.write(
        "=" * 60 + "\n\n"
    )

    archivo.write(
        f"Total de mediciones de búsqueda: "
        f"{cantidad_total}\n"
    )

    archivo.write(
        f"Mediciones >= 1 s: "
        f"{cantidad_mayor_1}\n"
    )

    archivo.write(
        f"Mediciones < 1 s: "
        f"{cantidad_menor_1}\n"
    )

    archivo.write(
        f"Porcentaje >= 1 s: "
        f"{100 * cantidad_mayor_1 / cantidad_total:.2f}%\n"
    )

    archivo.write(
        f"Tiempo mínimo: "
        f"{min(busquedas_totales):.6f} s\n"
    )

    archivo.write(
        f"Tiempo máximo: "
        f"{max(busquedas_totales):.6f} s\n"
    )

    archivo.write("\n")

    archivo.write(
        "Las mediciones inferiores a 1 s no se eliminan "
        "automáticamente. Se conservan porque forman parte "
        "del experimento y permiten documentar los casos en "
        "los que aumentar M produciría costos excesivos en "
        "otras estructuras.\n"
    )


# ============================================================
# PENDIENTES LOG-LOG
# ============================================================

def obtener_serie_busqueda(
    estructura,
    orden
):
    """
    Devuelve:

        N
        tiempo promedio por búsqueda

    agrupando las cinco repeticiones.
    """

    x = []
    y = []

    claves = [
        clave
        for clave in busqueda_por_n
        if (
            clave[0] == estructura
            and clave[1] == orden
        )
    ]

    claves.sort(
        key=lambda x: x[2]
    )

    for clave in claves:

        valores = busqueda_por_n[clave]

        x.append(clave[2])
        y.append(
            np.mean(valores)
        )

    return (
        np.array(x, dtype=float),
        np.array(y, dtype=float)
    )


# ============================================================
# EXPONENTES EMPÍRICOS
# ============================================================

def interpretar_pendiente(pendiente):
    """Lectura descriptiva de una pendiente log-log (no es una demostración)."""
    if abs(pendiente) < 0.3:
        return "crecimiento cercano a O(log N)"
    if 0.7 <= pendiente <= 1.3:
        return "crecimiento cercano a O(N) u O(N log N)"
    if pendiente >= 1.7:
        return "crecimiento cercano a O(N^2)"
    return "crecimiento intermedio o diferente de las referencias"


ruta_exponentes = (
    "resultados/"
    "exponentes_empiricos.csv"
)

with open(
    ruta_exponentes,
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    escritor = csv.writer(archivo)

    escritor.writerow([
        "estructura",
        "orden_insercion",
        "operacion",
        "pendiente_log_log",
        "interpretacion"
    ])

    # ----------------------------------------
    # Búsqueda
    # ----------------------------------------

    for orden in ORDENES:

        for estructura in ESTRUCTURAS:

            x, y = obtener_serie_busqueda(
                estructura,
                orden
            )

            # Eliminamos puntos que no pueden
            # utilizarse en logaritmos.
            mascara = (
                (x > 0)
                &
                (y > 0)
            )

            x_validos = x[mascara]
            y_validos = y[mascara]

            if len(x_validos) >= 2:

                pendiente = np.polyfit(
                    np.log(x_validos),
                    np.log(y_validos),
                    1
                )[0]

                if abs(pendiente) < 0.3:
                    interpretacion = (
                        "crecimiento cercano a O(log N)"
                    )

                elif (
                    0.7
                    <= pendiente
                    <= 1.3
                ):
                    interpretacion = (
                        "crecimiento cercano a O(N)"
                    )

                else:
                    interpretacion = (
                        "crecimiento intermedio "
                        "o diferente de las referencias"
                    )

                escritor.writerow([
                    estructura,
                    orden,
                    "busqueda",
                    f"{pendiente:.3f}",
                    interpretacion
                ])

    # ----------------------------------------
    # Inserción y listado (tiempo de UNA ejecución)
    # ----------------------------------------

    for operacion in ("insercion", "listado"):

        for orden in ORDENES:

            for estructura in ESTRUCTURAS:

                puntos = sorted(
                    (clave[3], float(np.mean(valores)))
                    for clave, valores in tiempos.items()
                    if (
                        clave[0] == estructura
                        and clave[1] == orden
                        and clave[2] == operacion
                    )
                )

                if len(puntos) >= 2:

                    x_op = np.array([p[0] for p in puntos], dtype=float)
                    y_op = np.array([p[1] for p in puntos], dtype=float)

                    pendiente = np.polyfit(
                        np.log(x_op),
                        np.log(y_op),
                        1
                    )[0]

                    escritor.writerow([
                        estructura,
                        orden,
                        operacion,
                        f"{pendiente:.3f}",
                        interpretar_pendiente(pendiente)
                    ])


# ============================================================
# FUNCIONES PARA GRÁFICAS
# ============================================================

def guardar_figura(figura, nombre):

    figura.tight_layout()

    figura.savefig(
        os.path.join(
            CARPETA_GRAFICAS,
            nombre
        ),
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(figura)


def serie_operacion(
    estructura,
    orden,
    operacion
):
    """
    Devuelve N, promedio y desviación estándar
    para inserción o listado.
    """

    x = []
    y = []
    s = []

    claves = [
        clave
        for clave in tiempos
        if (
            clave[0] == estructura
            and clave[1] == orden
            and clave[2] == operacion
        )
    ]

    claves.sort(
        key=lambda x: x[3]
    )

    for clave in claves:

        valores = tiempos[clave]

        e = estadisticas(valores)

        x.append(clave[3])
        y.append(e["promedio"])
        s.append(e["desv_est"])

    return (
        np.array(x),
        np.array(y),
        np.array(s)
    )


# ============================================================
# 1. BÚSQUEDA: TIEMPO POR BÚSQUEDA VS N
# ============================================================
#
# Esta es una de las gráficas PRINCIPALES del laboratorio.
#
# Se usa tiempo por búsqueda porque M cambia con N.
#
# Se generan:
#   - escala lineal
#   - escala logarítmica en Y
#

for orden in ORDENES:

    for escala in [
        "lineal",
        "logY"
    ]:

        figura, ax = plt.subplots(
            figsize=(9, 6)
        )

        for estructura in ESTRUCTURAS:

            x, y = obtener_serie_busqueda(
                estructura,
                orden
            )

            ax.plot(
                x,
                y,
                marker="o",
                linewidth=1.8,
                label=estructura
            )

        if escala == "logY":

            ax.set_yscale("log")

        ax.set_xlabel(
            "Tamaño de entrada N (estudiantes)"
        )

        ax.set_ylabel(
            "Tiempo promedio por búsqueda (µs)"
        )

        ax.set_title(
            "Tiempo promedio por búsqueda vs N\n"
            f"IDs insertados en orden {orden}"
        )

        ax.legend(
            title="Estructura"
        )

        ax.grid(
            True,
            which="both",
            alpha=0.3
        )

        guardar_figura(
            figura,
            f"01_busqueda_por_busqueda_"
            f"{orden}_{escala}.png"
        )


# ============================================================
# 2. TIEMPO TOTAL DE M BÚSQUEDAS
# ============================================================

for orden in ORDENES:

    figura, ax = plt.subplots(
        figsize=(9, 6)
    )

    for estructura in ESTRUCTURAS:

        claves = [
            clave
            for clave in tiempos
            if (
                clave[0] == estructura
                and clave[1] == orden
                and clave[2] == "busqueda"
            )
        ]

        claves.sort(
            key=lambda x: x[3]
        )

        x = []
        y = []

        for clave in claves:

            valores = tiempos[clave]

            x.append(clave[3])
            y.append(
                np.mean(valores)
            )

        ax.plot(
            x,
            y,
            marker="o",
            label=estructura
        )

    ax.set_yscale("log")

    ax.set_xlabel(
        "Tamaño de entrada N (estudiantes)"
    )

    ax.set_ylabel(
        "Tiempo total de M búsquedas (s)"
    )

    ax.set_title(
        "Tiempo total de búsqueda vs N\n"
        f"IDs insertados en orden {orden}"
    )

    ax.legend(
        title="Estructura"
    )

    ax.grid(
        True,
        which="both",
        alpha=0.3
    )

    guardar_figura(
        figura,
        f"02_tiempo_total_busqueda_"
        f"{orden}.png"
    )


# ============================================================
# 3. INSERCIÓN
# ============================================================

for orden in ORDENES:

    figura, ax = plt.subplots(
        figsize=(9, 6)
    )

    for estructura in ESTRUCTURAS:

        x, y, s = serie_operacion(
            estructura,
            orden,
            "insercion"
        )

        ax.errorbar(
            x,
            y,
            yerr=s,
            marker="o",
            capsize=3,
            label=estructura
        )

    ax.set_yscale("log")

    ax.set_xlabel(
        "Tamaño de entrada N (estudiantes)"
    )

    ax.set_ylabel(
        "Tiempo promedio de construcción (s)"
    )

    ax.set_title(
        "Tiempo de inserción vs N\n"
        f"IDs insertados en orden {orden}"
    )

    ax.legend(
        title="Estructura"
    )

    ax.grid(
        True,
        which="both",
        alpha=0.3
    )

    guardar_figura(
        figura,
        f"03_insercion_{orden}.png"
    )


# ============================================================
# 4. LISTADO
# ============================================================

for orden in ORDENES:

    figura, ax = plt.subplots(
        figsize=(9, 6)
    )

    for estructura in ESTRUCTURAS:

        x, y, s = serie_operacion(
            estructura,
            orden,
            "listado"
        )

        ax.errorbar(
            x,
            y,
            yerr=s,
            marker="o",
            capsize=3,
            label=estructura
        )

    ax.set_yscale("log")

    ax.set_xlabel(
        "Tamaño de entrada N (estudiantes)"
    )

    ax.set_ylabel(
        "Tiempo promedio de listado (s)"
    )

    ax.set_title(
        "Tiempo de listado ordenado vs N\n"
        f"IDs insertados en orden {orden}"
    )

    ax.legend(
        title="Estructura"
    )

    ax.grid(
        True,
        which="both",
        alpha=0.3
    )

    guardar_figura(
        figura,
        f"04_listado_{orden}.png"
    )


# ============================================================
# 5. ALTURA DE LOS ÁRBOLES
# ============================================================

figura, ax = plt.subplots(
    figsize=(9, 6)
)

for estructura in [
    "ABB",
    "B+"
]:

    for orden in ORDENES:

        claves = [
            clave
            for clave in alturas
            if (
                clave[0] == estructura
                and clave[1] == orden
            )
        ]

        claves.sort(
            key=lambda x: x[2]
        )

        x = []
        y = []

        for clave in claves:

            x.append(clave[2])

            y.append(
                np.mean(
                    alturas[clave]
                )
            )

        ax.plot(
            x,
            y,
            marker="o",
            label=f"{estructura} - {orden}"
        )


ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlabel(
    "Tamaño de entrada N (estudiantes)"
)

ax.set_ylabel(
    "Altura del árbol (niveles)"
)

ax.set_title(
    "Altura de los árboles vs tamaño de entrada"
)

ax.legend()

ax.grid(
    True,
    which="both",
    alpha=0.3
)

guardar_figura(
    figura,
    "05_altura_arboles.png"
)


# ============================================================
# 6. TIEMPO DE BÚSQUEDA VS ALTURA DEL ABB
# ============================================================

figura, ax = plt.subplots(
    figsize=(9, 6)
)

for orden in ORDENES:

    hs = []
    ts = []

    x, y = obtener_serie_busqueda(
        "ABB",
        orden
    )

    for n, tiempo_us in zip(x, y):

        clave_altura = (
            "ABB",
            orden,
            int(n)
        )

        if clave_altura not in alturas:
            continue

        altura_promedio = np.mean(
            alturas[clave_altura]
        )

        hs.append(
            altura_promedio
        )

        ts.append(
            tiempo_us
        )

    ax.plot(
        hs,
        ts,
        marker="o",
        label=f"IDs {orden}"
    )


# Eje X también logarítmico: la altura del ABB aleatorio (~10-30) y la del
# ordenado (hasta 10000) difieren en órdenes de magnitud.
ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlabel(
    "Altura promedio del ABB (niveles)"
)

ax.set_ylabel(
    "Tiempo promedio por búsqueda (µs)"
)

ax.set_title(
    "Relación entre altura del ABB y tiempo de búsqueda"
)

ax.legend()

ax.grid(
    True,
    which="both",
    alpha=0.3
)

guardar_figura(
    figura,
    "06_tiempo_vs_altura_ABB.png"
)


# ============================================================
# 7. RAZÓN LISTA / ABB / B+
# ============================================================

for orden in ORDENES:

    figura, ax = plt.subplots(
        figsize=(9, 6)
    )

    x_lista, y_lista = obtener_serie_busqueda(
        "Lista",
        orden
    )

    for estructura in [
        "ABB",
        "B+"
    ]:

        x, y = obtener_serie_busqueda(
            estructura,
            orden
        )

        # Se supone que los N son iguales.
        if not np.array_equal(
            x_lista,
            x
        ):
            continue

        razon = (
            y_lista / y
        )

        ax.plot(
            x_lista,
            razon,
            marker="o",
            label=f"Lista / {estructura}"
        )

    ax.axhline(
        1,
        linestyle=":",
        label="Mismo tiempo"
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel(
        "Tamaño de entrada N (estudiantes)"
    )

    ax.set_ylabel(
        "Razón de tiempos"
    )

    ax.set_title(
        "Comparación relativa de tiempo de búsqueda\n"
        f"IDs insertados en orden {orden}"
    )

    ax.legend()

    ax.grid(
        True,
        which="both",
        alpha=0.3
    )

    guardar_figura(
        figura,
        f"07_razon_lista_{orden}.png"
    )


# ============================================================
# FINAL
# ============================================================

print("=" * 70)
print("ANÁLISIS TERMINADO")
print("=" * 70)

print(
    "\nArchivos generados:"
)

print(
    "  resultados/resumen_estadistico.csv"
)

print(
    "  resultados/exponentes_empiricos.csv"
)

print(
    "  resultados/resumen_tiempos.txt"
)

print(
    "  resultados/validacion_tiempos.txt"
)

print(
    "\nGráficas guardadas en: graficas/"
)
