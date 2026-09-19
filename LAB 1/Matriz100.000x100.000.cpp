#include <iostream>
#include <fstream>
using namespace std;

const int N = 100000;
const int TAM = 10;

// Crear la matriz
void crearmatriz() {
    ofstream archivo("matriz.bin", ios::binary);
    if (!archivo) {
        cout << "No se pudo crear el archivo." << endl;
        return;
    }

    int* fila = new int[N];
    int separador = -1;

    for (int i = 0; i < N; i++) {

        // Crear la fila
        for (int j = 0; j < N; j++) {
            fila[j] = i + j;
        }

        // Escribir la fila en el archivo
        archivo.write(
            reinterpret_cast<char*>(fila),
            N * sizeof(int)
        );

        // Escribir el separador al final de la fila
        archivo.write(
            reinterpret_cast<char*>(&separador),
            sizeof(int)
        );
    }

    delete[] fila;
    archivo.close();
}


// Mostrar una sección de la matriz
void mostrarSeccion(
    ifstream& archivo,
    int filaInicio,
    int columnaInicio
) {

    int* fila = new int[N];

    // Recorrer las filas que queremos mostrar
    for (int i = filaInicio; i < filaInicio + TAM; i++) {

        // Cada fila ocupa:
        // N enteros + 1 separador
        archivo.seekg(
            static_cast<long long>(i) *
            (N + 1) *
            sizeof(int),
            ios::beg
        );

        // Leer la fila completa
        archivo.read(
            reinterpret_cast<char*>(fila),
            N * sizeof(int)
        );

        // Mostrar solamente las columnas necesarias
        for (
            int j = columnaInicio;
            j < columnaInicio + TAM;
            j++
        ) {
            cout << fila[j] << "\t";
        }

        cout << endl;
    }

    delete[] fila;

    cout << endl;
}


int main() {

    // Crear la matriz
    crearmatriz();

    // Abrir el archivo para lectura
    ifstream archivo("matriz.bin", ios::binary);

    if (!archivo) {
        cout << "No se pudo abrir el archivo." << endl;
        return 1;
    }

    cout << "MATRIZ DE " << N << " x " << N << endl;
    cout << "========================================\n\n";


    // Esquina superior izquierda
    cout << "Esquina superior izquierda:\n";
    mostrarSeccion(archivo, 0, 0);


    // Centro de la matriz
    cout << "Centro de la matriz:\n";
    mostrarSeccion(archivo, 50000, 50000);


    // Esquina inferior derecha
    cout << "Esquina inferior derecha:\n";
    mostrarSeccion(archivo, 99990, 99990);


    archivo.close();

    return 0;
}