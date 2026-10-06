# GUÍA PARA LA SUSTENTACIÓN

## Experimento de comparación: Lista, ABB y B+

---

# 1. ¿Cuál es el problema que estamos estudiando?

### Respuesta para la sustentación

> El objetivo del experimento es comparar experimentalmente el comportamiento de tres estructuras de datos: **lista, árbol binario de búsqueda, o ABB, y árbol B+**, principalmente para las operaciones de **inserción, búsqueda y listado**.
>
> Se busca observar cómo cambia el tiempo de ejecución cuando aumenta el tamaño de entrada y cómo influye el orden en que se insertan los datos.
>
> Finalmente, se comparan los resultados experimentales con las complejidades teóricas esperadas para determinar si el comportamiento observado es consistente con el análisis algorítmico.

---

# 2. ¿Qué variables se estudiaron?

Se analizaron principalmente dos factores:

### Estructura

* Lista
* ABB
* B+

### Orden de inserción

* Aleatorio
* Ordenado

Y se estudiaron tres operaciones:

* Inserción
* Búsqueda
* Listado

La principal variable medida fue:

> **El tiempo de ejecución**, tanto como tiempo total de la medición como tiempo promedio por ejecución.

También se registraron características estructurales, especialmente la **altura de los árboles**, porque permiten explicar por qué el tiempo de búsqueda cambia.

---

# 3. ¿Qué estructuras utilizaron?

## 3.1. Lista

Una lista almacena los elementos de manera secuencial.

### Búsqueda

Para encontrar un elemento, generalmente hay que recorrer la lista desde el principio hasta encontrarlo.

Por eso:

$$
O(N)
$$

en el caso general.

### Listado

Para recorrer todos los elementos:

$$
O(N)
$$

### Idea que debes recordar

> En una lista no aprovechamos una estructura jerárquica para descartar grandes cantidades de elementos, por lo que una búsqueda puede requerir recorrer una parte considerable de los elementos.

---

# 4. ABB — Árbol Binario de Búsqueda

Un ABB mantiene la propiedad:

* elementos menores → subárbol izquierdo;
* elementos mayores → subárbol derecho.

La búsqueda depende directamente de la **altura \(h\)** del árbol:

$$
O(h)
$$

Por eso:

* si está razonablemente balanceado → aproximadamente \(O(\log N)\);
* si está degenerado → \(O(N)\).

### Algo MUY importante

> **Un ABB no se balancea automáticamente.**

Por eso el orden de inserción es fundamental.

---

# 5. ¿Qué pasa con la inserción aleatoria en el ABB?

Cuando los elementos se insertan en un orden aleatorio, el ABB tiende a evitar la degeneración extrema.

No significa que quede perfectamente balanceado.

Por ejemplo:

$$
\log_2(10000)\approx13.3
$$

pero nuestras alturas son mayores que 13.

Sin embargo, siguen siendo muchísimo menores que 10.000.

Por eso esperamos un crecimiento mucho más lento que el lineal.

### Respuesta para sustentación

> Con inserción aleatoria, el ABB no queda necesariamente perfectamente balanceado, pero normalmente presenta una altura mucho menor que N. Por eso la búsqueda presenta un comportamiento promedio cercano al esperado para un árbol de búsqueda aproximadamente balanceado.

---

# 6. ¿Qué pasa con la inserción ordenada?

Este es uno de los resultados más importantes del experimento.

Si insertamos:

$$
1,2,3,4,5,6,\ldots
$$

el ABB puede convertirse prácticamente en una lista:

```text
1
 \
  2
   \
    3
     \
      4
       \
        5
```

La altura pasa a ser aproximadamente:

$$
h=N
$$

y como la búsqueda cuesta \(O(h)\), entonces:

$$
O(N)
$$

### Resultados observados

Para el ABB ordenado:

|     N | Altura |
| ----: | -----: |
|    50 |     50 |
|   100 |    100 |
|   500 |    500 |
|  1000 |   1000 |
|  2500 |   2500 |
|  5000 |   5000 |
| 10000 |  10000 |

Esto constituye una evidencia experimental muy fuerte de la degeneración del ABB.

---

# 7. Árbol B+

El B+ es un árbol de búsqueda balanceado y de múltiples caminos.

A diferencia del ABB:

* un nodo puede contener múltiples claves;
* puede tener muchos hijos;
* mantiene una altura pequeña;
* permanece balanceado;
* los nodos hoja contienen los registros y están enlazados para facilitar recorridos secuenciales.

Su búsqueda tiene complejidad teórica:

$$
O(\log N)
$$

y la inserción también presenta comportamiento logarítmico en términos de la altura.

El recorrido completo de todos los elementos es:

$$
O(N)
$$

### Idea clave

> El B+ mantiene su estructura balanceada incluso cuando cambia el orden en que llegan los datos.

---

# 8. ¿Por qué comparar ABB y B+?

### Respuesta

> Porque ambos son árboles de búsqueda que permiten realizar búsquedas eficientes, pero tienen propiedades estructurales diferentes.
>
> El ABB puede degenerarse dependiendo del orden de inserción, mientras que el B+ mantiene su estructura balanceada.
>
> Por eso el experimento permite estudiar no solamente qué estructura es más rápida, sino también cómo la forma de construir la estructura afecta su comportamiento.

---

# 9. ¿Qué tamaños de entrada utilizaron?

Se utilizaron:

$$
N=
10,\ 50,\ 100,\ 500,\ 1000,\ 2500,\ 5000,\ 10000
$$

