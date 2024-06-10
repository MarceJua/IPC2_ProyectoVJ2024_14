import os
class nodoEmpleados:
     def __init__(self, codigo, nombre, puesto,):
        self.codigo =codigo
        self.nombre = nombre
        self.puesto=puesto
        self.siguiente = None

class ListaCircularSimple:
    def __init__(self) -> None:
        self.cabeza=None # apuntadores
        self.ultimo=None
        self.size=0
    def agregar(self,codigo,nombre,puesto):
        if self.codigoUnico(codigo):
            nuevoNodo=nodoEmpleados(codigo,nombre,puesto)
            if self.cabeza is None:
                # Si la lista está vacía, el nuevo nodo es tanto la cabeza como el último nodo
                self.cabeza = nuevoNodo
                self.ultimo = nuevoNodo
                nuevoNodo.siguiente = self.cabeza  # Enlazar al nuevo nodo consigo mismo
            else:
                # Si la lista no está vacía, insertar al final
                self.ultimo.siguiente = nuevoNodo  # El nodo actual último apunta al nuevo nodo como su siguiente
                nuevoNodo.siguiente = self.cabeza  # El nuevo nodo apunta a la cabeza
                self.ultimo = nuevoNodo  # El nuevo nodo se convierte en el último nodo de la lista
            self.size += 1  # Incrementa el tamaño de la lista en 1
        else:
            # Si el nombre no es único, imprime un mensaje de error y no agrega el nodo
            print(f"Error: El id '{id}' ya existe en la lista. No se puede agregar.")
    
    def graficar(self):
        codigo_dot = ''
        archivo = open('reportesdot/listaVendedores.dot', 'w')
        codigo_dot += '''digraph G {
  rankdir=LR;
  node [shape = record, height = .1]\n'''
        
        actual = self.cabeza
        contador_nodos = 0
        if actual is not None:
            while True:
                # Crear nodos
                codigo_dot += f'node{contador_nodos} [label = "{{Codigo: {actual.codigo}|nombre: {actual.nombre}|puesto: {actual.puesto}}}"];\n'
                contador_nodos += 1
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

        actual = self.cabeza
        contador_nodos = 0
        if actual is not None:
            while True:
                siguiente_nodo = (contador_nodos + 1) % self.size
                # Crear relaciones entre nodos
                codigo_dot += f'node{contador_nodos} -> node{siguiente_nodo};\n'
                contador_nodos += 1
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

        codigo_dot += '}'
        archivo.write(codigo_dot)
        archivo.close()

        # Generar la imagen
        ruta_dot = 'reportesdot/listaVendedores.dot'
        ruta_imagen = 'reportes/listaVendedores.png'
        comando = 'dot -Tpng ' + ruta_dot + ' -o ' + ruta_imagen
        os.system(comando)

        # Abrir la imagen
        ruta_reporte = os.path.abspath(ruta_imagen)
        os.startfile(ruta_reporte)




            
            

    def codigoUnico(self, codigo):
        # Verifica si el id es único en la lista
        if self.cabeza is None:
            return True
        actual = self.cabeza
        while True:
            if actual.codigo == codigo:
                return False  # Si encuentra un id igual, retorna False
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return True  # Si no encuentra ningún id igual, retorna True
        