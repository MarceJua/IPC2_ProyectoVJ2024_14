import os
class NodoPila:
    def __init__(self,idUser,nombreUser,idProducto,nombreProducto,cantidad, total) :
        self.idUser=idUser
        self.nombreUser=nombreUser
        self.idProducto=idProducto
        self.nombreProducto=nombreProducto
        self.cantidad=cantidad
        self.total=total
        self.abajo=None

class Pila:
    def __init__(self) -> None:
        self.cima=None
        self.size=0
    
    def append(self,idUser,nombreUser,idProducto,nombreProducto,cantidad, total) :
        nuevo=NodoPila(idUser,nombreUser,idProducto,nombreProducto,cantidad, total)
        nuevo.abajo=self.cima
        self.cima=nuevo
        self.size+=1

    def vaciar(self):
        while self.cima is not None:
            nodo_a_eliminar = self.cima
            self.cima = self.cima.abajo  # Mover la cima de la pila al nodo de abajo
            del nodo_a_eliminar  # Eliminar el nodo
            self.size -= 1

    
    def graficar(self,iduser):
        try:
         codigodot = ''
         archivo = open(f'reportesdot/pila{iduser}.dot', 'w')
         codigodot += '''digraph G {
     rankdir=TB;
     node[shape=record];\n'''

         actual = self.cima
         contador = 0
         while actual is not None:
            label = f"ID: {actual.idUser}\\nUsuario: {actual.nombreUser}\\nProducto ID: {actual.idProducto}\\nProducto: {actual.nombreProducto}\\nCantidad: {actual.cantidad}\\nTotal: {actual.total}"
            codigodot += f'node{contador} [label="{label}"];\n'
            if actual.abajo is not None:
                codigodot += f'node{contador} -> node{contador + 1};\n'
            actual = actual.abajo
            contador += 1

         codigodot += "}"

        # GENERAMOS EL DOT
         archivo.write(codigodot)
         archivo.close()

        # GENERAMOS LA IMAGEN
         ruta_dot = f'reportesdot/pila{iduser}.dot'
         ruta_imagen = f'reportes/pila{iduser}.png'
         comando = 'dot -Tpng ' + ruta_dot + ' -o ' + ruta_imagen
         os.system(comando)

         # ABRIR LA IMAGEN
         # convierte la ruta a una ruta válida para windows
         ruta_reporte = os.path.abspath(ruta_imagen)
         os.startfile(ruta_reporte)
        except:
            print("[ERROR] no se han cargado datos")

    def retornar_pila(self):
        if self.cima is None:
            return None

        actual = self.cima
        id_usuario = actual.idUser
        nombre_usuario = actual.nombreUser
        productos_str = ''
        total = 0

        while actual is not None:
            productos_str += f"{actual.nombreProducto} (Cantidad: {actual.cantidad}, Total: {actual.total}), "
            total += actual.total
            actual = actual.abajo

        # Eliminar la última coma y espacio
        resultado = f"ID Usuario: {id_usuario}\nNombre Usuario: {nombre_usuario}\nPRODUCTOS: {productos_str}\nTotal: {total}"
        print(resultado)
        return resultado

         
    

    
    
    






    
