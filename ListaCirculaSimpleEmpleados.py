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
    def agregar(self, codigo, nombre, puesto):
        nuevo_nodo =nodoEmpleados(codigo, nombre, puesto)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        self.size += 1
    
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
                if siguiente_nodo == 0:
                    # Si es la relación del último nodo al primero, usamos una flecha curva
                    codigo_dot += f'node{contador_nodos} -> node{siguiente_nodo} [constraint=false];\n'
                else:
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
        