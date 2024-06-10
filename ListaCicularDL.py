import os
class NodoProductos:
    def __init__(self,id,precio,nombre,descripcion,categoria,cantidad, imagen) -> None:
        self.id=id
        self.nombre=nombre
        self.precio=precio
        self.descripcion=descripcion
        self.categoria=categoria
        self.cantidad=cantidad
        self.imagen=imagen
        self.siguiente=None
        self.anterior=None

class ListaDoblementeEnlazada:
    def __init__(self) -> None:
        self.cabeza=None
        self.ultimo=None
        self.size=0

    def agregar(self,id,precio,nombre,descripcion,categoria,cantidad, imagen):
        # Verificar que el nombre sea único
        if self.buscarPorId(id) is not None:
            print(f"Usuario con nombre '{id}' ya existe.")
            return

        # Crear un nuevo nodo
        nuevoNodo = NodoProductos(id,precio,nombre,descripcion,categoria,cantidad, imagen)
        
        if self.cabeza is None:
            # La lista está vacía, el nuevo nodo será el primero y el último
            self.cabeza = nuevoNodo
            self.ultimo = nuevoNodo
            # Enlazar el nuevo nodo consigo mismo (lista circular)
            nuevoNodo.siguiente = nuevoNodo
            nuevoNodo.anterior = nuevoNodo
        else:
            # La lista no está vacía, insertar al final
            nuevoNodo.anterior = self.ultimo  # El anterior del nuevo nodo es el nodo actual último
            nuevoNodo.siguiente = self.cabeza  # El siguiente del nuevo nodo es el nodo cabeza
            self.ultimo.siguiente = nuevoNodo  # El siguiente del nodo actual último es el nuevo nodo
            self.cabeza.anterior = nuevoNodo  # El anterior del nodo cabeza es el nuevo nodo
            self.ultimo = nuevoNodo  # Actualizar el último nodo de la lista al nuevo nodo
        
        self.size += 1  # Incrementar el tamaño de la lista


    def buscarPorId(self, id):
        if self.cabeza is None:
            return None
        actual = self.cabeza
        while True:
            if actual.id == id:
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None
    def imprimirLista(self):
        if self.cabeza is None:
            print("La lista está vacía.")
            return
        actual = self.cabeza
        while True:
            print(f"{actual.id} id: {actual.id} nombre: {actual.nombre} precio: {actual.precio} descripcion: {actual.descripcion} telefono: {actual.telefono}")
            actual = actual.siguiente
            if actual == self.cabeza:
                break

    def graficar(self):
        codigo_dot = ''
        archivo = open('reportesdot/listaProductos.dot', 'w')
        codigo_dot += '''digraph G {
  rankdir=LR;
  node [shape = record,  height = .5]\n'''
        
        actual = self.cabeza
        contador_nodos = 0
        # PRIMERO CREAMOS LOS NODOS
        if actual is not None:
            while True:
                codigo_dot += f'node{contador_nodos} [label = "{{ID: {actual.id}|Nombre: {actual.nombre}|nombre: {actual.nombre}|Precio: {actual.precio}|descripcion: {actual.descripcion}|cantidad: {actual.cantidad}|:categoria {actual.categoria}|imagen: {actual.imagen}}}"];\n'
                contador_nodos += 1
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

        # HACEMOS LAS RELACIONES
        actual = self.cabeza
        contador_nodos = 0
        if actual is not None:
            while True:
                siguiente_nodo = (contador_nodos + 1) % self.size  # Para circularidad
                codigo_dot += f'node{contador_nodos} -> node{siguiente_nodo};\n'
                codigo_dot += f'node{siguiente_nodo} -> node{contador_nodos};\n'
                contador_nodos += 1
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

        codigo_dot += '}'
        archivo.write(codigo_dot)
        archivo.close()

        # GENERAMOS LA IMAGEN
        ruta_dot = 'reportesdot/listaProductos.dot'
        ruta_imagen = 'reportes/listaProductos.png'
        comando = 'dot -Tpng ' + ruta_dot + ' -o ' + ruta_imagen
        os.system(comando)

        # ABRIR LA IMAGEN
        # convierte la ruta a una ruta válida para windows
        ruta_reporte = os.path.abspath(ruta_imagen)
        os.startfile(ruta_reporte)