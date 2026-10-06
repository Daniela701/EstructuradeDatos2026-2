# Laboratorio 3: Sistema de Búsqueda de Estudiantes

**Estudiante:** Daniela Andrea Gallego Díaz

Estudio experimental del comportamiento de tres estrategias de almacenamiento y búsqueda de estudiantes:

* **Lista**
* **Árbol Binario de Búsqueda (ABB)**
* **Árbol B+**

El objetivo es estudiar cómo cambia el tiempo de ejecución al variar el tamaño de los datos, el número de búsquedas y el orden en que se insertan los estudiantes, y comparar los resultados experimentales con la complejidad teórica de cada estructura.

---

## Problema

Se requiere administrar registros de estudiantes con los siguientes atributos:

* `id`
* `nombre`
* `edad`
* `promedio`

Las operaciones principales son:

1. Buscar un estudiante por su ID.
2. Insertar un estudiante.
3. Listar todos los estudiantes en orden ascendente de ID.

Para resolver el problema se implementan y comparan tres estructuras de datos: Lista, ABB y Árbol B+.

---

## Pregunta experimental

¿Cómo cambia el tiempo de ejecución de las operaciones de búsqueda, inserción y listado al aumentar el tamaño `N` de los datos, y cómo influye el orden de inserción de los IDs?

Para la búsqueda también se estudia el efecto del número `M` de búsquedas realizadas.

---

## Contenido del proyecto

| Archivo / carpeta      | Descripción                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------- |
| `estructuras.py`       | Implementación de Lista, ABB y Árbol B+                                                              |
| `calibrar.py`          | Etapa preliminar utilizada para determinar valores adecuados de `M` antes del experimento definitivo |
| `experimento.py`       | Ejecuta el experimento definitivo y guarda las mediciones                                            |
| `analisis.py`          | Calcula estadísticas y genera las gráficas                                                           |
| `resultados/`          | Resultados crudos, estadísticas, información del entorno y validaciones                              |
| `graficas/`            | Gráficas generadas automáticamente                                                                   |
| `GUIA_SUSTENTACION.md` | Material de apoyo para la sustentación                                                               |
| `CODIGO_HONOR.md`      | Código de honor y declaración de uso de herramientas de IA |

---

## Cómo repetir el experimento

Se requiere Python 3.8 o superior.

Instalar las dependencias:

```bash
pip install matplotlib numpy
```

Ejecutar el experimento:

```bash
python experimento.py
```

Después de finalizar:

```bash
python analisis.py
```

El archivo `calibrar.py` **no es necesario para ejecutar nuevamente el experimento**. Fue utilizado como etapa previa para determinar valores adecuados de `M`. Los valores seleccionados quedaron definidos explícitamente en `experimento.py`, de manera que el experimento definitivo sea reproducible.

Las semillas utilizadas son fijas (`SEMILLA_BASE = 2026`), por lo que los datos generados son reproducibles. Sin embargo, los tiempos de ejecución pueden variar dependiendo de la máquina y de la carga del sistema.

---

## Hardware y software utilizados

| Componente | Detalle |
| --- | --- |
| Equipo y procesador | MacBook Pro con chip Apple M1 Pro |
| Núcleos lógicos | 10 |
| Memoria RAM | 16 GB |
| Sistema operativo | macOS 26.6.2 (arm64) |
| Python | 3.12.7 (distribución Anaconda) |
| Librerías | matplotlib y numpy (versiones: 3.10.8 , 1.26.4) |

El detalle que registra el propio programa está en `resultados/entorno_experimento.txt`.

Durante la ejecución del experimento se recomienda cerrar otras aplicaciones y mantener el equipo conectado a la corriente para reducir la variabilidad.

---

# Diseño experimental

## Estructuras comparadas

Se comparan:

* Lista de Python.
* Árbol Binario de Búsqueda (ABB) no balanceado.
* Árbol B+ de orden 32.

El ABB no realiza balanceo automático. Por esta razón, su comportamiento depende fuertemente del orden de inserción.

El Árbol B+ mantiene una estructura balanceada y almacena los datos en sus hojas.

---

## Tamaños de entrada

Se utilizaron los siguientes valores de `N`:

### Inserción aleatoria

```text
N = 10, 50, 100, 500, 1000, 2500, 5000, 10000
```

### Inserción ordenada

```text
N = 10, 50, 100, 500, 1000, 2500, 5000, 10000
```

El número `M` de búsquedas se seleccionó previamente mediante `calibrar.py`.

