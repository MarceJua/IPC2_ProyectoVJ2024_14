import os
class  NodoCompras:
    def __init__(self,comprastr) -> None:
        self.comprastr=comprastr
       
        self.siguiente=None
class listaSimple:
    def __init__(self) -> None:
        self.cabeza=None
        self.size=0
    def agregar(self,comprastr):
        nodo=NodoCompras(comprastr)
        if self.cabeza == None:
            self.cabeza = nodo
        else:
            actual = self.cabeza
            while actual != None:
                if actual.siguiente == None:
                    actual.siguiente = nodo
                    break
                actual = actual.siguiente
        self.size += 1
    def graficar(self):
        try:
         codigodot = ''
         archivo = open('reportesdot/lista_simple.dot', 'w')
         codigodot += '''digraph G {
   rankdir=LR;
   node [shape = record, height = .1]'''
         contador_nodos = 0
        #PRIMERO CREAMOS LOS NODOS
         actual = self.cabeza
         while actual != None:
            codigodot += 'node'+str(contador_nodos)+' [label = \"{'+ str(actual.comprastr)+'|<f1>}\"];\n'
            contador_nodos += 1
            actual = actual.siguiente

         #AHORA CREAMOS LAS RELACIONES
         actual = self.cabeza
         contador_nodos = 0
         while actual.siguiente != None:
            codigodot += 'node'+str(contador_nodos)+'-> node'+str(contador_nodos+1)+';\n'
            contador_nodos += 1
            actual = actual.siguiente

         codigodot += '}'

         #Lo escribimos en el archivo dot
         archivo.write(codigodot)
         archivo.close()

         #Generamos la imagen
         ruta_dot = 'reportesdot/lista_simple.dot'
         ruta_reporte = 'reportes/lista_simple.png'
         comando = 'dot -Tpng '+ruta_dot+' -o '+ruta_reporte
         os.system(comando)
         #Abrir la imagen
         #CONVERTIR DE RUTA RELATIVA A RUTA ABSOLUTA
         ruta_abrir_reporte = os.path.abspath(ruta_reporte)
         os.startfile(ruta_abrir_reporte)
         print('Reporte generado con éxito')
        except:
            print("vacio")