Esto permite observar el comportamiento desde tamaños pequeños hasta 10.000 elementos.

### ¿Por qué esos tamaños?

> Se escogieron tamaños crecientes para poder observar tanto el comportamiento inicial como la tendencia a tamaños mayores. Los tamaños pequeños permiten observar el comportamiento cuando \(N\) es reducido y los tamaños grandes permiten diferenciar mejor los comportamientos lineales y sublineales.

---

# 10. ¿Por qué no utilizar siempre el mismo M?

Este punto es importante.

\(M\) representa el número de veces que se ejecuta una operación durante la medición.

Las operaciones individuales pueden ser extremadamente rápidas, especialmente en estructuras como el B+.

Por eso, para obtener un tiempo suficientemente grande y medible, se ajusta \(M\) según el tamaño y el costo de la operación.

### Respuesta

> \(M\) se ajustó de acuerdo con el tamaño de entrada y la operación para que el tiempo acumulado fuera suficientemente grande para realizar una medición estable. Si una operación es demasiado rápida, ejecutarla una sola vez produciría una medición muy sensible a la resolución del reloj y al ruido del sistema.

---

# 11. ¿Cuántas repeticiones hicieron?

Para cada configuración experimental se realizaron:

$$
\boxed{5\text{ repeticiones}}
$$

Pero debes diferenciar dos conceptos.

### Repeticiones experimentales

Son las cinco mediciones independientes:

```text
1
2
3
4
5
```

### Ejecuciones internas

Dentro de una medición se puede ejecutar la operación muchas veces.

Por ejemplo:

```text
M = millones de ejecuciones
```

Estas dos cantidades **no son lo mismo**.

### Respuesta

> Las cinco repeticiones son réplicas de la misma configuración experimental. En cambio, M representa cuántas veces se ejecuta la operación dentro de una medición para obtener un tiempo suficientemente grande y estable.

---

# 12. ¿Cómo se seleccionaron los parámetros?

Este punto debes mencionarlo brevemente porque forma parte de la metodología.

### Respuesta

> La selección de los parámetros no fue arbitraria. Primero se realizó una etapa de **calibración**, cuyos resultados quedaron registrados en el archivo de calibración. A partir de esa calibración se seleccionaron los parámetros utilizados posteriormente en el experimento definitivo, buscando que las mediciones fueran suficientemente estables y medibles.

### Si el profesor pregunta por qué hicieron calibración

> Porque antes de ejecutar el experimento definitivo era necesario determinar una configuración adecuada de los parámetros de medición, especialmente para evitar tiempos demasiado pequeños o mediciones poco estables.

### Si el profesor pregunta si los valores de M salieron exactamente de la calibración

> Casi todos sí. La excepción es el caso de IDs aleatorios con N = 10000: la calibración propuso M = 10.000, pero con el costo medido por búsqueda eso habría dado mediciones de apenas unos milisegundos para el ABB y el B+, así que lo aumenté manualmente a 2.000.000. Todo está documentado en el README.

---

# 13. ¿Cómo se generaron los datos?

Se utilizaron datos reproducibles mediante una semilla aleatoria.

La generación parte de elementos con información como:

```python
{
    "id": 1001 + i,
    "nombre": f"Estudiante_{i + 1}",
    "edad": random.randint(17, 30),
    "promedio": round(random.uniform(2.5, 5.0), 2)
}
```

Y se utilizó:

```python
random.seed(42)
```

### ¿Por qué utilizar una semilla?

Porque permite reproducir la misma secuencia de datos aleatorios.

### Respuesta

> Utilizamos una semilla fija, 42, para que la generación aleatoria fuera reproducible. De esta manera, si volvemos a ejecutar el experimento bajo las mismas condiciones, podemos obtener los mismos datos.

---

# 14. ¿Cómo se manejó el orden de inserción?

Se analizaron dos escenarios.

## Aleatorio

Los elementos se insertaron en un orden aleatorio.

## Ordenado

Los elementos se insertaron siguiendo un orden creciente.

### ¿Por qué?

Porque queremos observar cómo el orden afecta particularmente al ABB.

### Idea fundamental

> El conjunto de datos puede ser el mismo, pero cambiar el orden de inserción puede cambiar completamente la estructura interna de un ABB.

Esto es precisamente lo que muestran los resultados.

---

# 15. ¿Cómo se generaron las búsquedas?

Las búsquedas se realizaron utilizando valores pertenecientes al conjunto de datos.

Lo importante para la comparación es que las diferentes estructuras fueran sometidas a condiciones equivalentes.

Es decir:

> La comparación debe realizarse utilizando las mismas condiciones de búsqueda para las estructuras que se están comparando.

\(M\) representa el número de búsquedas realizadas durante la medición.

Por tanto:

$$
T_{\text{promedio}}
=
\frac{T_{\text{total}}}{M}
$$

y posteriormente se expresa en microsegundos cuando corresponde.

---

# 16. Ejemplo del cálculo del tiempo promedio

Para la lista aleatoria con:

$$
N=1000
$$

se obtuvo aproximadamente:

$$
T_{\text{total}}=47.03s
$$

y:

$$
M=5\,000\,000
$$

Entonces:

$$
\frac{47.03}{5\,000\,000}
$$

da aproximadamente:

$$
9.41\ \mu s
$$

que coincide con el resultado experimental cercano a:

$$
9.406545\ \mu s
$$

