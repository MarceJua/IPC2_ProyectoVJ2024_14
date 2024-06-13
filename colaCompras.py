import os
class nodoCola:
    def __init__(self,compraStr) :
        self.compraStr=compraStr
        self.siguiente =None

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.size = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, compraStr):
        nuevo_nodo = nodoCola(compraStr)
        if self.final:
            self.final.siguiente = nuevo_nodo
        self.final = nuevo_nodo
        if self.frente is None:
            self.frente = nuevo_nodo
        self.size += 1

    def desencolar(self):
        if self.esta_vacia():
            print("desencolar desde una cola vacía")
        dato = self.frente.compraStr
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.size -= 1
        return dato

    def obtener_frente(self):
        if self.esta_vacia():
            raise IndexError("obtener el frente de una cola vacía")
        return self.frente.compraStr

    def obtener_tamaño(self):
        return self.size

    def vaciar(self):
        while not self.esta_vacia():
            self.desencolar()
    
    import os

    def graficar(self):
     try:
      codigo_dot = 'digraph G {\n'
      codigo_dot += 'rankdir=LR;\n'
      codigo_dot += 'node [shape=record];\n'
    
      actual = self.frente
      contador_nodos = 0

    # Crear nodos
      while actual is not None:
        codigo_dot += f'nodo{contador_nodos} [label="{actual.compraStr}"];\n'
        contador_nodos += 1
        actual = actual.siguiente

    # Crear conexiones
      for i in range(contador_nodos - 1):
        codigo_dot += f'nodo{i} -> nodo{i + 1};\n'

      codigo_dot += '}'

    # Guardar archivo .dot
      with open('reportesdot/cola.dot', 'w') as archivo:
        archivo.write(codigo_dot)

    #  Generar la imagen usando Graphviz
      comando = 'dot -Tpng reportesdot/cola.dot -o reportes/cola.png'
      os.system(comando)

    # Abrir la imagen
      ruta_imagen = os.path.abspath('reportes/cola.png')
      os.startfile(ruta_imagen)
     except:
        print("vacio")

        