Los valores definitivos utilizados por `experimento.py` son:

| Orden de inserción |     N |          M |
| ------------------ | ----: | ---------: |
| Aleatorio          |    10 | 10.000.000 |
| Aleatorio          |    50 | 10.000.000 |
| Aleatorio          |   100 | 10.000.000 |
| Aleatorio          |   500 |  5.000.000 |
| Aleatorio          |  1000 |  5.000.000 |
| Aleatorio          |  2500 |  5.000.000 |
| Aleatorio          |  5000 |  5.000.000 |
| Aleatorio          | 10000 |  2.000.000 |
| Ordenado           |    10 | 10.000.000 |
| Ordenado           |    50 | 10.000.000 |
| Ordenado           |   100 | 10.000.000 |
| Ordenado           |   500 | 10.000.000 |
| Ordenado           |  1000 |  5.000.000 |
| Ordenado           |  2500 |     20.000 |
| Ordenado           |  5000 |     10.000 |
| Ordenado           | 10000 |      5.000 |

**Nota sobre la calibración.** Los valores de `M` coinciden con los de `resultados/calibracion.csv`, excepto en **IDs aleatorios con N = 10000**: la calibración propuso `M = 10.000` (estado "aceptable"), pero con el costo medido por búsqueda eso habría dado mediciones de apenas unos milisegundos para ABB y B+. Por eso ese valor se subió manualmente a `M = 2.000.000`, y es el que usa `experimento.py`.

Estos valores fueron seleccionados buscando que las mediciones fueran suficientemente largas para reducir el ruido del reloj y del sistema, evitando al mismo tiempo tiempos excesivamente grandes.

Como el `M` utilizado puede ser diferente entre distintos valores de `N` y entre inserción aleatoria y ordenada, la comparación principal de búsqueda se realiza mediante el **tiempo promedio por búsqueda**.

No se comparan directamente los tiempos totales de una condición aleatoria con los de una condición ordenada cuando utilizan diferentes valores de `M`.

---

## Repeticiones

Cada combinación de:

* estructura,
* orden de inserción,
* tamaño `N`

se ejecuta **5 veces**.

Las repeticiones utilizan datos generados nuevamente con semillas reproducibles.

---

## Generación de datos

Para cada repetición se generan `N` IDs únicos mediante:

```python
random.sample(range(1, 10*N + 1), N)
```

Para cada estudiante también se generan:

* edad aleatoria entre 17 y 30;
* promedio aleatorio entre 2.5 y 5.0;
* nombre asociado al ID.

Para cada conjunto de datos se consideran dos órdenes de inserción:

### Aleatorio

Los IDs se insertan en el orden en que fueron generados.

### Ordenado

Los mismos IDs se ordenan de menor a mayor antes de insertarlos.

Esto permite estudiar específicamente cómo afecta el orden de inserción al ABB.

---

## Generación de búsquedas

Las búsquedas se generan seleccionando aleatoriamente IDs que existen en la estructura:

```python
rng.choices(ids, k=M)
```

Se permite repetición de IDs.

Dentro de cada repetición se utiliza la misma secuencia de búsquedas para las tres estructuras, de manera que la comparación sea justa.

Las búsquedas se generan fuera del intervalo cronometrado.

---

## Medición de tiempos

Se utiliza:

```python
time.perf_counter()
```

porque proporciona un reloj adecuado para medir intervalos de tiempo de ejecución.

No se mide cada búsqueda individualmente, ya que una búsqueda puede durar solamente unos pocos microsegundos. En su lugar, se mide el tiempo de un bloque de `M` búsquedas y posteriormente se calcula:

```text
tiempo promedio por búsqueda =
tiempo total / M
```

El recolector de basura se fuerza mediante `gc.collect()` antes de la medición y se desactiva durante el intervalo cronometrado para reducir pausas ocasionadas por el recolector.

La generación de datos y de búsquedas ocurre fuera del cronómetro.

---

## Medición de inserción y listado

Para inserción y listado no se utiliza `M`, ya que ambas operaciones dependen de `N`.

En estos casos se repite la operación completa hasta acumular al menos aproximadamente un segundo de ejecución.

Se registra además cuántas veces fue necesario repetirla.

En `resultados_experimento.csv` se guardan el tiempo total acumulado (`tiempo_total_s`, siempre cercano o superior a 1 s) y el número de ejecuciones (`ejecuciones`). `analisis.py` calcula el tiempo de **una** ejecución como `tiempo_total_s / ejecuciones`, y ese es el valor que se resume en las tablas y se grafica para inserción y listado.