### ¿Qué demuestra esto?

Que el tiempo reportado por operación no es el tiempo total de la medición, sino el tiempo total distribuido entre las ejecuciones realizadas.

---

# 17. ¿Cómo se midió el tiempo?

Conceptualmente, el benchmark funciona así:

```text
inicio
    ejecutar la operación M veces
fin
```

Se calcula:

$$
T_{\text{total}}=fin-inicio
$$

y posteriormente:

$$
T_{\text{promedio}}
=
\frac{T_{\text{total}}}{M}
$$

Esto permite medir operaciones demasiado rápidas para ser apreciadas individualmente.

**Inserción y listado:** no tienen M, así que la operación completa (construir la estructura o listar los N estudiantes) se repite hasta acumular al menos 1 s. Se guarda el tiempo total y el número de ejecuciones, y el tiempo de una ejecución es `tiempo_total_s / ejecuciones`.

---

# 18. ¿Por qué en el CSV aparecen tantos tiempos cercanos a 1 segundo?

En `resultados_experimento.csv`, la columna `tiempo_total_s` de **inserción y listado** casi siempre vale entre 1.000 y 1.01 s. Eso es **por diseño**: esas dos operaciones no tienen un M que se pueda aumentar, así que se repiten una y otra vez hasta acumular al menos 1 segundo, y se guarda cuántas veces se repitieron en la columna `ejecuciones`.

El tiempo de **una** ejecución es:

$$
\text{tiempo de una ejecución} = \frac{\text{tiempo\_total\_s}}{\text{ejecuciones}}
$$

y eso es lo que `analisis.py` grafica y resume. Si se graficara el total sin dividir, todas las curvas quedarían planas en 1 s y no se vería ninguna diferencia entre estructuras ni entre tamaños.

### Respuesta

> El valor cercano a un segundo en el CSV es la ventana de medición: repito la operación hasta acumular 1 s para reducir el efecto de la resolución del reloj y del ruido. No es el costo de una operación. El costo de una ejecución es el tiempo total dividido entre el número de ejecuciones, y es lo que se grafica.

Las **búsquedas** son distintas: se miden en una sola ejecución de M búsquedas, y su duración depende de N y de M.

---

# 19. ¿Cómo se trataron los valores atípicos?

Aquí debes ser muy cuidadosa.

No debes afirmar que se eliminaron valores atípicos si el procedimiento no lo demuestra.

La respuesta correcta es:

> Se realizaron cinco repeticiones por configuración para observar la variabilidad de las mediciones. Los resultados se compararon entre repeticiones y se utilizaron estadísticas descriptivas. No se eliminaron automáticamente valores solamente por ser diferentes; para considerar un dato como atípico tendría que aplicarse un criterio estadístico explícito.

### Si el profesor pregunta:

**¿Por qué no eliminaron simplemente el valor más alto?**

> Porque una medición alta no necesariamente es un error. Puede deberse a actividad del sistema, procesos en segundo plano u otras fuentes de variabilidad. Eliminarla sin un criterio definido podría introducir sesgo.

---

# 20. ¿Qué estadísticas se analizaron?

La métrica principal es el tiempo promedio:

$$
\bar T=\frac{T_{\text{total}}}{M}
$$

Además, las cinco repeticiones permiten observar:

* promedio;
* mínimo;
* máximo;
* variabilidad;
* consistencia entre repeticiones.

La idea no es mirar únicamente un número aislado, sino observar la tendencia.

---

# 21. ¿Qué muestran los resultados de la lista?

Para búsqueda aleatoria, los tiempos aumentan aproximadamente de forma proporcional a \(N\).

Resultados representativos:

|     N | Tiempo aproximado |
| ----: | ----------------: |
|    10 |           0.15 μs |
|    50 |           0.49 μs |
|   100 |           1.00 μs |
|   500 |           4.48 μs |
|  1000 |           9.41 μs |
|  2500 |           23.1 μs |
|  5000 |           46.2 μs |
| 10000 |          89–90 μs |

Por ejemplo:

$$
N=5000\rightarrow46\mu s
$$

mientras:

$$
N=10000\rightarrow89\mu s
$$

Al duplicar aproximadamente \(N\), el tiempo también se duplica aproximadamente.

### Conclusión

El comportamiento experimental es consistente con:

$$
\boxed{O(N)}
$$

para la búsqueda secuencial.

---

# 22. ¿Qué ocurre con el ABB aleatorio?

Los resultados muestran un crecimiento mucho menor.

Resultados representativos:

|     N | Tiempo aproximado |
| ----: | ----------------: |
|    10 |           0.17 μs |
|    50 |           0.28 μs |
|   100 |           0.33 μs |
|   500 |      0.49–0.53 μs |
|  1000 |           0.62 μs |
|  2500 |      0.72–0.77 μs |
|  5000 |      0.83–0.88 μs |
| 10000 |      0.87–1.00 μs |

Mientras \(N\) aumenta considerablemente, el tiempo de búsqueda aumenta mucho menos que en la lista.

Esto se relaciona directamente con la altura del árbol.

Por ejemplo, para tamaños grandes se observaron alturas aproximadamente entre:

$$
29-35
$$

para \(N=10000\), en lugar de una altura cercana a 10.000.

### Conclusión

> El ABB aleatorio presenta un crecimiento mucho más lento que la lista y es consistente con el comportamiento esperado de un ABB cuya altura crece mucho más lentamente que N.

---

# 23. ¿Qué ocurre con el ABB ordenado?

