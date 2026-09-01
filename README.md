Nombre Estudiante: Daniela Andrea Gallego Díaz
Matriz 100.000 × 100.000 en disco

Descripción

Este programa crea una matriz de 100.000 × 100.000 elementos y la almacena en un archivo binario (matriz.bin) en el disco.

La matriz contiene un total de 10.000.000.000 elementos. Cada elemento es de tipo int (4 bytes), por lo que el archivo generado ocupa aproximadamente 40 GB.

Funcionamiento

Debido al gran tamaño de la matriz, no se almacena completa en la memoria RAM. En su lugar, el programa:

1. Reserva memoria únicamente para una fila de 100.000 elementos.
2. Genera los valores de cada fila mediante fila[j] = i + j.
3. Escribe cada fila directamente en el archivo binario.
4. Libera la memoria utilizada y cierra el archivo.
5. Abre nuevamente el archivo para realizar la lectura.
6. Utiliza seekg() para desplazarse directamente hasta las filas necesarias.
7. Muestra tres secciones de 10 × 10:
    * Esquina superior izquierda.
    * Centro de la matriz.
    * Esquina inferior derecha.

De esta manera, es posible trabajar con una matriz de aproximadamente 40 GB sin cargarla completamente en memoria RAM.

Ejemplo

La esquina superior izquierda se visualiza como:

0   1   2   3   4   5   6   7   8   9
1   2   3   4   5   6   7   8   9   10
2   3   4   5   6   7   8   9   10  11
...

El programa también muestra una sección del centro y otra de la esquina inferior derecha para comprobar el acceso a diferentes posiciones de la matriz.

Cada fila de la matriz se almacena consecutivamente en el archivo binario y al finalizar cada fila se escribe un valor separador de tipo int, en este caso -1. De esta manera se puede identificar dónde termina cada fila y comienza la siguiente. Como el separador ocupa el mismo tamaño que un int, cada fila ocupa 400.004 bytes. Esto también permite calcular mediante seekg() la posición de cualquier fila.

Tecnologías

* C++
* iostream
* fstream
* Archivos binarios
* Acceso aleatorio mediante seekg()