---

## Estadísticas

Para cada combinación experimental se calculan:

* promedio;
* desviación estándar muestral;
* mediana;
* mínimo;
* máximo;
* coeficiente de variación;
* cantidad de posibles valores atípicos mediante IQR.

El coeficiente de variación se calcula como:

```text
CV = desviación estándar / promedio × 100
```

Los valores atípicos se identifican mediante:

```text
Q1 - 1.5 × IQR
Q3 + 1.5 × IQR
```

No se eliminan automáticamente.

Esto evita modificar artificialmente los resultados. Los valores detectados se reportan para poder evaluar la variabilidad de las mediciones.

También se calcula una pendiente empírica en escala log-log como herramienta descriptiva para estudiar el crecimiento observado. Esta pendiente no constituye por sí sola una demostración de la complejidad asintótica.

---

## Verificación de correctitud

Antes de considerar válida una medición se verifica que:

1. El listado contenga todos los estudiantes.
2. Los estudiantes estén ordenados por ID.
3. Las búsquedas realizadas encuentren el estudiante correcto.
4. Una búsqueda de un ID inexistente devuelva `None`.

Si una verificación falla, el programa detiene la ejecución mediante `assert`.

---

# Complejidad teórica esperada

| Estructura    | Búsqueda          | Inserción de 1 elemento | Listado ordenado      |
| ------------- | ----------------- | ----------------------- | --------------------- |
| Lista         | O(n)              | O(1) amortizado         | O(n log n) en general |
| ABB aleatorio | O(log n) promedio | O(log n) promedio       | O(n)                  |
| ABB ordenado  | O(n)              | O(n)                    | O(n)                  |
| B+            | O(log n)          | O(log n)                | O(n)                  |

En el ABB, la complejidad depende de su altura.

Con inserción aleatoria se espera una altura relativamente pequeña y un comportamiento promedio cercano a logarítmico.

Con inserción ordenada, el ABB puede degenerar hasta convertirse esencialmente en una cadena de nodos. En ese caso la altura puede aproximarse a `N` y las operaciones de búsqueda e inserción pasan a comportarse linealmente.

El Árbol B+ mantiene una altura pequeña mediante su mecanismo de división de nodos y balanceo, por lo que no debería presentar la misma degradación por inserción ordenada.

---

# Gráficas

Las gráficas se generan automáticamente en la carpeta `graficas/` (ya están incluidas en el repositorio, no hace falta correr el experimento para verlas). Todas tienen título, nombres de ejes con unidades y leyenda, y comparan las tres estructuras dentro de un mismo tipo de IDs. **Nunca se comparan directamente tiempos de IDs aleatorios con tiempos de IDs ordenados cuando usan valores distintos de M.**

| Archivo | Qué muestra |
| --- | --- |
| `01_busqueda_por_busqueda_{aleatorio,ordenado}_{lineal,logY}.png` | Tiempo promedio de **una** búsqueda (µs) vs N. Se entrega con eje Y lineal y logarítmico: la escala logarítmica permite ver las curvas del ABB y el B+ que en escala lineal quedan pegadas al eje |
| `02_tiempo_total_busqueda_{aleatorio,ordenado}.png` | Tiempo total de las M búsquedas (s) vs N, para verificar que las mediciones duren cerca de 1 s o más. M cambia con N, por eso no se usa para comparar crecimiento |
| `03_insercion_{aleatorio,ordenado}.png` | Tiempo de construir la estructura (insertar N estudiantes), por ejecución |
| `04_listado_{aleatorio,ordenado}.png` | Tiempo de listar los N estudiantes en orden ascendente, por ejecución |
| `05_altura_arboles.png` | Altura del ABB y del B+ vs N, con IDs aleatorios y ordenados |
| `06_tiempo_vs_altura_ABB.png` | Tiempo por búsqueda vs altura del ABB (ejes logarítmicos) |
| `07_razon_lista_{aleatorio,ordenado}.png` | Cuántas veces es más lenta la Lista que el ABB y el B+ al buscar; muestra desde qué N las diferencias son claras |

---

# Comparación con la teoría

Los resultados deben interpretarse considerando tanto la complejidad teórica como los costos constantes de las implementaciones.

Para la Lista se espera que el tiempo de búsqueda crezca aproximadamente de manera lineal con `N`.

Para el ABB con inserción aleatoria se espera un comportamiento promedio cercano a logarítmico.