Este es probablemente el resultado más fuerte de todo el experimento.

Cuando los datos se insertan ordenadamente:

$$
h=N
$$

prácticamente en los tamaños evaluados.

Por ejemplo:

```text
N = 500     → h = 500
N = 1000    → h = 1000
N = 2500    → h = 2500
N = 5000    → h = 5000
N = 10000   → h = 10000
```

El árbol se convierte prácticamente en una lista.

### ¿Qué sucede con la búsqueda?

Los tiempos también aumentan aproximadamente de forma lineal.

Ejemplos:

$$
N=500\rightarrow10.2\mu s
$$

$$
N=1000\rightarrow22.9\mu s
$$

$$
N=5000\rightarrow119\mu s
$$

$$
N=10000\rightarrow249\mu s
$$

### Conclusión

> El ABB no garantiza \(O(\log N)\). Su búsqueda depende de la altura. En el caso ordenado, la altura llega a N y la búsqueda pasa a comportarse como \(O(N)\).

---

# 24. Comparación fundamental: ABB aleatorio vs. ABB ordenado

Esta comparación debes saberla muy bien.

### ABB aleatorio

$$
h\ll N
$$

→ crecimiento lento de la búsqueda.

### ABB ordenado

$$
h\approx N
$$

→ crecimiento lineal de la búsqueda.

### Frase ideal

> El mismo ABB presenta comportamientos completamente diferentes dependiendo del orden de inserción. Con inserción aleatoria, el árbol mantiene una altura relativamente pequeña; con inserción ordenada, se degenera y su altura pasa a ser aproximadamente N.

---

# 25. ¿Qué ocurre con el B+?

El B+ presenta un comportamiento muy estable.

En búsqueda aleatoria se observaron aproximadamente:

* \(N=500\) → 0.195 μs
* \(N=1000\) → 0.24 μs
* \(N=2500\) → 0.274 μs
* \(N=5000\) → 0.30 μs
* \(N=10000\) → 0.31–0.34 μs

El crecimiento es muy pequeño en comparación con la lista.

Además, cuando los datos se insertan ordenadamente, el B+ mantiene su eficiencia.

Para \(N=10000\):

$$
B+\approx0.34\mu s
$$

frente aproximadamente a:

$$
ABB\ ordenado\approx250\mu s
$$

y:

$$
Lista\approx110\mu s
$$

### Conclusión

> El B+ mostró los menores tiempos de búsqueda en las condiciones evaluadas y mantuvo un comportamiento estable frente al orden de inserción.

---

# 26. ¿Por qué el B+ puede ser más rápido que el ABB si ambos tienen O(log N)?

Porque Big-O describe el crecimiento asintótico, no el tiempo exacto.

Dos estructuras pueden tener:

$$
O(\log N)
$$

pero diferentes constantes y diferentes costos por operación.

Además, el B+ tiene:

* múltiples claves por nodo;
* múltiples caminos;
* altura pequeña;
* estructura balanceada.

En nuestros resultados, por ejemplo:

```text
N=1000  → h ≈ 3
N=2500  → h ≈ 3
N=5000  → h ≈ 3
N=10000 → h ≈ 4
```

Esto ayuda a explicar por qué el número de niveles que debe recorrer una búsqueda permanece muy pequeño.

---

# 27. ¿Qué significa la altura?

La altura indica cuántos niveles debe atravesar una búsqueda desde la raíz hasta la posición correspondiente.

### ABB ordenado

$$
h\approx N
$$

### ABB aleatorio

$$
h\ll N
$$

### B+

$$
h\approx2-4
$$

en los tamaños evaluados.

Por eso la altura es una variable muy importante para explicar los tiempos de búsqueda de los árboles.

---

# 28. ¿Qué significa `pendiente_log_log`?

Esta parte corresponde directamente al archivo de análisis.

Se representa:

$$
\log(T)
$$

contra:

$$
\log(N)
$$

Si:

$$
T(N)\approx cN^p
$$

entonces:

$$
\log(T)\approx\log(c)+p\log(N)
$$

y la pendiente de la regresión representa aproximadamente \(p\).

### Interpretación general

|   Pendiente | Interpretación                     |
| ----------: | ---------------------------------- |
|         ≈ 1 | crecimiento aproximadamente lineal |
| entre 0 y 1 | crecimiento sublineal              |
| cercana a 0 | crecimiento muy lento              |
|         ≈ 2 | crecimiento cuadrático             |

### Pero hay una precisión MUY importante

Una complejidad:

$$
O(\log N)
$$

**no significa matemáticamente que la pendiente log-log sea exactamente 0**.

Para un algoritmo logarítmico:

$$
T(N)\sim\log N
$$

por lo que:

$$
\log T=\log(\log N)
$$

y eso no tiene una pendiente constante.

Por eso la pendiente log-log debe utilizarse como:

> **indicador empírico del crecimiento en el rango de tamaños estudiado**, no como una demostración matemática de la complejidad asintótica.

---

# 29. ¿Qué muestran los nuevos resultados del archivo de análisis?

Los resultados son:

| Estructura | Orden     | Operación | Pendiente log-log | Interpretación                      |
| ---------- | --------- | --------- | ----------------: | ----------------------------------- |
| Lista      | Aleatorio | Búsqueda  |         **0.941** | Crecimiento cercano a \(O(N)\)      |
| ABB        | Aleatorio | Búsqueda  |         **0.245** | Crecimiento sublineal y muy lento   |
| B+         | Aleatorio | Búsqueda  |         **0.141** | Crecimiento aún más lento/sublineal |

