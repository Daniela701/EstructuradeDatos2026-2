#LAB 2
#Daniela Andrea Gallego Díaz - CC 1001470496

#La función def sha256 fue hecha con IA, con el propósito de calcular hashes SHA-256 pedidos en este laboratorio
import hashlib #librería sugerida por la IA para la función def sha256 para la realización del cálculo

#Función que devuelve el hash SHA-256 de una cadena de texto (hecho con IA)
def sha256(data):

    if not isinstance(data, bytes): #comprueba si data no es de tipo bytes (SHA-256 trabaja internamente con bytes)
        data = data.encode("utf-8") #converte la data a bytes usando UTF-8
    return hashlib.sha256(data).hexdigest() #hace el cálculo SHA-256

# Función que nos permite hacer los cálculos en hojas y ramas, construir y retornar la raíz y obtener el resultado de la prueba de inclusión
def generar_prueba_raiz(transacciones, indice):

    nivel = [] # lista para guardar el nivel que se está procesando
    # hojas
    for t in transacciones:
        nivel.append(sha256(t))

    prueba = []
    while len(nivel) > 1:

        if len(nivel) % 2 != 0:
            nivel.append(nivel[-1]) # duplicamos la hoja o el padre

        hermano, posicion = posicion_hermano(indice, nivel)
        prueba.append((hermano, posicion))
        siguiente_nivel = concatenar(nivel)
        nivel = siguiente_nivel
        indice = indice // 2

    raiz = nivel[0]

    return raiz, prueba

#Función para concatenar los hijos y aplica el cálculo SHA256
def concatenar(nivel):

    siguiente_nivel = []
    i = 0
    while i < len(nivel):
        izquierda = nivel[i]
        derecha = nivel[i + 1]
        concatenacion = izquierda + derecha
        padre = sha256(concatenacion)
        siguiente_nivel.append(padre)
        i= i + 2

    return siguiente_nivel

#Funcion para calcular el hermano y su posicion (derecha o izquierda)
def posicion_hermano(indice, nivel):

    hermano = indice + 1 if indice % 2 == 0 else indice - 1

    if indice % 2 == 0:
        posicion = "derecha"
    else:
        posicion = "izquierda"

    return nivel[hermano], posicion

#Funcion para verificar si una transaccion pertenece al arbol (comparamos raices)
def verificar_prueba(dato, prueba, raiz_esperada):
    hash_actual = sha256(dato)

    for hash_hermano, posicion in prueba:

        if posicion == "izquierda":
            concatenacion = hash_hermano + hash_actual
        else:
            concatenacion = hash_actual + hash_hermano

        hash_actual = sha256(concatenacion)

    return hash_actual == raiz_esperada

#main
if __name__ == "__main__":

    #Punto 1
    #Estas transacciones fueron sugeridas por la IA
    transacciones = [
        "Alice -> Bob: 10",
        "Bob -> Carol: 5",
        "Carol -> David: 2",
        "David -> Alice: 1",
        "Eve -> Alice: 7"
    ]

    print("ÁRBOL DE MERKLE")

    #Punto 2
    # Construir el árbol, obtener la raíz y generar la prueba
    raiz, prueba = generar_prueba_raiz(transacciones, 2)

    print("\nRaíz original:")
    print(raiz)

    #Punto 3
    # Modificar una transacción
    transacciones_modificadas = transacciones.copy()

    transacciones_modificadas[0] = input(
        "\nIngrese una nueva transacción para reemplazar la primera: "
    )

    # Construir nuevamente el árbol con la transacción modificada
    raiz_nueva, _ = generar_prueba_raiz(transacciones_modificadas, 2)

    print("\nNueva raíz:")
    print(raiz_nueva)

    print("\n¿La raíz cambió?")
    print(raiz != raiz_nueva)

    #Punto 4
    # Verificar la prueba de inclusión de la transacción 3
    resultado = verificar_prueba(transacciones[2],prueba,raiz)

    print("\nPrueba de inclusión de la transacción 3:")
    print("Válida" if resultado else "Inválida")

    #Punto 5
    # Verificar con un dato incorrecto
    dato_incorrecto = input(
        "\nIngrese un dato incorrecto para comprobar la prueba: "
    )

    resultado = verificar_prueba(
        dato_incorrecto,
        prueba,
        raiz
    )

    print("\nVerificación del dato incorrecto:")
    print("Válida" if resultado else "Inválida")