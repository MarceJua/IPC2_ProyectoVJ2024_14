import os

from listaOrtogonal.listaCabecera import ListaCabecera
from listaOrtogonal.nodoCabecera import NodoCabecera
from listaOrtogonal.nodoCelda import NodoCelda

class MatrizDispersa:
    def __init__(self):
        self.filas = ListaCabecera("fila")
        self.columnas = ListaCabecera("columna")
    
    def insertar(self, id, nombre, descripcion, empleado, dia, hora):
        nuevo = NodoCelda(id, nombre, descripcion, empleado, dia, hora)
        celda_x = self.filas.obtenerCabecera(dia)
        celda_y = self.columnas.obtenerCabecera(hora)

        if celda_x is None:
            celda_x = NodoCabecera(dia)
            self.filas.insertarNodoCabecera(celda_x)
        if celda_y is None:
            celda_y = NodoCabecera(hora)
            self.columnas.insertarNodoCabecera(celda_y)

        if celda_x.acceso is None:
            celda_x.acceso = nuevo
        else:
            if nuevo.hora < celda_x.acceso.hora:
                nuevo.derecha = celda_x.acceso
                celda_x.acceso.izquierda = nuevo
                celda_x.acceso = nuevo
            else:
                actual = celda_x.acceso
                while actual is not None:
                    if nuevo.hora < actual.hora:
                        nuevo.derecha = actual
                        nuevo.izquierda = actual.izquierda
                        actual.izquierda.derecha = nuevo
                        actual.izquierda = nuevo
                        break
                    elif nuevo.dia == actual.dia and nuevo.hora == actual.hora:
                        break
                    else:
                        if actual.derecha is None:
                            actual.derecha = nuevo
                            nuevo.izquierda = actual
                            break
                        else:
                            actual = actual.derecha

        if celda_y.acceso is None:
            celda_y.acceso = nuevo
        else:
            if nuevo.dia < celda_y.acceso.dia:
                nuevo.abajo = celda_y.acceso
                celda_y.acceso.arriba = nuevo
                celda_y.acceso = nuevo
            else:
                actual2 = celda_y.acceso
                while actual2 is not None:
                    if nuevo.dia < actual2.dia:
                        nuevo.abajo = actual2
                        nuevo.arriba = actual2.arriba
                        actual2.arriba.abajo = nuevo
                        actual2.arriba = nuevo
                        break
                    elif nuevo.dia == actual2.dia and nuevo.hora == actual2.hora:
                        break
                    else:
                        if actual2.abajo is None:
                            actual2.abajo = nuevo
                            nuevo.arriba = actual2
                            break
                        else:
                            actual2 = actual2.abajo

    def recorridoFilas(self, fila):
        print('--------------Recorrido por fila------------------')
        inicio = self.filas.obtenerCabecera(fila)
        if inicio is None:
            print('La fila no existe')
            return 
        
        actual = inicio.acceso
        while actual is not None:
            print(f'{str(actual.id)}, {str(actual.nombre)}, {str(actual.descripcion)}, {str(actual.empleado)}, {str(actual.dia)}, {str(actual.hora)}')
            actual = actual.derecha

    def recorridoColumnas(self, columna):
        print('--------------Recorrido por columna------------------')
        inicio = self.columnas.obtenerCabecera(columna)
        if inicio is None:
            print('La columna no existe')
            return 
        
        actual = inicio.acceso
        while actual is not None:
            print(f'{str(actual.id)}, {str(actual.nombre)}, {str(actual.descripcion)}, {str(actual.empleado)}, {str(actual.dia)}, {str(actual.hora)}')
            actual = actual.abajo

    def buscar(self, dia, hora):
        actual = self.filas.obtenerCabecera(dia).acceso
        while actual is not None:
            if actual.hora == hora:
                return actual
            actual = actual.derecha
        return None
    

"""# Ejemplo de uso:
matriz = MatrizDispersa()
matriz.insertar(1, "Atención al Cliente", "Atender a los clientes de la tienda", 1, 2, 14)
matriz.insertar(2, "Limpieza de estanterías", "Limpiar y ordenar las estanterias del pasillo 1", 1, 1, 7)

print(matriz.to_xml())"""