### Lista

$$
p=0.941
$$

Está muy cerca de:

$$
p=1
$$

por lo que los datos presentan un crecimiento empírico cercano al lineal.

Esto coincide con:

$$
O(N)
$$

para la búsqueda secuencial.

---

### ABB aleatorio

$$
p=0.245
$$

Es mucho menor que 1.

Esto indica un crecimiento sublineal y mucho más lento que el de la lista.

Es consistente con el comportamiento esperado de un ABB aleatorio, cuya altura crece mucho más lentamente que N.

---

### B+

$$
p=0.141
$$

Es todavía menor.

Esto indica que dentro del rango experimental el tiempo presenta un crecimiento muy lento.

Esto es consistente con el hecho de que la altura del B+ se mantiene muy pequeña.

### Frase correcta para defenderlo

> La lista presenta una pendiente cercana a uno, lo que respalda su comportamiento lineal. El ABB aleatorio y el B+ presentan pendientes mucho menores, indicando un crecimiento sublineal y mucho más lento. Esto es consistente con el comportamiento esperado de estructuras de búsqueda basadas en árboles balanceados, aunque la pendiente log-log por sí sola no demuestra matemáticamente una complejidad \(O(\log N)\).

---

# 30. ¿Por qué no podemos decir simplemente "la pendiente demuestra O(log N)"?

Porque sería una sobreinterpretación.

La complejidad teórica proviene del análisis del algoritmo.

La pendiente nos proporciona evidencia experimental sobre el patrón de crecimiento observado.

### Respuesta perfecta

> La pendiente log-log no demuestra por sí sola la complejidad asintótica. Es un indicador empírico que permite comparar la velocidad de crecimiento de los tiempos. En nuestro caso, las pendientes pequeñas del ABB y del B+ son consistentes con el crecimiento lento esperado, mientras que la pendiente de la lista, cercana a uno, es consistente con un crecimiento lineal.

---

# 31. ¿Qué ocurre con la operación de listado?

Teóricamente listar es O(N) en las tres estructuras (la Lista necesita ordenar, O(N log N) en general). Con N = 10000, el tiempo de **una** ejecución fue:

| Orden | Lista | ABB | B+ |
| --- | ---: | ---: | ---: |
| Aleatorio | 1.28 ms | 0.68 ms | 0.045 ms |
| Ordenado | 0.52 ms | 0.60 ms | 0.054 ms |

Las pendientes log-log estuvieron entre 0.84 y 1.10, compatibles con crecimiento casi lineal.

### Cosas que puedes decir

* El B+ lista más rápido porque solo recorre sus hojas enlazadas, sin recorrer nodos ni ordenar.
* La Lista tarda menos cuando los datos ya vienen ordenados (1.28 ms frente a 0.52 ms): es compatible con que `sorted` aproveche que la entrada ya está ordenada. **Es una explicación esperable, no algo que el experimento haya comprobado.**
* El ABB lista en tiempo casi igual en ambos órdenes, porque el recorrido inorden visita los mismos N nodos.

### Cuidado

> No digas "como el número de ejecuciones es X, entonces la complejidad es Y". El número de ejecuciones solo depende de la ventana de 1 s. Analiza cómo cambia el tiempo **de una ejecución** al aumentar N.

---

# 32. ¿Qué muestran los resultados de inserción?

Con N = 10000, el tiempo de **construir** la estructura (una ejecución) fue:

| Orden | Lista | ABB | B+ |
| --- | ---: | ---: | ---: |
| Aleatorio | 0.41 ms | 9.0 ms | 4.1 ms |
| Ordenado | 0.41 ms | 2147 ms | 3.4 ms |

Pendientes log-log: Lista 0.94, ABB aleatorio 1.19, B+ aleatorio 1.11, B+ ordenado 1.08, **ABB ordenado 1.98**.

### Qué concluir

* **ABB con IDs ordenados:** la construcción crece de forma cuadrática. Cada inserción recorre toda la cadena (altura N), así que insertar N elementos cuesta 1 + 2 + … + N ≈ N²/2 pasos. Con N = 10000 son 2.15 s, unas 240 veces más que con IDs aleatorios.
* **B+:** casi no cambia con el orden (4.1 ms frente a 3.4 ms). Su costo por inserción es logarítmico y no se degrada.
* **Lista:** es la más rápida para insertar (0.41 ms) porque solo agrega al final, O(1) por elemento. Pero es la más lenta para buscar: es un compromiso entre inserción y búsqueda.
* El B+ es más lento que la Lista al insertar porque busca la hoja y a veces la divide.

### Respuesta corta

> La inserción confirma lo que mostró la búsqueda: el ABB es muy sensible al orden de inserción y el B+ no. Con IDs ordenados, la construcción del ABB pasó de milisegundos a más de dos segundos con N = 10000, y su pendiente log-log fue cercana a 2.

---

# 33. ¿Cuál fue la estructura más rápida para búsqueda?

En las condiciones del experimento:

$$
\boxed{B+}
$$

presentó los menores tiempos de búsqueda.

Pero debes formularlo científicamente.

### NO digas:

> "B+ siempre es mejor."

### Di:

> En las condiciones de este experimento, el B+ presentó los menores tiempos de búsqueda y mostró mayor estabilidad frente al orden de inserción.

---