Para el ABB con inserción ordenada se espera una degradación hacia comportamiento lineal debido a que el árbol no se balancea.

Para el B+ se espera un crecimiento mucho más lento que el de la Lista y una menor sensibilidad al orden de inserción.

Sin embargo, las mediciones corresponden a un rango finito de tamaños y están influenciadas por factores como Python, las implementaciones concretas y los costos constantes. Por esto, las gráficas se utilizan como evidencia experimental y no como una demostración matemática de complejidad.

---

# Resultados y conclusiones

Todos los valores son promedios de 5 repeticiones. Las tablas completas (promedio, desviación estándar, mediana, mínimo, máximo, coeficiente de variación y atípicos) están en `resultados/resumen_estadistico.csv`.

## Búsqueda (tiempo promedio por búsqueda)

| N | Orden | Lista | ABB | B+ |
| ---: | --- | ---: | ---: | ---: |
| 10 | aleatorio | 0.156 µs | 0.171 µs | 0.117 µs |
| 10000 | aleatorio | 88.6 µs | 0.925 µs | 0.323 µs |
| 10 | ordenado | 0.153 µs | 0.228 µs | 0.116 µs |
| 10000 | ordenado | 111.6 µs | 250.4 µs | 0.347 µs |

Pendientes log-log del tiempo de búsqueda contra N (`resultados/exponentes_empiricos.csv`):

| Estructura | IDs aleatorios | IDs ordenados |
| --- | ---: | ---: |
| Lista | 0.941 | 0.980 |
| ABB | 0.245 | 1.031 |
| B+ | 0.141 | 0.143 |

## Inserción (construir con N = 10000, tiempo por ejecución) y listado

| Operación | Orden | Lista | ABB | B+ |
| --- | --- | ---: | ---: | ---: |
| Inserción | aleatorio | 0.41 ms | 9.0 ms | 4.1 ms |
| Inserción | ordenado | 0.41 ms | 2147 ms | 3.4 ms |
| Listado | aleatorio | 1.28 ms | 0.68 ms | 0.045 ms |
| Listado | ordenado | 0.52 ms | 0.60 ms | 0.054 ms |

Pendientes log-log: inserción ABB ordenado = 1.98; las demás inserciones entre 0.94 y 1.19; listado entre 0.84 y 1.10.

## Respuestas a las preguntas del experimento

**¿Se comporta como predice la teoría?** En general sí. La Lista crece casi linealmente en búsqueda (pendientes 0.94 y 0.98). El ABB con IDs aleatorios y el B+ crecen muy lentamente (0.245 y 0.141), compatible con un comportamiento logarítmico. El ABB con IDs ordenados crece de forma lineal en búsqueda (1.03) y cuadrática en construcción (1.98). Las pendientes son una herramienta descriptiva en un rango finito de N, no una demostración de complejidad.

**¿Cuándo el ABB deja de ser O(log N)?** Cuando los IDs se insertan en orden creciente: como no se balancea, cada nodo nuevo va a la derecha y la altura es igual a N (gráfica 05). Con IDs aleatorios la altura fue de 6.4 con N = 10 y 32 con N = 10000, unas 2.4 veces log2(N). No se estudiaron entradas parcialmente ordenadas.

**¿Qué relación hay entre altura y tiempo?** Es aproximadamente proporcional. Con N = 10000, el ABB tarda unos 0.029 µs por nivel con IDs aleatorios y 0.025 µs por nivel con IDs ordenados: costos por nivel parecidos aunque la altura difiera unas 300 veces (gráfica 06).

**¿Qué ocurre con datos ordenados y qué diferencias hay respecto a los aleatorios?** El ABB es la única estructura que cambia drásticamente: con N = 10000, su búsqueda pasa de 0.93 µs a 250 µs (unas 270 veces más lenta) y su construcción de 9 ms a 2.15 s (unas 240 veces). La Lista y el B+ cambian muy poco en búsqueda; el B+ solo sube su altura de 3 a 4 niveles. La única diferencia notable de la Lista está en el listado (1.28 ms frente a 0.52 ms), que es compatible con que `sorted` aproveche datos ya ordenados; esa explicación no se verificó experimentalmente. Estas comparaciones se hacen sobre tiempos por operación, no sobre tiempos totales, porque M difiere entre ambos órdenes.

