LAB 2
Estudiante: Daniela Andrea Gallego Díaz
CC: 1001470496




Implementación de un Árbol de Merkle

Descripción

Este proyecto implementa un Árbol de Merkle utilizando Python y el algoritmo de hash SHA-256.

Un Árbol de Merkle permite representar un conjunto de datos mediante una única cadena llamada Raíz de Merkle (Merkle Root).

Cada transacción se convierte primero en un hash SHA-256. Luego, los hashes se agrupan de dos en dos y se calcula un nuevo hash para cada pareja. Este proceso se repite hasta obtener un único hash, que corresponde a la raíz del árbol.

En este proyecto también se implementa una prueba de inclusión, que permite comprobar si una determinada transacción pertenece al árbol sin necesidad de guardar todo el árbol.




Objetivos

El programa permite:

1. Crear 5 transacciones simuladas.
2. Construir un Árbol de Merkle utilizando SHA-256 y obtener y mostrar la raíz de Merkle.
3. Modificar una transacción y comprobar que la raíz cambia.
4. Generar una prueba de inclusión para la transacción 3 y verificar que pertenece al árbol.
5. Intentar verificar un dato incorrecto y comprobar que la verificación falla.




Estructura del programa

Se compone de varias funciones:

sha256(data)

Calcula y devuelve el hash SHA-256 de los datos recibidos.

generar_prueba_raiz(transacciones, indice)

Construye los niveles del Árbol de Merkle hasta obtener la raíz y, al mismo tiempo, genera la prueba de inclusión para la transacción indicada.

Devuelve:

* La raíz del árbol.
* La prueba de inclusión.

concatenar(nivel)

Combina los hashes de un nivel de dos en dos y calcula el hash de cada nodo padre para formar el siguiente nivel.

posicion_hermano(indice, nivel)

Obtiene el hash hermano del nodo indicado y determina si este se encuentra a la izquierda o a la derecha.

verificar_prueba(dato, prueba, raiz_esperada)

Comprueba si un dato pertenece al árbol reconstruyendo la raíz a partir del dato y de la prueba de inclusión.

Devuelve:

* True si la raíz reconstruida coincide con la raíz esperada.
* False si no coincide.




Diagrama del Árbol de Merkle

El proyecto utiliza las siguientes cinco transacciones:

T1 = Alice -> Bob: 10
T2 = Bob -> Carol: 5
T3 = Carol -> David: 2
T4 = David -> Alice: 1
T5 = Eve -> Alice: 7

Como hay un número impar de transacciones, T5 se duplica:

                           RAÍZ
                         /      \
                      H1234     H55
                      /   \     / \
                    H12   H34  H5  H5
                   /  \   /  \
                 H1   H2 H3   H4
                 │    │  │    │
                 T1   T2 T3   T4
                             
                         T5 → T5

De forma simplificada:

H1 = SHA-256(T1)
H2 = SHA-256(T2)
H3 = SHA-256(T3)
H4 = SHA-256(T4)
H5 = SHA-256(T5)

H12   = SHA-256(H1 + H2)
H34   = SHA-256(H3 + H4)
H1234 = SHA-256(H12 + H34)
H55   = SHA-256(H5 + H5)

RAÍZ = SHA-256(H1234 + H55)




Prueba de inclusión

Para verificar la tercera transacción, no es necesario guardar todo el árbol.

La prueba contiene los hashes hermanos necesarios para reconstruir el camino desde la transacción hasta la raíz.

El proceso es:

Hash de T3
   │
   ├── + hash hermano
   ↓
Hash del padre
   │
   ├── + hash hermano
   ↓
   RAÍZ

Si la raíz reconstruida es igual a la raíz original, la prueba es válida.




Resultados esperados

La estructura de la salida será similar a:

ÁRBOL DE MERKLE

Raíz original:
[hash]

Ingrese una nueva transacción para reemplazar la primera:
[entrada]

Nueva raíz:
[hash diferente]

¿La raíz cambió?
True

Prueba de inclusión de la transacción 3:
Válida

Ingrese un dato incorrecto para comprobar la prueba:
[entrada]

Verificación del dato incorrecto:
Inválida


Los valores de los hashes pueden variar dependiendo de las transacciones utilizadas.




Conclusión

La implementación demuestra cómo un Árbol de Merkle permite representar un conjunto de datos mediante una única raíz y cómo una prueba de inclusión permite verificar una transacción sin necesidad de almacenar todo el árbol.