# 34. ¿Por qué B+ es más estable ante el orden de inserción?

Porque mantiene el árbol balanceado.

Cuando se insertan nuevos elementos, el B+ puede dividir nodos y reorganizar la estructura para mantener una altura pequeña.

Por eso no ocurre la misma degeneración observada en el ABB ordenado.

### Respuesta

> El B+ mantiene su balance mediante la división y reorganización de nodos, por lo que el orden en que llegan los elementos no produce una cadena degenerada como ocurre en un ABB sin balanceo.

---

# 35. ¿Cuál es el principal resultado sobre el orden de inserción?

### Respuesta corta para memorizar

> El orden de inserción afecta principalmente al ABB. Con datos aleatorios, el ABB mantiene una altura relativamente pequeña y la búsqueda crece lentamente. Con datos ordenados, el ABB se degenera hasta tener altura aproximadamente N y la búsqueda pasa a tener comportamiento lineal. El B+ mantiene su estructura balanceada y por eso es mucho más estable frente al orden de inserción.

---

# 36. ¿Cuál es el resultado más importante del experimento?

La conclusión más interesante no es simplemente que B+ sea rápido.

Es:

$$
\boxed{
\text{estructura}
+
\text{forma de construcción}
+
\text{tamaño de entrada}
\rightarrow
\text{comportamiento observado}
}
$$

### Frase para la sustentación

> El experimento demuestra que no basta con conocer el nombre de una estructura de datos. También debemos considerar cómo se construye, cuál es su altura o estructura interna y cómo cambia el costo de las operaciones cuando aumenta el tamaño de entrada.

---

# 37. Tabla teórica que debes saber

| Estructura    | Inserción                    | Búsqueda                     | Listado  | Dependencia del orden |
| ------------- | ---------------------------- | ---------------------------- | -------- | --------------------- |
| Lista         | depende de implementación    | **O(N)**                     | **O(N)** | baja                  |
| ABB aleatorio | aprox. **O(log N)** esperado | aprox. **O(log N)** esperado | **O(N)** | alta                  |
| ABB ordenado  | **O(N)**                     | **O(N)**                     | **O(N)** | muy alta              |
| B+            | **O(log N)**                 | **O(log N)**                 | **O(N)** | baja                  |

### Aclaración fundamental

Para ABB:

$$
\boxed{\text{búsqueda}=O(h)}
$$

y solamente cuando:

$$
h=O(\log N)
$$

podemos obtener:

$$
O(\log N)
$$

---

# 38. Si te preguntan: "¿Por qué el ABB aleatorio no tiene altura exactamente log₂(N)?"

### Respuesta

> Porque un ABB construido aleatoriamente no necesariamente queda perfectamente balanceado. La expresión log₂(N) corresponde aproximadamente a la altura de un árbol perfectamente balanceado. Un ABB aleatorio puede tener una altura mayor, pero mientras su crecimiento sea mucho menor que N, su comportamiento sigue siendo muy diferente al de un árbol degenerado.

---

# 39. Si te preguntan: "¿Entonces el ABB aleatorio es O(log N) o no?"

### Respuesta rigurosa

> La búsqueda de un ABB es O(h), donde h es la altura. Bajo inserciones aleatorias esperamos, en promedio, una altura del orden de log N, por lo que la búsqueda tiene comportamiento promedio cercano a O(log N). Sin embargo, el peor caso sigue siendo O(N).

---

# 40. Si te preguntan: "¿Por qué el ABB ordenado es tan malo?"

### Respuesta

> Porque el ABB no realiza balanceo automático. Al insertar los elementos ordenadamente, cada nuevo elemento termina siguiendo el mismo camino hacia un lado, formando una estructura degenerada similar a una lista. Por eso la altura pasa a ser aproximadamente N y la búsqueda pasa a tener comportamiento O(N).

---

# 41. Si te preguntan: "¿Por qué el B+ no sufre el mismo problema?"

### Respuesta

> Porque el B+ mantiene una estructura balanceada. Cuando se insertan elementos puede dividir nodos y reorganizar la estructura para conservar una altura pequeña. Por eso el orden de llegada de los datos no produce la misma degeneración que observamos en el ABB.

---

# 42. Si te preguntan: "¿Por qué utilizar una semilla?"

### Respuesta

> Para garantizar reproducibilidad. Al utilizar una semilla fija, la generación aleatoria produce los mismos datos cada vez que ejecutamos el experimento bajo las mismas condiciones.

---

# 43. Si te preguntan: "¿Por qué utilizar cinco repeticiones?"

### Respuesta

> Porque una única medición puede estar afectada por ruido del sistema, procesos en segundo plano o variaciones temporales. Las cinco repeticiones permiten observar la variabilidad y obtener una medida más representativa del comportamiento.

---

# 44. Si te preguntan: "¿Por qué usar M ejecuciones?"

### Respuesta

> Porque una sola operación puede ser demasiado rápida para medirla con suficiente precisión. Al repetirla muchas veces acumulamos un tiempo mayor y después dividimos por M para estimar el costo promedio de una operación.

---

# 45. Si te preguntan: "¿Por qué utilizar tamaños diferentes?"

### Respuesta

> Porque queremos observar cómo escala el tiempo de ejecución. Si utilizáramos únicamente un tamaño, podríamos comparar tiempos puntuales, pero no podríamos estudiar el crecimiento de la operación.

---

# 46. Si te preguntan: "¿Por qué utilizar orden aleatorio y ordenado?"

### Respuesta