**¿Desde qué N se ven claramente las diferencias?** Con IDs aleatorios, la Lista tarda 5.6 veces lo que el B+ con N = 100 y 23 veces con N = 500; frente al ABB, 3.0 veces con N = 100 y 8.8 veces con N = 500. Con IDs ordenados, la Lista es entre 5 y 321 veces más lenta que el B+ desde N = 100 hasta N = 10000, mientras que el ABB es entre 2.0 y 2.4 veces más lento que la Lista a partir de N = 50.

**¿Hay costos constantes que igualen estructuras con entradas pequeñas?** Sí. Con N = 10, las tres estructuras tardan entre 0.12 y 0.23 µs por búsqueda, y la Lista es ligeramente más rápida que el ABB (razón Lista/ABB = 0.91 con IDs aleatorios). El ABB aleatorio supera a la Lista entre N = 10 y N = 50 (razón 1.67 con N = 50); el B+ ya era algo más rápido que la Lista con N = 10 (razón 1.3).

## Principales hallazgos

1. El B+ fue la estructura más rápida en búsqueda y la menos sensible al orden de inserción.
2. La Lista es la más rápida para insertar (solo agrega al final), pero la más lenta en búsqueda con IDs aleatorios: 275 veces más lenta que el B+ con N = 10000.
3. El ABB sin balanceo se degrada con IDs ordenados: altura N, búsqueda lineal y construcción cuadrática.
4. Con IDs ordenados el ABB llega a ser más lento que una Lista (unas 2.2 veces con N = 10000), por el costo de recorrer nodos.
5. Las diferencias entre estructuras son claras desde N del orden de 100 en adelante.

---

# Limitaciones

* Los tiempos absolutos dependen del hardware y del estado del sistema.
* El experimento se realiza en un único equipo.
* Python es un lenguaje interpretado y sus costos constantes pueden influir considerablemente en tamaños pequeños.
* `bisect` y `sorted` utilizan implementaciones internas eficientes, lo que puede favorecer a determinadas estructuras.
* Solo se estudian búsquedas exitosas.
* No se estudiaron búsquedas de IDs inexistentes.
* El máximo utilizado es `N = 10000`, por lo que no se observa el comportamiento para tamaños mucho mayores.
* El Árbol B+ utiliza orden 32; no se estudia el efecto de cambiar este parámetro.
* Se utilizan 5 repeticiones, suficientes para observar tendencias pero limitadas para realizar inferencias estadísticas más fuertes.
* Otros procesos ejecutándose en el sistema pueden introducir variabilidad en los tiempos.
* **40 de las 240 mediciones de búsqueda (8 de las 48 combinaciones) duran menos de 1 s:** B+ con IDs aleatorios y N = 500 (0.97 s) y N = 10000 (0.65 s), y, con IDs ordenados y N = 2500, 5000 y 10000, la Lista (≈ 0.5 s) y el B+ (entre 0.002 y 0.005 s). No se descartaron, y su coeficiente de variación es bajo (no pasa de 4.6 % en el B+), pero deben leerse con esa precaución. Subir M para llevarlas a 1 s habría hecho que el ABB con IDs ordenados superara el límite de 5 minutos en los N más grandes. El detalle está en `resultados/validacion_tiempos.txt`.
* El valor de `M` de IDs aleatorios con N = 10000 se ajustó manualmente respecto a la calibración (ver nota en "Tamaños de entrada").
* Como `M` cambia con `N`, el tiempo total de las búsquedas no sirve para comparar el crecimiento; por eso se usa el tiempo por búsqueda.

---

# Uso de Inteligencia Artificial

En este laboratorio utilicé la Inteligencia Artificial como herramienta de apoyo durante el desarrollo.

La utilicé para consultar conceptos relacionados con estructuras de datos, complejidad, diseño experimental y estadística aplicada a mediciones de tiempo, así como para generar y revisar una primera versión de los scripts de experimentación, análisis y documentación.

Las implementaciones de la Lista, el ABB y el Árbol B+ parten del código que yo había desarrollado previamente.

La IA se utilizó principalmente para ayudar a integrar estas implementaciones en un experimento reproducible, organizar las mediciones, generar estadísticas y producir las gráficas.

Yo revisé y ejecuté el código en mi propio equipo, verifiqué la correctitud de las estructuras, revisé los resultados obtenidos, comprobé las estadísticas y las gráficas y analicé la relación entre los resultados experimentales y la complejidad teórica.

La IA fue utilizada como herramienta de apoyo. La responsabilidad sobre el código final, los experimentos, los datos y las conclusiones me corresponde.