> Para estudiar el efecto de la forma de construcción sobre el ABB. El orden aleatorio representa un escenario donde el árbol tiende a evitar la degeneración, mientras que el ordenado representa un caso desfavorable que puede convertir el ABB en una estructura similar a una lista.

---

# 47. Si te preguntan: "¿Qué resultado te sorprendió?"

### Respuesta

> El comportamiento del ABB ordenado. Inicialmente podría pensarse que utilizar un árbol siempre proporciona una búsqueda eficiente, pero los resultados muestran que el comportamiento depende de cómo se construye. Para N=10.000 el ABB ordenado alcanza altura 10.000 y su búsqueda llega aproximadamente a 250 μs, mientras que el ABB aleatorio se mantiene alrededor de 1 μs y el B+ alrededor de 0.3 μs.

---

# 48. ¿Qué limitaciones tiene el experimento?

Debes conocerlas.

### 1. Hardware

Los tiempos absolutos dependen del computador utilizado.

### 2. Sistema operativo

Procesos en segundo plano pueden introducir ruido.

### 3. Resolución del temporizador

Las operaciones individuales son muy rápidas.

### 4. Ventana de medición

Los tiempos cercanos a un segundo son consecuencia de la metodología de benchmark.

### 5. Rango de tamaños

El experimento llega hasta:

$$
N=10000
$$

No podemos extrapolar indefinidamente.

### 6. Distribución de los datos

El comportamiento de un ABB aleatorio depende de la distribución y orden concretos utilizados.

### 7. Constantes ocultas

Big-O describe el crecimiento, pero no determina las constantes ni los costos concretos de cada implementación.

---

# 49. ¿Qué NO podemos concluir?

No podemos afirmar:

> "El B+ siempre es más rápido que cualquier ABB."

Ni:

> "El B+ siempre será mejor."

Ni:

> "La pendiente demuestra matemáticamente Big-O."

Ni:

> "Como una medición duró un segundo, una operación tarda un segundo."

Ni:

> "Estos mismos tiempos se obtendrán en cualquier computador."

### La conclusión correcta es:

> Bajo las condiciones experimentales utilizadas, el B+ presentó los menores tiempos de búsqueda y una mayor estabilidad frente al orden de inserción.

---

# 50. ¿Cómo reproducir el experimento?

La metodología puede resumirse así:

### Paso 1

Implementar:

* Lista
* ABB
* B+

### Paso 2

Utilizar los tamaños:

```text
10
50
100
500
1000
2500
5000
10000
```

### Paso 3

Para cada tamaño generar los escenarios:

```text
aleatorio
ordenado
```

### Paso 4

Construir cada estructura.

### Paso 5

Ejecutar:

```text
inserción
búsqueda
listado
```

### Paso 6

Realizar cinco repeticiones.

### Paso 7

Utilizar el número \(M\) de ejecuciones determinado por la metodología de medición y calibración.

### Paso 8

Medir el tiempo total.

### Paso 9

Calcular:

$$
T_{\text{promedio}}
=
\frac{T_{\text{total}}}{M}
$$

### Paso 10

Registrar:

* estructura;
* orden de inserción;
* N;
* M;
* repetición;
* operación;
* tiempo;
* ejecuciones;
* altura cuando corresponda.

### Paso 11

Construir tablas y gráficas.

### Paso 12

Comparar:

$$
\text{resultado experimental}
\leftrightarrow
\text{complejidad teórica}
$$

---

# 51. Hardware y software

En la sustentación debes mencionar exactamente el hardware y software registrados en el informe del experimento.

La estructura de respuesta debe ser:

> El experimento se ejecutó en [equipo utilizado], utilizando [procesador], [memoria RAM] y [sistema operativo]. El software utilizado fue [lenguaje/versión y herramientas empleadas]. Se mantuvo el mismo entorno para las diferentes estructuras con el objetivo de hacer la comparación bajo condiciones equivalentes.

### Importante

No debes inventar estos datos durante la sustentación. Debes utilizar exactamente los valores que aparecen en el informe o archivo del experimento.

---

# 52. ¿Cuál es la relación entre teoría y experimento?

Esta es una pregunta muy importante.

### Teoría

Nos dice cómo debería crecer el costo de la operación cuando \(N\) aumenta.

### Experimento

Nos muestra qué ocurrió realmente bajo las condiciones utilizadas.

Por ejemplo:

### Lista

Teoría:

$$
O(N)
$$

Experimento:

$$
p=0.941
$$

→ comportamiento empírico cercano a lineal.

### ABB aleatorio

Teoría:

$$
O(\log N)
$$

en condiciones promedio favorables.

Experimento:

$$
p=0.245
$$

→ crecimiento sublineal y muy lento.

### B+

Teoría:

$$
O(\log N)
$$

Experimento:

$$
p=0.141
$$

→ crecimiento aún más lento en el rango evaluado.

### Conclusión

> Los resultados experimentales son consistentes en términos generales con las tendencias teóricas, pero las mediciones no sustituyen el análisis matemático de complejidad.

---

# 53. ¿Por qué los resultados reales no son exactamente iguales a la teoría?

Porque el tiempo de ejecución depende de muchos factores:

* implementación;
* hardware;
* memoria caché;
* sistema operativo;
* procesos en segundo plano;
* distribución de los datos;
* constantes de cada estructura;
* rango de tamaños;
* mecanismo de medición.

Por eso:

$$
O(\log N)
$$

no significa:

> "siempre tardará exactamente X microsegundos".

Significa:

> "su crecimiento con respecto a N está acotado asintóticamente por un comportamiento logarítmico bajo las condiciones correspondientes."

---

# 54. Las 10 cosas que DEBES memorizar

Si antes de la sustentación solamente puedes memorizar diez cosas, memoriza estas:

### 1.

**Lista → búsqueda O(N).**

### 2.

**ABB → búsqueda O(h).**

### 3.

**ABB aleatorio → comportamiento promedio cercano a O(log N).**

### 4.

**ABB ordenado → h ≈ N → búsqueda O(N).**

### 5.

**B+ → árbol balanceado de múltiples caminos.**

### 6.

**Listado → O(N) para las tres estructuras.**

### 7.

**Tamaños: 10, 50, 100, 500, 1000, 2500, 5000 y 10000.**

### 8.

**Cinco repeticiones por configuración.**

### 9.

**Tiempo promedio = tiempo total / M.**

### 10.

**Las pendientes log-log son evidencia experimental, no una demostración matemática de Big-O.**

---

# 55. Las pendientes del archivo de análisis que debes memorizar

Esta tabla es especialmente importante porque corresponde al resultado final del análisis:

| Estructura    | Pendiente |
| ------------- | --------: |
| Lista         | **0.941** |
| ABB aleatorio | **0.245** |
| B+            | **0.141** |

### Cómo explicarlo de memoria

> La lista obtuvo una pendiente de 0.941, muy cercana a uno, por lo que presenta crecimiento aproximadamente lineal. El ABB obtuvo 0.245 y el B+ 0.141, valores mucho menores que uno, lo que indica un crecimiento sublineal y mucho más lento. Estos resultados son consistentes con el comportamiento esperado de los árboles de búsqueda, aunque una pendiente log-log no demuestra por sí sola una complejidad O(log N).

---

# 56. La historia completa del experimento en 30 segundos

Si el profesor dice:

> **"Explíqueme rápidamente su experimento."**

Puedes responder:

> Comparamos una lista, un ABB y un B+ para las operaciones de inserción, búsqueda y listado, utilizando tamaños entre 10 y 10.000 elementos. Para analizar el efecto de la construcción utilizamos órdenes de inserción aleatorio y ordenado. Cada configuración se repitió cinco veces y las búsquedas se ejecutaron M veces para obtener tiempos suficientemente medibles. Los parámetros utilizados fueron seleccionados previamente mediante un archivo de calibración. Observamos que la lista presenta crecimiento aproximadamente lineal en búsqueda; el ABB aleatorio presenta un crecimiento mucho más lento, mientras que el ABB ordenado se degenera, alcanza altura N y presenta comportamiento lineal. El B+ mantiene una altura pequeña y presentó los menores tiempos de búsqueda. Finalmente, utilizamos un análisis log-log para comparar empíricamente las tendencias de crecimiento con las complejidades teóricas.

---

# 57. La conclusión final de la sustentación

Si el profesor pregunta:

> **"¿Cuál es la conclusión general de su experimento?"**

Esta es una excelente respuesta:

> El experimento muestra que el comportamiento práctico de una estructura de datos depende tanto de su complejidad teórica como de la forma en que se construye y de las condiciones de ejecución.
>
> La lista presenta un crecimiento aproximadamente lineal en búsqueda, respaldado por una pendiente log-log de 0.941. El ABB presenta un comportamiento muy dependiente del orden de inserción: con datos aleatorios mantiene una altura relativamente pequeña y un crecimiento mucho más lento, mientras que con datos ordenados se degenera, alcanza una altura aproximadamente igual a N y su búsqueda adquiere comportamiento lineal.
>
> Por otro lado, el B+ mantiene una estructura balanceada y una altura muy pequeña, por lo que presentó los menores tiempos de búsqueda y mayor estabilidad frente al orden de inserción en las condiciones evaluadas. Su pendiente log-log de 0.141 también muestra un crecimiento empírico muy lento.
>
> En conclusión, los resultados experimentales son consistentes en términos generales con las predicciones teóricas y muestran por qué las estructuras balanceadas son importantes cuando se busca mantener un buen comportamiento al aumentar el tamaño de los datos y ante diferentes órdenes de inserción.

---

# ⭐ IDEA CENTRAL QUE DEBES TENER PRESENTE

Tu experimento **no demuestra simplemente que "B+ es más rápido"**.

La historia realmente importante es:

$$
\boxed{
\text{estructura}
+
\text{forma de construcción}
+
\text{tamaño de entrada}
\rightarrow
\text{comportamiento observado}
}
$$

La evidencia más fuerte es:

### ABB aleatorio

$$
h\approx20-35
$$

para tamaños de hasta 10.000.

### ABB ordenado

$$
h=N
$$

en los tamaños grandes.

### B+

$$
h\approx2-4
$$

incluso con \(N=10000\).

Y el análisis log-log refuerza esta historia:

$$
\boxed{
\text{Lista}=0.941
\qquad
\text{ABB}=0.245
\qquad
\text{B+}=0.141
}
$$

Por tanto, la idea que debes defender no es simplemente:

> **"B+ es más rápido."**

Sino:

> **"La estructura y la forma en que se construye determinan cómo escala el costo de las operaciones. El ABB evidencia claramente que una estructura de búsqueda puede perder su eficiencia cuando se degenera, mientras que el B+ mantiene su balance y presenta un crecimiento mucho más estable."**
